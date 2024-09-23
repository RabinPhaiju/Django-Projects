from django.contrib import admin

# Register your models here.
from .models import Blog,Author,Entry
from .models import Dog

from .models import BookAuthor,Book,Publisher,Store


admin.site.register(Blog)
admin.site.register(Author)
admin.site.register(Entry)

admin.site.register(Dog)


admin.site.register(BookAuthor)
admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Store)
