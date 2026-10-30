from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count

from app.models import Author, Book

# Create your views here.


def index(request):
    return redirect("home")

def home(request):
    query = request.GET.get("q", "").strip()
    authors = Author.objects.annotate(book_count=Count("books")).order_by("lastname")
    if query:
        authors = authors.filter(
            Q(firstname__icontains=query) | Q(lastname__icontains=query)
        )
    return render(request, "home.html", context={"authors": authors, "query": query})


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = author.books.order_by("-publication_date")
    return render(
        request, "author_detail.html", context={"author": author, "books": books}
    )


def book_list(request):
    query = request.GET.get("q", "").strip()
    books = Book.objects.select_related("author").order_by("title")
    if query:
        books = books.filter(
            Q(title__icontains=query)
            | Q(isbn__icontains=query)
            | Q(author__firstname__icontains=query)
            | Q(author__lastname__icontains=query)
        )
    return render(request, "book_list.html", context={"books": books, "query": query})


def book_detail(request, pk):
    book = get_object_or_404(Book.objects.select_related("author"), pk=pk)
    return render(request, "book_detail.html", context={"book": book})
