from django import forms

from app.models import Author, Book


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["firstname", "lastname", "birthdate", "email"]
        widgets = {
            "birthdate": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_date", "isbn", "summary"]
        widgets = {
            "publication_date": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
            "summary": forms.Textarea(attrs={"rows": 5}),
        }
