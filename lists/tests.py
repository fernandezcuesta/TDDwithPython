from django.test import TestCase

class SmokeTest(TestCase):

    def test_fails(self):
        self.assertEqual(1 + 1, 3)