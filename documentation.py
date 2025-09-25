def f(a, b):
    """
    Extracts the last `b` digits from integer `a` and returns them as a list in original order.

    Args:
        a (int): The integer from which digits are extracted.
        b (int): The number of digits to extract from the end of `a`.

    Returns:
        list: A list of the extracted digits in the order they appear in `a`.
    """
    r = []
    while b:
        r.append(a % 10)
        a //= 10
        b -= 1
    return r[::-1]

print(f(987654, 3))