from helper import Helper

def test_ordered():
    c = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    assert Helper.inv(c) == 0

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

def test_zero_out_of_place():
    c = [
        [1, 0, 3],
        [4, 2, 6],
        [7, 5, 8]
    ]
    assert Helper.inv(c) == 4

def test_m_diff_n():
    c = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 0],
    ]
    assert Helper.inv(c) == 0

def test_max_inv():
    c = [
        [15, 14, 13, 12],
        [11, 10, 9, 8],
        [7, 6, 5, 4],
        [3, 2, 1, 0]
    ]
    N = len(c)*len(c[0])
    assert Helper.inv(c) == ((N - 1) * (N - 2)) // 2


#ind(c)
def test_ind_last_row():
    assert Helper.ind(3, 2) == 1
    assert Helper.ind(4, 3) == 1
    assert Helper.ind(5, 4) == 1

def test_ind_first_row():
    """Obiettivo: Helper.ind(n, 0) restituisca n"""
    assert Helper.ind(3, 0) == 3
    assert Helper.ind(4, 0) == 4
    assert Helper.ind(5, 0) == 5

def test_ind_middle_row():
    assert Helper.ind(4, 2) == 2
    assert Helper.ind(4, 1) == 3
    assert Helper.ind(5, 2) == 3

def test_ind_minimal_row():
    assert Helper.ind(1, 0) == 1


# _flatten(c)
def test_flatten_odd():
    c = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    assert Helper._flatten(c) == [1, 2, 3, 4, 5, 6, 7, 8, 0]

def test_flatten_even():
    c = [
        [1,  2,  3,  4],
        [5,  6,  7,  8],
        [9,  10, 11, 12],
        [13, 14, 15, 0]
    ]
    assert Helper._flatten(c) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]