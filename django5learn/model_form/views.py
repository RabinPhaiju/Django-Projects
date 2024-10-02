from django.forms import Textarea, modelform_factory
from django.shortcuts import render
from .models import AuthorForm,BookForm,AuthorForm1,Author

def authorForm(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():

            print(form.cleaned_data["name"] )
            print(form.cleaned_data["slug"] )
            return render(request, "author_form.html", {"form": form,"message": "Author Created"})
    else:
        form = AuthorForm(
            initial={
                "slug": "This is slug",
            }
        ) #default way
        # form = modelform_factory(Author, form=AuthorForm, widgets={"title": Textarea()}) # factory way

    return render(request, "author_form.html", {"form": form})


def bookForm(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["name"] )
            print(form.cleaned_data["authors"] )
            return render(request, "book_form.html", {"form": form,"message": "Book Created"})
    else:
        form = BookForm() #default way
    return render(request, "book_form.html", {"form": form})