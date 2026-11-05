from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from app.forms import AuthorForm, BookForm
from app.models import Author, Book

# Create your views here.

PER_PAGE = 12


def paginate(request, queryset):
    """Retourne la page demandée (?page=) et la liste des numéros à afficher."""
    paginator = Paginator(queryset, PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    page_range = paginator.get_elided_page_range(
        page_obj.number, on_each_side=1, on_ends=1
    )
    return page_obj, page_range


def index(request):
    return redirect("home")


class AuthorListView(ListView):
    model = Author
    template_name = "home.html"
    context_object_name = "authors"
    ordering = ["lastname", "firstname"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj, page_range = paginate(self.request, context["authors"])
        context["authors"] = page_obj
        context["page_range"] = page_range
        context["query"] = self.request.GET.get("q", "").strip()
        return context

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        queryset = super().get_queryset().annotate(book_count=Count("books"))
        if query:
            queryset = queryset.filter(
                Q(firstname__icontains=query) | Q(lastname__icontains=query)
            )
        return queryset


class AuthorDetailView(DetailView):
    model = Author
    template_name = "author_detail.html"
    context_object_name = "author"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.order_by("-publication_date")
        return context


def author_create(request):
    form = AuthorForm(request.POST or None)
    if form.is_valid():
        author = form.save()
        messages.success(request, f"L'auteur « {author} » a bien été ajouté.")
        return redirect("author_detail", pk=author.pk)
    return render(
        request,
        "form.html",
        context={
            "form": form,
            "title": "Nouvel auteur",
            "cancel_url": reverse("home"),
        },
    )


def book_list(request):
    query = request.GET.get("q", "").strip()
    books = Book.objects.select_related("author").order_by("title", "pk")
    if query:
        books = books.filter(
            Q(title__icontains=query)
            | Q(isbn__icontains=query)
            | Q(author__firstname__icontains=query)
            | Q(author__lastname__icontains=query)
        )
    page_obj, page_range = paginate(request, books)
    return render(
        request,
        "book_list.html",
        context={
            "books": page_obj,
            "page_obj": page_obj,
            "page_range": page_range,
            "query": query,
        },
    )


def book_create(request):
    # ?author=<pk> : ajout depuis la fiche d'un auteur (auteur présélectionné)
    author_id = request.GET.get("author", "")
    author = get_object_or_404(Author, pk=author_id) if author_id.isdigit() else None

    form = BookForm(request.POST or None, initial={"author": author})
    if form.is_valid():
        book = form.save()
        messages.success(request, f"Le livre « {book.title} » a bien été ajouté.")
        if author:
            return redirect("author_detail", pk=author.pk)
        return redirect("book_detail", pk=book.pk)
    return render(
        request,
        "form.html",
        context={
            "form": form,
            "title": f"Nouveau livre de {author}" if author else "Nouveau livre",
            "cancel_url": (
                reverse("author_detail", args=[author.pk])
                if author
                else reverse("book_list")
            ),
        },
    )


def book_detail(request, pk):
    book = get_object_or_404(Book.objects.select_related("author"), pk=pk)
    return render(request, "book_detail.html", context={"book": book})
