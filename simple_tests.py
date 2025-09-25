def is_palindrome(s: str) -> bool:
    s = s.lower().replace(" ", "")
    return s == s[::-1]

print(is_palindrome("Racecar"))  # True
print(is_palindrome("Hello"))    # False