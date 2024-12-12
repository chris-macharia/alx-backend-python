import unittest
from unittest.mock import patch

def memoize(func):
    """A simple memoize decorator."""
    cache = {}

    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapper

class TestClass:
    def a_method(self):
        return 42

    @memoize
    def a_property(self):
        return self.a_method()

class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            test_instance = TestClass()
            
            # Call the memoized property twice
            first_call = test_instance.a_property()
            second_call = test_instance.a_property()

            # Assert the correct result is returned both times
            self.assertEqual(first_call, 42)
            self.assertEqual(second_call, 42)

            # Ensure a_method is called only once
            mock_method.assert_called_once()

if __name__ == "__main__":
    unittest.main()
