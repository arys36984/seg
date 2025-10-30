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
