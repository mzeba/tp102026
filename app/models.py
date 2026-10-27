from django.db import models

# Create your models here.


class Author(models.Model):
    firstname = models.CharField(
        max_length=100,
        help_text="Saisissez le prénom de l'auteur",
        verbose_name="Prénom",
    )
    lastname = models.CharField(
        max_length=100, help_text="Saisissez le nom de l'auteur", verbose_name="Nom"
    )
    birthdate = models.DateField(verbose_name="Date de naissance")
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name = "Auteur"
        verbose_name_plural = "Auteurs"


class Book(models.Model):
    title = models.CharField(
        max_length=200, help_text="Saisissez le titre du livre", verbose_name="Titre"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name="books",
        help_text="Sélectionnez l'auteur du livre",
        verbose_name="Auteur",
    )
    publication_date = models.DateField(verbose_name="Date de publication")
    isbn = models.CharField(
        max_length=13,
        help_text="Saisissez l'ISBN du livre",
        verbose_name="ISBN",
        null=True,
        blank=True,
    )
    summary = models.TextField(
        help_text="Saisissez un résumé du livre",
        verbose_name="Résumé",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        verbose_name = "Livre"
        verbose_name_plural = "Livres"
