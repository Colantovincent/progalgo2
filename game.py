import random

class Game:
    def __init__(self, width:int, heigth:int) -> None:
        self._width = width
        self._height = heigth
        self._cv : tuple[int,int] = (random.randint(1,width),random.randint(1,heigth)) #ricorda di cambiare
        self._completed : bool = False
        self._table : list[list[int]] = [[0] * width for _ in range (heigth)]
       
        

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
    

        