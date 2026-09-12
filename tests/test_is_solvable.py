from game import Game
from table import _Table #type: ignore
#N.B. La test suite aveva per forza bisogno di accedere a _Table quindi mi tocca fare type ignore :/

def from_config(c: list[list[int]]) -> _Table:
    n, m = len(c), len(c[0])
    game = Game(m, n)
    tab = _Table(game)
    for i in range(n):
        for j in range(m):
            tab.set_box(i, j, c[i][j])
    return tab

def test_even_solvable():
    config = [
        [1,  2,  3,  4],
        [5,  6,  7,  8],
        [9,  10, 11, 12],
        [13, 14, 15, 0]
    ]
    t = from_config(config)
    assert t.is_solvable()



def test_odd_solvable():
    config = [
        [1,  2,  3],
        [4,  5,  6],
        [7,  8,  9],
        [10, 11, 0]
    ]
    t = from_config(config)
    assert t.is_solvable()


def test_even_unsolvable():
    config = [
        [1,  2,  3,  4],
        [5,  6,  7,  8],
        [9,  10, 11, 12],
        [13, 15, 14, 0]
    ]
    t = from_config(config)
    assert not t.is_solvable()


def test_odd_unsolvable():
    config = [
        [1,  2,  3],
        [4,  5,  6],
        [7,  8,  9],
        [11, 10, 0]
    ]
    t = from_config(config)
    assert not t.is_solvable()

def test_odd_scrambled_solvable():
    config = [
        [2, 4, 5],
        [1, 8, 0],
        [6, 7, 3]
    ]
    t = from_config(config)
    assert t.is_solvable()

def test_odd_scrambled_unsolvable():
    config = [
        [2, 7, 8],
        [1, 4, 5],
        [0, 3, 6]
    ]
    t = from_config(config)
    assert not t.is_solvable()

def test_even_scrambled_solvable():
    config = [
        [11, 12, 6, 10],
        [14, 4, 7, 8],
        [3, 13, 1, 2],
        [5, 15, 9, 0]
    ]
    t = from_config(config)
    assert t.is_solvable()

def test_even_scrambled_unsolvable():
    config = [
        [1, 9, 7, 6],
        [5, 11, 13, 4],
        [10, 14, 2, 8],
        [12, 3, 0, 15]
    ]
    t = from_config(config)
    assert not t.is_solvable()