from loans.models import Book
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
	help = "Unseed the book table"

	def handle(self, *args, **options):
		Book.objects.all().delete()