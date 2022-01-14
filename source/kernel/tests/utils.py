import unittest

# Custom TestCase
class BaseTestCase(unittest.TestCase):
    def assertLengthEqual(self, iterable, length):
        self.assertEqual(len(iterable), length)
    
    def assertIsEmpty(self, iterable):
        self.assertLengthEqual(iterable, 0)

    def assertIsNotEmpty(self, iterable):
        self.assertNotEqual(len(iterable), 0)

    def assertJustOneElementIn(self, iterable, element):
        self.assertEqual(iterable, [element])

    def assertIncludedIn(self, element, iterable):
        self.assertTrue(element in iterable)

    def denyIncludedIn(self, element, iterable):
        self.assertFalse(element in iterable)