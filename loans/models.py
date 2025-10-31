from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.
class Book (models.Model):
    authors = models.CharField(max_length=255, validators=[MinLengthValidator(4)])
    title = models.CharField(max_length=255)
    publication_date = models.DateField()
    isbn = models.CharField(max_length = 13, unique=True)

    def __str__(self):
        return(f'{self.authors} ({self.publication_date}) "{self.title}" ISBN {self.isbn}.' )
    
class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return(f"Member {self.id}: {self.last_name}, {self.first_name} <{self.email}>")
    
class Loan(models.Model):
    member = models.ForeignKey(Member, on_delete=models.SET_NULL)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL)
    start_at = models.DateField()
    end_at = models.DateField()
