# Relationships

- **Many-to-one relationships**
  - To define a many-to-one relationship, use django.db.models.ForeignKey.
    - You can also create recursive relationships (an object with a many-to-one relationship to itself)

- **Many-to-many relationships**
  - To define a many-to-many relationship, use ManyToManyField.
  - you can also create recursive relationships (an object with a many-to-many relationship to itself)
    - It doesn’t matter which model has the ManyToManyField, but you should only put it in one of the models – not both.
    - Generally, ManyToManyField instances should go in the object that’s going to be edited on a form

- **One-to-one relationships**
  - To define a one-to-one relationship, use OneToOneField.