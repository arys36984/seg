from django.test import TestCase
from django.urls import reverse
from django.db import transaction

from loans.forms import BookForm
from loans.models import Book

import datetime

class CreateBookTest(TestCase):
    def setUp(self):
        self.url = reverse('create_book')
        self.form_input = {
            'authors': 'Doe, J.',
            'title': 'A title',
            'publication_date': "2024-09-01",
            'isbn': '123456789123',
        }

    def test_create_book_url(self):
        self.assertEqual(self.url, '/create_book/')

    def test_get_create_book(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_book.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(isinstance(form, BookForm))
        self.assertFalse(form.is_bound)

    def test_post_with_valid_data(self):
        before_count = Book.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Book.objects.count()
        self.assertEqual(before_count+1, after_count)
        expected_redirect_url = reverse("books")
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

    def test_post_with_invalid_data(self):
        self.form_input['authors'] = ''
        before_count = Book.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Book.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_book.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(isinstance(form, BookForm))
        self.assertTrue(form.is_bound)

    def test_post_with_non_unique_isbn(self):
        Book.objects.create(
            authors='Joe, D.',
            title='Another title',
            publication_date=datetime.datetime(2024,8,2),
            isbn="123456789123"
        )
        before_count = Book.objects.count()
        with transaction.atomic():
            response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Book.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_book.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(isinstance(form, BookForm))
        self.assertTrue(form.is_bound)