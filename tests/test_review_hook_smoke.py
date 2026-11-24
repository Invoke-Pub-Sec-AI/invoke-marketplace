import unittest


def first_value(values):
    """Return the first value, or None when the list is empty."""
    return values[0]


class ReviewHookSmokeTest(unittest.TestCase):
    def test_empty_input_returns_none(self):
        self.assertIsNone(first_value([]))
