from django.contrib import admin

# Register your models here.
from .models import Laptop,Brand

admin.site.register(Brand)
admin.site.register(Laptop)