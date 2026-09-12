from __future__ import annotations
from typing import TYPE_CHECKING
from helper import Helper
from copy import deepcopy
import random
import math

if TYPE_CHECKING:
    from game import Game

class OutOfBoundsError(IndexError):
    def __init__(self, riga: int, colonna: int) -> None:
        self.riga = riga
        self.colonna = colonna
        msg = f"Posizione invalida: ({riga}, {colonna}) fuori dai limiti"
        super().__init__(msg)

class _Table:
    def __init__(self, g: Game):
        self._partita = g
        self._tabellone: list[list[int]] = [[0] * g.width for _ in range(g.height)]
        self._cifre = math.floor(math.log10(g.width * g.height)) + 1 #assumiamo non si voglia istanziare una matrice 0x0
        self._cv: tuple[int, int] = (random.randint(0, g.height - 1), random.randint(0, g.width - 1))
        self._mossa: tuple[int, int] = (-1, -1)

    @property
    def cv(self) -> tuple[int, int]:
        return self._cv

    @property
    def tabellone(self) -> list[list[int]]:
        return self._tabellone

    @tabellone.setter
    def tabellone(self, v: list[list[int]]) -> None:
        self._tabellone = deepcopy(v)

    @property
    def mossa(self) -> tuple[int, int]:
        return self._mossa

    @mossa.setter
    def mossa(self, v: tuple[int, int]) -> None:
        self._mossa = v

    @classmethod
    def copy_table(cls, t: _Table) -> _Table:
        copia = _Table(t._partita)
        for i in range(t._partita.height):
            for j in range(t._partita.width):
                copia.set_box(i, j, t.get_box(i, j))
        return copia


    def set_box(self, row: int, column: int, value: int) -> None:
        if not (0 <= row < self._partita.height and 0 <= column < self._partita.width):
            raise OutOfBoundsError(row, column)

        upper_bound = self._partita.width * self._partita.height - 1
        if not (0 <= value <= upper_bound):
            raise ValueError(f"{value} deve essere compreso tra 0 e {upper_bound}")

        self._tabellone[row][column] = value
        if value == 0:
            self._cv = (row, column)


    def get_box(self, row: int, column: int) -> int:
        if not (0 <= row < self._partita.height and 0 <= column < self._partita.width):
            raise OutOfBoundsError(row, column)

        return self._tabellone[row][column]


    def is_solvable(self) -> bool:
        if self._partita.width % 2 == 0:
            return (Helper.inv(self._tabellone) + Helper.ind(self._partita.height, self.cv[0])) % 2 == 1

        return Helper.inv(self._tabellone) % 2 == 0


    def __str__(self) -> str:
        tmp = ""

        for row in self.tabellone:
            for el in row:
                tmp = tmp + f" {el:{self._cifre}}"
            tmp = tmp + "\n"

        return tmp
