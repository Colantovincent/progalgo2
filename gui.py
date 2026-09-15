from __future__ import annotations
from ezgraphics import GraphicsWindow
from game import Game
class EventHandler:
    def __init__(self, g: Game, gui: Gui):
        self._g = g
        self._gui = gui

    @property
    def g(self) -> Game:
        return self._g

    @property
    def gui(self) -> Gui:
        return self._gui

    def onKeyPress(self, win, e):
        if e.state == 4:
            key = e.keysym.lower()
            if key == "z":
                self.g.undo()
                self.gui.scrivi
            elif key == "y":
                self.g.redo()
                self.gui.scrivi

    def onMouseDown(self, win, e):
        if e.button != 1:
            return

        i = round(e.x / 40 - 1)
        j = round(e.y / 40 - 1)
        self.g.move(i, j)
        self.gui.scrivi
        print(self.g)


class Gui:
    def __init__(self, g : Game) -> None:
        self._win= GraphicsWindow(g.width * 40, g.height * 40)
        self._canvas = self._win.canvas()
        self._g = g
        for i in range(g.height):
            for j in range(g.width):
                self.canvas.drawRect(i*40,j*40,40,40)
        self.scrivi
        self._handler = EventHandler(self.g, self)

        self.win.enableEvents("KeyPress", "MouseDown")
        self.win.setEventHandler(self._handler)

        self.win.wait()


    @property
    def g(self):
        return self._g

    @property
    def win(self):
        return self._win

    @property
    def canvas(self):
        return self._canvas

    @property
    def scrivi(self):
        for el in self.canvas.items():
            if self.canvas.itemType(el) == "text":
                self.canvas.removeItem(el)

        for i in range(len(self.g.table)):
            for j in range(len(self.g.table[0])):
                if self.g.table[i][j] != 0:
                    self.canvas.drawText((i+1)*40-20,(j+1)*40-20,self.g.table[i][j])


gui= Gui(Game(5,5))