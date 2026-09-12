from table  import _Table
import copy

class Game:
    def __init__(self, width:int, heigth:int) -> None:
        self._width = width
        self._height = heigth
        t = _Table(self)
        self._completed : bool = False
        self._table : list[list[int]] = t.tabellone
        self._cv : tuple[int,int] = t.cv 
        self._history : list[_Table] = []
        self._indice : int = 0
        

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

    @table.setter
    def table(self, new : list[list[int]]):
        self._table = new
        return

    @property
    def cv(self):
        return self._cv

    @cv.setter
    def cv(self, new : tuple[int,int]):
        self._cv = new
        return

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, new : list[_Table]):
        self._history = new
        return 

    @property
    def indice(self):
        return self._indice

    @indice.setter
    def indice(self, new : int):
        self._indice = new
        return

    def move(self, row:int, column:int) -> None:
        if self.completed or (row, column) == self.cv or (self.cv[0] != row and self.cv[1] != column):
            return
        if self.indice < len(self.history)-1 :
            self.history = self.history[:self.indice+1]
        tmp : list[int] = []
        if row == self.cv[0]:
            tmp  , scelta= (self.table[row][self.cv[1] + 1 : column + 1], True) if column > self.cv[1] else (self.table[row][column : self.cv[1]],False)
            if scelta:
                for i in range(abs(column-self.cv[1])):
                    self.table[row][self.cv[1]+i] = tmp[i]
                self.table[row][column] = 0
            else:
                for i in range(abs(column-self.cv[1])):
                    self.table[row][self.cv[1]-i] = tmp[-1-i]
                self.table[row][column] = 0
        else:
            tmp, scelta = (
            ([self.table[i][column] for i in range(self.cv[0] + 1, row + 1)], True)
            if row > self.cv[0]
            else ([self.table[i][column] for i in range(row, self.cv[0])], False)
            )
            if scelta:
                for i in range(abs(row-self.cv[0])):
                    self.table[self.cv[0]+i][column] = tmp[i]
                self.table[row][column] = 0
            else:
                for i in range(abs(row-self.cv[0])):
                    self.table[self.cv[0]-i][column] = tmp[-1-i]
                self.table[row][column] = 0
        new : _Table = _Table(self)
        new.tabellone = copy.deepcopy(self.table)
        self.history.append(new)
        self.indice = len(self.history) - 1
        new.mossa,self.cv= (row,column),(row,column)

        return  

    def undo(self) -> None:
        if self.indice >0:
            self.indice -= 1
            self.table = _Table.copy_table(self.history[self.indice]).tabellone
            self.cv = self.history[self.indice].cv
        return

    def redo(self) -> None:
        if self.indice < len(self.history)-1:
            self.indice +=1 
            self.table = _Table.copy_table(self.history[self.indice]).tabellone
            self.cv = self.history[self.indice].cv
        return
         
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