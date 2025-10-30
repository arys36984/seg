from django.test import TestCase
from loans.helpers import is_prime
from parameterized import parameterized

class IsPrimeTestCase(TestCase):
    @parameterized.expand([
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (5, True),
        (7, True),
        (9, False),
        (11, True),
        (15, False),
        (27, False),
        (2017, True),
        (2117, False)
    ])
    def test_is_prime_with_positive_integer(self, number, expected_result):
        actual_result = is_prime(number)
        self.assertEqual(expected_result, actual_result)

    def test_0_raises_exception(self):
        with self.assertRaises(ValueError):
            is_prime(0)

    def test_negative_raises_exception(self):
        with self.assertRaises(ValueError):
            is_prime(-1)

    def test_string_raises_exception(self):
        with self.assertRaises(ValueError):
            is_prime("string")