# Commands

# Manager
>>>
>>> Person.people.all()
>>> Person.authors.all()
>>> Person.editors.all()

## Calling custom QuerySet methods from the manager
>>>
>>> Person.people.all()
>>> Person.people.authors().all()
>>> Person.people.editors().all()

