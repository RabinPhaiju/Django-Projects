# Commands

## Author
>>>
>>> from model_form.models import Author
>>> from model_form.forms import AuthorForm

## Create a form instance from POST data

>>> f = AuthorForm(request.POST)

## Save a new Author object from the form's data

>>> new_Author = f.save()

## Create a form to edit an existing Author, but use

-- POST data to populate the form.
>>> a = Author.objects.get(pk=1)
>>> f = AuthorForm(request.POST, instance=a)
>>> f.save()

-----------------------

## Create a form instance with POST data.

>>> f = AuthorForm(request.POST)

## Create, but don't save the new author instance.

>>> new_author = f.save(commit=False)

## Modify the author in some way.

>>> new_author.some_field = "some_value"

## Save the new instance.

>>> new_author.save()

## Now, save the many-to-many data for the form.

>>> f.save_m2m()
-- Calling save_m2m() is only required if you use save(commit=False)

