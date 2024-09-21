from django.contrib import admin

# Register your models here.
from .models import Blog,Author,Entry
from .models import Dog


admin.site.register(Blog)
admin.site.register(Author)
admin.site.register(Entry)

admin.site.register(Dog)
