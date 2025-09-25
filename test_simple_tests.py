import pytest
from simple_tests import is_palindrome

@pytest.mark.parametrize("input_str,expected", [
  ("Racecar", True),
  ("racecar", True),
  ("Race car", True),
  ("Hello", False),
  ("", True),
  ("A", True),
  ("No lemon no melon", True),
  ("Was it a car or a cat I saw", False),  # spaces removed, but not punctuation
  ("12321", True),
  ("12345", False),
])
def test_is_palindrome(input_str, expected):
  assert is_palindrome(input_str) == expected