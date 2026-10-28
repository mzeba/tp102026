from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from app.models import Author, Book

# Create your views here.


def home(request):
    authors = Author.objects.all()
    return render(request, "home.html", context={"authors": authors})
