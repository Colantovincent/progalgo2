import random
from table import _Table
class Game:
    def __init__(self, width:int, heigth:int) -> None:
        self._width = width
        self._height = heigth
        t = _Table(self)
        self._completed : bool = False
        self._table : list[list[int]] = t.tabellone
        self._cv : tuple[int,int] = t.cv 
        

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height

    @property
    def completed(self):
        return self._completed

    @property
    def table(self):
        return self._table

    @property
    def cv(self):
        return self._cv

    def move(self, row:int, column:int) -> None:
        if self.completed or (row, column) != self.cv or (self.cv[0] != row and self.cv[1] != column):
            return
        tmp : list[int] = []
        if row == self.cv[0]:
            tmp  , scelta= (self.table[row][self.cv[1]+1 : column], True) if column > self.cv[1] else (self.table[row][column : self.cv[1] - 1],False)
            if scelta:
                for i in range(abs(row-self.cv[0])):
                    self.table[row][self.cv[1]+i] = tmp[i]
                self.table[row][column] = 0
            else:
                for i in range(abs(row-self.cv[0])):
                    self.table[row][self.cv[1]-i] = tmp[i]
                self.table[row][column] = 0
        else:
            tmp, scelta = (
            ([self.table[i][column] for i in range(self.cv[0] + 1, row + 1)], True)
            if row > self.cv[0]
            else ([self.table[i][column] for i in range(row, self.cv[0])], False)
            )
            if scelta:
                for i in range(abs(column-self.cv[1])):
                    self.table[self.cv[0]+i][column] = tmp[i]
                self.table[row][column] = 0
            else:
                for i in range(abs(column-self.cv[1])):
                    self.table[self.cv[0]-i][column] = tmp[i]
                self.table[row][column] = 0
        return    

        