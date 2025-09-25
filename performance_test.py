import pytest
from performance import has_duplicates
import time

@pytest.mark.parametrize("items,expected", [
    ([1, 2, 3, 4, 5], False),
    ([1, 2, 3, 2, 5], True),
    ([], False),
    ([42], False),
    ([7, 7, 7, 7], True),
    ([1, 2, 3, 4, 5, 1], True),
    ([0, -1, -2, -3, -1], True),
    ([1000000, 999999, 888888], False),
])
def test_has_duplicates_basic(items, expected):
    assert has_duplicates(items) == expected

def test_has_duplicates_large_list_performance():
    large_list = list(range(10000)) + [9999]  # One duplicate at the end
    start = time.time()
    result = has_duplicates(large_list)
    duration = time.time() - start
    assert result is True
    assert duration < 2  # Should finish within 2 seconds