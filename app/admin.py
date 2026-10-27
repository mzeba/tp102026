from django.contrib import admin

from app.models import Author, Book

# Register your models here.

admin.site.register([Author, Book])
