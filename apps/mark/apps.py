from django.apps import AppConfig


class MarkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.mark'

    def ready(self):
        # Import signals to register them
        import apps.mark.signals