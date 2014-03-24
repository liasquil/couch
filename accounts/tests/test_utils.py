from django.test import TestCase
from django.test.client import Client, RequestFactory

from accounts.utils import looks_like_email

class LooksLikeEmailTests(TestCase):
    def test_false_positive(self):
        self.assertFalse(looks_like_email('foo@bar'))
        self.assertFalse(looks_like_email('foo.bar@foo'))
        self.assertFalse(looks_like_email('foo@@bar'))
        self.assertFalse(looks_like_email('foo@@bar.foo'))

    def test_false_negative(self):
        self.assertTrue(looks_like_email('foo@bar.net'))
        self.assertTrue(looks_like_email('foo.bar@bar.foo.net'))



