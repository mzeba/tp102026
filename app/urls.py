from django.urls import path

from app import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.AuthorListView.as_view(), name="home"),
    path("authors/new/", views.author_create, name="author_create"),
    path("authors/<int:pk>/", views.AuthorDetailView.as_view(), name="author_detail"),
    path("books/", views.book_list, name="book_list"),
    path("books/new/", views.book_create, name="book_create"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
]
