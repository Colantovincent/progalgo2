from __future__ import annotations
from game import Game
from helper import Helper

class OutOfBoundsError(IndexError):
    def __init__(self, riga: int, colonna: int) -> None:
        self.riga = riga
        self.colonna = colonna
        msg = f"Posizione invalida: ({riga}, {colonna}) fuori dai limiti"
        super().__init__(msg)

class _Table:
    def __init__(self, g: Game):
        self._partita = g
        self._tabellone: list[list[int]] = [[0 for __ in range(g.width)] for _ in range(g.height)]

    @classmethod
    def copy_table(cls, t: _Table) -> _Table:
        copia = _Table(t._partita)
        copia._tabellone = [[t._tabellone[i][j] for j in range(t._partita.width)] for i in range(t._partita.height)]
        return copia

    def set_box(self, row: int, column: int, value: int) -> None:
        if not (0 <= row < self._partita.height and 0 <= column < self._partita.width):
            raise OutOfBoundsError(row, column)

        upper_bound = self._partita.width * self._partita.height - 1
        if not (0 <= value < upper_bound):
            raise ValueError(f"{value} deve essere compreso tra 0 e {upper_bound}")

        self._tabellone[row][column] = value


    def get_box(self, row: int, column: int) -> int:
        if not (0 <= row < self._partita.height and 0 <= column < self._partita.width):
            raise OutOfBoundsError(row, column)

        return self._tabellone[row][column]


    def is_solvable(self) -> bool:
        if self._partita.width % 2 == 0:
            return bool((Helper.inv(self._tabellone) + Helper.ind(self._tabellone)) % 2)

        return bool(Helper.inv(self._tabellone) % 2)