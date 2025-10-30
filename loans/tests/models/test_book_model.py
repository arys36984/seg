from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

import datetime

from loans.models import Book

class BookTestCase(TestCase):
    def setUp(self):
        authors = "Doe, J."
        title = "A title"
        publication_date = datetime.datetime(2020, 1, 1)
        isbn = "123456789123"
        self.book = Book(authors=authors, title=title, publication_date=publication_date, isbn=isbn)

    def test_book_is_valid(self):
        try:
            self.book.full_clean()
        except ValidationError:
            self.fail("Default test book should be deemed valid")

    def test_book_with_blank_author_is_invalid(self):
        self.book.authors = ''
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_overlong_author_is_invalid(self):
        self.book.authors = 'x' * 256
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_short_author_is_invalid(self):
        self.book.authors = 'x' * 3
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_blank_title_is_invalid(self):
        self.book.title = ''
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_overlong_title_is_invalid(self):
        self.book.title = 'x' * 256
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_blank_publication_date_is_invalid(self):
        self.book.publication_date = None
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_non_date_publication_date_is_invalid(self):
        self.book.publication_date = "not a date"
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_blank_isbn_is_invalid(self):
        self.book.isbn = ''
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_overlong_isbn_is_invalid(self):
        self.book.isbn = 'x' * 14
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_isbn_must_be_unique(self):
        self.book.save()
        authors = "Doe"
        title = "Another title"
        publication_date = datetime.datetime(2020, 2, 2)
        isbn = "123456789123"
        with self.assertRaises(IntegrityError):
            Book.objects.create(authors=authors, title=title, publication_date=publication_date, isbn = isbn)

    def test_string(self):
        required_string = 'Doe, J. (2020-01-01 00:00:00) "A title" ISBN 123456789123.'
        self.assertEqual(self.book.__str__(), required_string)