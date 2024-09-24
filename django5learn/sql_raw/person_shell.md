# Commands

## Raw sql
>>>
>>> for p in Person.objects.raw("SELECT * FROM sql_raw_person"):
...     print(p)

## Mapping query fields to model fields¶
>>>
>>> Person.objects.raw("SELECT id, first_name, last_name, birth_date FROM sql_raw_person")
>>> Person.objects.raw("SELECT last_name, birth_date, first_name, id FROM sql_raw_person")

-- Matching is done by name.So if you had some other table that had Person data in it, you could easily map it into Person instances:
>>> Person.objects.raw(
...     """
...     SELECT first AS first_name,
...            last AS last_name,
...            bd AS birth_date,
...            pk AS id,
...     FROM sql_raw_person
...     """
... )
-- Alternatively, you can map fields in the query to model fields using the translations argument to raw()
>>> name_map = {"first": "first_name", "last": "last_name", "bd": "birth_date", "pk": "id"}
>>> Person.objects.raw("SELECT * FROM sql_raw_person", translations=name_map)

## Index lookups
>>>
>>> first_person = Person.objects.raw("SELECT * FROM sql_raw_person")[0]
-- However, the indexing and slicing are not performed at the database level. If you have a large number of Person objects in your database, it is more efficient to limit the query at the SQL level:
>>> first_person = Person.objects.raw("SELECT * FROM sql_raw_person LIMIT 1")[0]

## Adding annotations (age only available in postgres)
>>>
>>> people = Person.objects.raw("SELECT *, age(birth_date) AS age FROM sql_raw_person")
>>> for p in people:
...     print("%s is %s." % (p.first_name, p.age))

## Passing parameters into raw()
>>>
>>> lname = "Doe"
>>> Person.objects.raw("SELECT * FROM sql_raw_person WHERE last_name = %s", [lname])

## ![Executing custom SQL directly](https://docs.djangoproject.com/en/5.1/topics/db/sql/#executing-custom-sql-directly)
>>>
