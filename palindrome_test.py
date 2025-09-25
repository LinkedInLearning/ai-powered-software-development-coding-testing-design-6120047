import unittest
from palindrome import is_palindrome

class TestPalindrome(unittest.TestCase):
  def test_simple_palindrome(self):
    self.assertTrue(is_palindrome("madam"))
    self.assertTrue(is_palindrome("racecar"))
    self.assertTrue(is_palindrome("level"))
    self.assertTrue(is_palindrome("deified"))
    self.assertTrue(is_palindrome("civic"))
    self.assertFalse(is_palindrome("python"))
    self.assertFalse(is_palindrome("hello"))

if __name__ == "__main__":
  unittest.main()