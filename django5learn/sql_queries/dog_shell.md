# Commands

## Create
>>> Dog.objects.create(name="Max", data=None)  # SQL NULL.
>>> Dog.objects.create(name="Archie", data=Value(None, JSONField()))  # JSON null.
>>> Dog.objects.filter(data=None)
>>> Dog.objects.filter(data=Value(None, JSONField()))
>>> Dog.objects.filter(data__isnull=True)
>>> Dog.objects.filter(data__isnull=False)

## Key, index, and path transforms
>>>
>>> Dog.objects.create(
...     name="Rufus",
...     data={
...         "breed": "labrador",
...         "owner": {
...             "name": "Bob",
...             "other_pets": [
...                 {
...                     "name": "Fishy",
...                 }
...             ],
...         },
...     },
... )
>>> Dog.objects.create(name="Meg", data={"breed": "collie", "owner": None})
>>> Dog.objects.filter(data__breed="collie")
>>> Dog.objects.filter(data__owner__name="Bob")
>>> Dog.objects.filter(data__owner__other_pets__0__name="Fishy")

## KT() expressions
>>>
-- Represents the text value of a key, index, or path transform of JSONField
>>> Dog.objects.create(
...     name="Shep",
...     data={
...         "owner": {"name": "Bob"},
...         "breed": ["collie", "lhasa apso"],
...     },
... )
>>> Dogs.objects.annotate(first_breed=KT("data__breed__1"), owner_name=KT("data__owner__name")).filter(first_breed__startswith="lhasa", owner_name="Bob")


## contains loopup
>>>
>>> Dog.objects.create(name="Rufus", data={"breed": "labrador", "owner": "Bob"})
>>> Dog.objects.create(name="Meg", data={"breed": "collie", "owner": "Bob"})
>>> Dog.objects.create(name="Fred", data={})
>>> Dog.objects.filter(data__contains={"owner": "Bob"})
>>> Dog.objects.filter(data__contains={"breed": "collie"})

## contained_by lookup
>>>
-- This is the inverse of the contains lookup

## has_key lookup
>>>
-- Returns objects where the given key is in the top-level of the data
>>> Dog.objects.create(name="Rufus", data={"breed": "labrador"})
>>> Dog.objects.create(name="Meg", data={"breed": "collie", "owner": "Bob"})
>>> Dog.objects.filter(data__has_key="owner")

## has_keys | has_any_keys lookup
