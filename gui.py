from __future__ import annotations
import sys
from abc import ABC, abstractmethod
from typing import Final
from ezgraphics import GraphicsWindow
from game import Game


class EventHandler(ABC):
    def __init__(self, g: Game, gui: Gui):
        self._g = g
        self._gui = gui

    @property
    def g(self) -> Game:
        return self._g

    @property
    def gui(self) -> Gui:
        return self._gui

    @property
    @abstractmethod
    def modifier_mask(self) -> int:
        """Maschera di bit specifica per il tasto modificatore (Ctrl/Cmd) in base all'OS. PERCHE QUALCUNO USA MACOS E ME LO HA ROTTO""" # docstring by Vincent
        pass

    def onKeyPress(self, win, e):
        if e.state & self.modifier_mask:
            key = e.keysym.lower()
            if key == "z":
                self.g.undo()
                self.gui.scrivi()
            elif key == "y":
                self.g.redo()
                self.gui.scrivi()

    def onMouseDown(self, win, e):
        if e.button != 1:
            return

        col = (e.x - self.gui.PADDING) // self.gui.CELL_SIZE
        row = (e.y - self.gui.PADDING) // self.gui.CELL_SIZE

        if 0 <= row < self.g.height and 0 <= col < self.g.width:
            self.g.move(row, col)
            self.gui.scrivi()
            print(self.g)

    @staticmethod
    def create(g: Game, gui: Gui) -> EventHandler:
        if sys.platform == "darwin":
            return MacEventHandler(g, gui)
        return WindowsLinuxEventHandler(g, gui)


class WindowsLinuxEventHandler(EventHandler):
    @property
    def modifier_mask(self) -> int:
        return 4  # Tasto Ctrl su Windows e Linux


class MacEventHandler(EventHandler):
    @property
    def modifier_mask(self) -> int:
        return 8  # Tasto Command (Mod1) su macOS


class Gui:
    #Costanti per lo stile
    CELL_SIZE: Final[int] = 50
    PADDING: Final[int] = 100
    BORDER_COLOR: Final[str] = "royalblue"
    BORDER_WIDTH: Final[int] = 2
    OUTER_BORDER_COLOR: Final[str] = "navy"
    OUTER_BORDER_WIDTH: Final[int] = 4
    TEXT_COLOR: Final[str] = "black"
    FONT_FAMILY: Final[str] = "helvetica"
    FONT_SIZE: Final[int] = 14

    def __init__(self, g: Game, start_loop: bool = True) -> None:
        self._g = g

        self._win = GraphicsWindow(self.win_width, self.win_height)
        self._win.setTitle("Gioco del 15")
        self._canvas = self._win.canvas()

        self.disegna_tabellone()
        self.scrivi()
        self._handler = EventHandler.create(self.g, self)

        self.win.enableEvents("KeyPress", "MouseDown")
        self.win.setEventHandler(self._handler)

        if start_loop:
            self.win.wait()

    @property
    def g(self) -> Game:
        return self._g

    @property
    def win(self) -> GraphicsWindow:
        return self._win

    @property
    def canvas(self):
        return self._canvas

    @property
    def win_width(self) -> int:
        return self.g.width * self.CELL_SIZE + 2 * self.PADDING

    @property
    def win_height(self) -> int:
        return self.g.height * self.CELL_SIZE + 2 * self.PADDING

    def disegna_tabellone(self) -> None:
        # Bordo esterno del tabellone di gioco
        self.canvas.setLineWidth(self.OUTER_BORDER_WIDTH)
        self.canvas.setOutline(self.OUTER_BORDER_COLOR)
        self.canvas.setFill()
        self.canvas.drawRect(
            self.PADDING,
            self.PADDING,
            self.g.width * self.CELL_SIZE,
            self.g.height * self.CELL_SIZE,
        )

        self.canvas.setLineWidth(self.BORDER_WIDTH)
        self.canvas.setOutline(self.BORDER_COLOR)
        self.canvas.setFill()
        for i in range(self.g.height):
            for j in range(self.g.width):
                x = self.PADDING + j * self.CELL_SIZE
                y = self.PADDING + i * self.CELL_SIZE
                self.canvas.drawRect(x, y, self.CELL_SIZE, self.CELL_SIZE)

    def scrivi(self) -> None:
        for el in self.canvas.items():
            if self.canvas.itemType(el) == "text":
                self.canvas.removeItem(el)

        self.canvas.setTextAnchor("center")
        self.canvas.setTextFont(self.FONT_FAMILY, "bold", self.FONT_SIZE)
        self.canvas.setOutline(self.TEXT_COLOR)

        for i in range(len(self.g.table)):
            for j in range(len(self.g.table[0])):
                val = self.g.table[i][j]
                if val != 0:
                    center_x = self.PADDING + j * self.CELL_SIZE + self.CELL_SIZE // 2
                    center_y = self.PADDING + i * self.CELL_SIZE + self.CELL_SIZE // 2
                    self.canvas.drawText(center_x, center_y, str(val))
        self.canvas.drawText(self.win_width // 2, self.PADDING // 2, f"Mosse: {self.g.mosse}")


if __name__ == "__main__":
    gui = Gui(Game(5, 5))