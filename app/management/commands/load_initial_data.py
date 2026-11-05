import json
from datetime import date
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from app.models import Author, Book

DEFAULT_FILE = Path(__file__).resolve().parents[2] / "initial" / "data.json"


class Command(BaseCommand):
    help = "Enregistre dans la base les auteurs et leurs livres à partir d'un fichier JSON."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=Path,
            default=DEFAULT_FILE,
            help=f"Chemin du fichier JSON (par défaut : {DEFAULT_FILE})",
        )

    def handle(self, *args, **options):
        path = Path(options["file"])
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise CommandError(f"Fichier introuvable : {path}")
        except json.JSONDecodeError as error:
            raise CommandError(f"JSON invalide dans {path} : {error}")

        authors_created = books_created = 0

        # Tout ou rien : en cas d'erreur, aucune donnée n'est enregistrée
        with transaction.atomic():
            for item in data:
                try:
                    author, created = Author.objects.update_or_create(
                        firstname=item["firstname"],
                        lastname=item["lastname"],
                        defaults={
                            "birthdate": date.fromisoformat(item["birthdate"]),
                            "email": item["email"],
                        },
                    )
                    authors_created += created

                    for book_item in item.get("books", []):
                        _, created = Book.objects.update_or_create(
                            title=book_item["title"],
                            author=author,
                            defaults={
                                "publication_date": date.fromisoformat(
                                    book_item["publication_date"]
                                ),
                                "isbn": book_item.get("isbn"),
                                "summary": book_item.get("summary"),
                            },
                        )
                        books_created += created
                except (KeyError, ValueError) as error:
                    raise CommandError(
                        f"Donnée invalide pour l'auteur {item.get('firstname')} "
                        f"{item.get('lastname')} : {error!r}"
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"{authors_created} auteur(s) et {books_created} livre(s) ajouté(s). "
                f"Total en base : {Author.objects.count()} auteur(s), "
                f"{Book.objects.count()} livre(s)."
            )
        )
