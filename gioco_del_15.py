from __future__ import annotations
from copy import deepcopy
import random
import math

class OutOfBoundsError(IndexError):
    def __init__(self, riga: int, colonna: int) -> None:
        self.riga = riga
        self.colonna = colonna
        msg = f"Posizione invalida: ({riga}, {colonna}) fuori dai limiti"
        super().__init__(msg)

class Helper:
    @classmethod
    def inv(cls, c: list[list[int]]) -> int:
        conta = 0
        v = cls._flatten(c)
        for i in range(len(v)):
            el = v[i]
            if el == 0:
                continue

            for j in range(i - 1, -1, -1):
                if el < v[j]:
                    conta += 1
        return conta

    @classmethod
    def ind(cls, n: int, i: int) -> int:
        return n - i

    @classmethod
    def _flatten(cls, c: list[list[int]]) -> list[int]:
        linearizzata: list[int] = []
        for riga in c:
            for el in riga:
                linearizzata.append(el)
        return linearizzata

class _Table:
    def __init__(self, g: Game):
        self._partita = g
        self._tabellone: list[list[int]] = [[0] * g.width for _ in range(g.height)]
        self._cifre = math.floor(math.log10(g.width * g.height)) + 1 #assumiamo non si voglia istanziare una matrice 0x0
        self._cv: tuple[int, int] = (random.randint(0, g.height - 1), random.randint(0, g.width - 1))
        self._mossa: tuple[int, int] = (-1, -1)
        self.randomize()

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


    def randomize(self) -> None:
        solvable = False
        while not solvable:
            tmp = [i for i in range(self._partita.width * self._partita.height)]
            random.shuffle(tmp)
            k = 0
            for i in range(self._partita.height):
                for j in range(self._partita.width):
                    self.set_box(i, j, tmp[k])
                    k += 1
            solvable = self.is_solvable()


    def __str__(self) -> str:
        tmp = ""

        for row in self.tabellone:
            for el in row:
                tmp = tmp + f" {el:{self._cifre}}"
            tmp = tmp + "\n"

        return tmp

class Game:
    def __init__(self, width:int, height:int) -> None:
        self._width = width
        self._height = height
        self._t = _Table(self)
        self._completed : bool = False
        self._table : list[list[int]] = self.t.tabellone
        self._cv : tuple[int,int] = self.t.cv 
        self._history : list[_Table] = [self.t]
        self._indice : int = 0
        self._mosse : int = 0

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height

    @property
    def t(self):
        return self._t

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, new : bool):
        self._completed = new

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, new : list[list[int]]):
        self._table = new

    @property
    def cv(self):
        return self._cv

    @cv.setter
    def cv(self, new : tuple[int,int]):
        self._cv = new

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, new : list[_Table]):
        self._history = new

    @property
    def indice(self):
        return self._indice

    @indice.setter
    def indice(self, new : int):
        self._indice = new

    @property
    def mosse(self):
        return self._mosse

    @mosse.setter
    def mosse(self, new : int):
        self._mosse = new

    def move(self, row:int, column:int) -> None:
        if self.completed or (row, column) == self.cv or (self.cv[0] != row and self.cv[1] != column):
            return
        
        if self.indice < len(self.history)-1 :
            self.history = self.history[:self.indice+1]
        tmp : list[int] = []

        if row == self.cv[0]:

            if column > self.cv[1]:
                tmp  , scelta= self.table[row][self.cv[1] + 1 : column + 1], True
            else:
                tmp,scelta =(self.table[row][column : self.cv[1]],False)
            if scelta:
                for i in range(abs(column-self.cv[1])):
                    self.table[row][self.cv[1]+i] = tmp[i]
                self.table[row][column] = 0
            else:
                for i in range(abs(column-self.cv[1])):
                    self.table[row][self.cv[1]-i] = tmp[-1-i]
                self.table[row][column] = 0
        else:

            if row > self.cv[0]:
                tmp, scelta =  [self.table[i][column] for i in range(self.cv[0] + 1, row + 1)], True
            else: 
                tmp,scelta = [self.table[i][column] for i in range(row, self.cv[0])], False
            
            if scelta:
                for i in range(abs(row-self.cv[0])):
                    self.table[self.cv[0]+i][column] = tmp[i]
                self.table[row][column] = 0
            else:
                for i in range(abs(row-self.cv[0])):
                    self.table[self.cv[0]-i][column] = tmp[-1-i]
                self.table[row][column] = 0
                
        self.t.tabellone = self.table
        new  : _Table = _Table.copy_table(self.t)
        self.history.append(new)
        self.indice = len(self.history) - 1
        new.mossa,self.cv= (row,column),(row,column)
        self.mosse += 1
        self.completed = self.completato()

    def undo(self) -> None:
        if self.indice >0:
            self.indice -= 1
            self.table = _Table.copy_table(self.history[self.indice]).tabellone
            self.cv = self.history[self.indice].cv
            self.mosse += 1
            self.completed = self.completato()

    def redo(self) -> None:
        if self.indice < len(self.history)-1:
            self.indice +=1 
            self.table = _Table.copy_table(self.history[self.indice]).tabellone
            self.cv = self.history[self.indice].cv
            self.mosse += 1
            self.completed = self.completato()
         
    def __str__(self) -> str:
        risultato : list[str] = []
        for i in range(self.indice + 1): 
            tabellone_corrente : _Table = self.history[i]
            if i == 0:
                risultato.append(f"Tabellone iniziale:\n{str(tabellone_corrente)}")
            else:
                riga, colonna = tabellone_corrente.mossa
                risultato.append(f"Tabellone a seguito della mossa di riga {riga} e colonna {colonna}:\n{str(tabellone_corrente)}")
        
        return "\n\n".join(risultato)

    def completato(self) -> bool:
        if self.table[self.height - 1][self.width - 1] != 0:
            return False
        atteso = 1
        for i in range(self.height):
            for j in range(self.width):
                if i == self.height - 1 and j == self.width - 1:
                    return True
                if self.table[i][j] != atteso:
                    return False
                atteso += 1
        return True