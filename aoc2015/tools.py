def range_inclusive(start, end):
    """
    >>> range_inclusive(2, 5)
    [2, 3, 4, 5]
    >>> range_inclusive(5, 2)
    [5, 4, 3, 2]
    """
    if start > end:
        return list(range(start, end - 1, -1))
    else:
        return list(range(start, end + 1))
