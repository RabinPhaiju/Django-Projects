import os
from collections import defaultdict
from typing import Any, Dict, List

import frontmatter
import yaml
from django.apps import apps
from django.db import models as db
from frontmatter.default_handlers import YAMLHandler
from py_yaml_fixtures import FixturesLoader as BaseFixturesLoader
from py_yaml_fixtures.factories.django import (
    DjangoModelFactory as BaseDjangoModelFactory,
)
from py_yaml_fixtures.fixtures_loader import MULTI_CLASS_FILENAMES
from py_yaml_fixtures.management.commands import import_fixtures
from py_yaml_fixtures.types import Identifier

from core.models import get_model

RECORDS_DATA_DIR = "records"


def get_metadata_value(metadata, key):
    default_metadata = {
        "noupdate": False,
        "model": None,
    }

    metadata = dict(default_metadata, **metadata)

    return metadata[key]


class DjangoModelFactory(BaseDjangoModelFactory):
    def maybe_convert_values(
        self,
        identifier: Identifier,
        data: Dict[str, Any],
    ):
        noupdate = data.pop("__noupdate__", None)
        rv = super().maybe_convert_values(identifier, data)

        return dict(rv, __noupdate__=noupdate)

    def create_or_update(
        self,
        identifier: Identifier,
        data: Dict[str, Any],
    ):
        if self.model_instances[identifier.class_name].get(identifier.key):
            return self.model_instances[identifier.class_name][identifier.key], False

        noupdate = data.pop("__noupdate__", False)

        kwargs, defaults, m2m = {}, {}, {}
        model_class = self.models[identifier.class_name]

        for k, v in data.items():
            if not hasattr(model_class, k):
                defaults[k] = v
                continue

            field = model_class._meta.get_field(k)

            if isinstance(field, (db.ManyToManyField, db.ManyToManyRel)):
                m2m[k] = v
                continue

            if field.primary_key or field.unique:
                kwargs[k] = v
            else:
                defaults[k] = v

        if not kwargs:
            kwargs = dict(defaults, __noupdate__=noupdate)
            instance, created = model_class.objects.from_fixture(**kwargs)
        else:
            kwargs = dict(kwargs, __noupdate__=noupdate)
            instance, created = model_class.objects.from_fixture(
                defaults,
                **kwargs,
            )

        for k, v in m2m.items():
            for obj in v:
                getattr(instance, k).add(obj)

        self.model_instances[identifier.class_name][identifier.key] = instance
        action = "Created" if created else ("Skipped" if noupdate else "Updated")
        return instance, action


class FixturesLoader(BaseFixturesLoader):
    def _load_data(self):
        """
        Load all fixtures from :attr:`fixtures_dir`
        """
        filepaths = []
        model_identifiers = defaultdict(list)

        # attempt to load fixture files from given directories (first pass)
        # for each valid model fixture file, read it into the cache and get the
        # list of identifier keys from it
        for fixtures_dir in self.fixture_dirs:
            for filename in os.listdir(fixtures_dir):
                filepath = os.path.join(fixtures_dir, filename)
                file_ext = filename[filename.find(".") + 1 :]

                # make sure it's a valid fixture file
                if os.path.isfile(filepath) and file_ext in {"yml", "yaml"}:
                    filepaths.append(filepath)
                    with open(filepath) as f:
                        self._file_cache[filepath] = f.read()

                    # preload to determine identifier keys
                    with self._preloading_env() as env:
                        rendered_yaml = env.get_template(filepath).render()

                        (metadata, content) = frontmatter.parse(
                            rendered_yaml, encoding="UTF-8", handler=YAMLHandler()
                        )

                        model_name = get_metadata_value(metadata, key="model")

                        if not get_model(model_name):
                            raise Exception(
                                "invalid model in fixutre file %s" % filepath
                            )

                        *_, class_name = model_name.split(".")

                        data = yaml.load(content, Loader=yaml.loader.SafeLoader)

                        model_identifiers[class_name] = list(data.keys())

        # second pass where we can render the jinja templates with knowledge of all
        # the model identifier keys (allows random_model and random_models to work)
        for filepath in filepaths:
            self._load_from_yaml(filepath, model_identifiers)

        self._loaded = True

    def _load_from_yaml(self, filepath: str, model_identifiers: Dict[str, List[str]]):
        """
        Load fixtures from the given filename
        """
        rendered_yaml = self.env.get_template(filepath).render(
            model_identifiers=model_identifiers
        )

        (metadata, content) = frontmatter.parse(
            rendered_yaml, encoding="UTF-8", handler=YAMLHandler()
        )

        model_name = get_metadata_value(metadata, key="model")
        noupdate = get_metadata_value(metadata, key="noupdate")

        if not get_model(model_name):
            raise Exception("invalid model in fixutre file %s" % filepath)

        *_, class_name = model_name.split(".")

        data = yaml.load(content, Loader=yaml.loader.SafeLoader)
        identifier_data = {}

        d, self.relationships[class_name] = self._post_process_yaml_data(
            data, self.factory.get_relationships(class_name)
        )
        identifier_data[class_name] = d

        for class_name, d in identifier_data.items():
            for identifier_key, instance_data in d.items():
                self.model_fixtures[class_name][identifier_key] = dict(
                    instance_data,
                    __noupdate__=noupdate,
                )


class Command(import_fixtures.Command):
    def handle(self, *args, **options):
        models = []
        fixture_dirs = []
        apps_with_fixtures = set()

        app_names = options.get("apps")
        app_configs = (
            [apps.get_app_config(app_name) for app_name in app_names]
            if app_names
            else apps.get_app_configs()
        )
        for app_config in app_configs:
            models.extend(app_config.get_models())
            fixtures_dir = os.path.join(app_config.path, RECORDS_DATA_DIR)
            if os.path.exists(fixtures_dir):
                fixture_dirs.append(fixtures_dir)
                apps_with_fixtures.add(app_config.name)
            for filename in MULTI_CLASS_FILENAMES:
                if os.path.exists(os.path.join(app_config.path, filename)):
                    if app_config.path not in fixture_dirs:
                        fixture_dirs.append(app_config.path)

        if not fixture_dirs:
            print("No records found. Exiting.")
            return

        factory = DjangoModelFactory(models)
        loader = FixturesLoader(factory, fixture_dirs=fixture_dirs)

        # factory = BaseDjangoModelFactory(models)
        # loader = BaseFixturesLoader(factory, fixture_dirs=fixture_dirs)

        print("Loading records from apps: " + ", ".join(sorted(apps_with_fixtures)))

        loader.create_all(
            lambda identifier, model, action: print(
                "{action} {identifier}: {model}".format(
                    action=action, identifier=identifier.key, model=repr(model)
                )
            )
        )

        print("Done loading records. Exiting.")
