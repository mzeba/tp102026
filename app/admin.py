from django.contrib import admin

from app.models import Author, Book

# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "birthdate", "email")
    search_fields = ("firstname", "lastname", "books__title")


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_date", "isbn")
    search_fields = ("title", "author__firstname", "author__lastname", "isbn")


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
