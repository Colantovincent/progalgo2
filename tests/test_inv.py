from helper import Helper

def test_swapped():
    c = [
        [1, 3, 2, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]
    assert Helper.inv(c) == 1

def test_multiple_lesser():
    c = [
        [1, 4, 3, 2],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]
    assert Helper.inv(c) == 3