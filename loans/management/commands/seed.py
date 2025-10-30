from faker import Faker
from loans.models import Book
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
	help = "Seed the Book table"

	def handle(self, *args, **options):
		fake = Faker()
		for _ in range(100):
			author = f"{fake.last_name()}, {fake.first_name()}"
			title = fake.sentence()
			publication_date = fake.date()
			isbn = fake.unique.isbn13().replace('-','')
			Book.objects.create(authors = author, title = title, 
                                publication_date = publication_date, 
                                isbn = isbn)