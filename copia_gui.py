from __future__ import annotations
from ezgraphics import GraphicsWindow
from game import Game

# Costanti di stile e layout
CELL_SIZE = 50               # Dimensione in pixel di ciascuna cella
PADDING = 100                # Spazio (margine) tra il tabellone e il bordo della finestra
BORDER_COLOR = "royalblue"   # Colore dei bordi delle celle
BORDER_WIDTH = 2             # Spessore dei bordi delle celle
OUTER_BORDER_COLOR = "navy"  # Colore del bordo esterno del tabellone
OUTER_BORDER_WIDTH = 4       # Spessore del bordo esterno
TEXT_COLOR = "black"         # Colore dei numeri
FONT_FAMILY = "helvetica"    # Font per i numeri
FONT_SIZE = 14               # Dimensione del font


class EventHandler:
    def __init__(self, g: Game, gui: Gui):
        self._g = g
        self._gui = gui
        self._lunghezza = self.g.width * self.gui.cell_size + 2 * self.gui.padding

    @property
    def g(self) -> Game:
        return self._g

    @property
    def gui(self) -> Gui:
        return self._gui

    @property
    def lunghezza(self):
        return self._lunghezza

    def onKeyPress(self, win, e):
        if (e.state & 4) or (e.state & 8) or e.state == 4:
            key = e.keysym.lower()
            if key == "z":
                self.g.undo()
                self.gui.scrivi(self.lunghezza)
            elif key == "y":
                self.g.redo()
                self.gui.scrivi(self.lunghezza)

    def onMouseDown(self, win, e):
        if e.button != 1:
            return

        col = (e.x - self.gui.padding) // self.gui.cell_size
        row = (e.y - self.gui.padding) // self.gui.cell_size

        if 0 <= row < self.g.height and 0 <= col < self.g.width:
            self.g.move(row, col)
            self.gui.scrivi(self.g.width * self.gui.cell_size + 2 * self.gui.padding)
            print(self.g)


class Gui:
    def __init__(
        self,
        g: Game,
        cell_size: int = CELL_SIZE,
        padding: int = PADDING,
        border_color: str = BORDER_COLOR,
        border_width: int = BORDER_WIDTH,
        outer_border_color: str = OUTER_BORDER_COLOR,
        outer_border_width: int = OUTER_BORDER_WIDTH,
        text_color: str = TEXT_COLOR,
        font_size: int = FONT_SIZE,
        start_loop: bool = True
    ) -> None:
        self._g = g
        self._cell_size = cell_size
        self._padding = padding
        self._border_color = border_color
        self._border_width = border_width
        self._outer_border_color = outer_border_color
        self._outer_border_width = outer_border_width
        self._text_color = text_color
        self._font_size = font_size

        win_width = g.width * self.cell_size + 2 * self.padding
        win_height = g.height * self.cell_size + 2 * self.padding

        self._win = GraphicsWindow(win_width, win_height)
        self._win.setTitle("Gioco del 15")
        self._canvas = self._win.canvas()

        self.disegna_tabellone()
        self.scrivi(win_width)
        self._handler = EventHandler(self.g, self)

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
    def cell_size(self) -> int:
        return self._cell_size

    @property
    def padding(self) -> int:
        return self._padding

    def disegna_tabellone(self) -> None:
        # Bordo esterno del tabellone di gioco
        self.canvas.setLineWidth(self._outer_border_width)
        self.canvas.setOutline(self._outer_border_color)
        self.canvas.setFill()
        self.canvas.drawRect(
            self.padding,
            self.padding,
            self.g.width * self.cell_size,
            self.g.height * self.cell_size,
        )

        self.canvas.setLineWidth(self._border_width)
        self.canvas.setOutline(self._border_color)
        self.canvas.setFill()
        for i in range(self.g.height):
            for j in range(self.g.width):
                x = self.padding + j * self.cell_size
                y = self.padding + i * self.cell_size
                self.canvas.drawRect(x, y, self.cell_size, self.cell_size)


    def scrivi(self, lunghezza : int):
        for el in self.canvas.items():
            if self.canvas.itemType(el) == "text":
                self.canvas.removeItem(el)

        self.canvas.setTextAnchor("center")
        self.canvas.setTextFont(FONT_FAMILY, "bold", self._font_size)
        self.canvas.setOutline(self._text_color)

        for i in range(len(self.g.table)):
            for j in range(len(self.g.table[0])):
                val = self.g.table[i][j]
                if val != 0:
                    center_x = self.padding + j * self.cell_size + self.cell_size // 2
                    center_y = self.padding + i * self.cell_size + self.cell_size // 2
                    self.canvas.drawText(center_x, center_y, str(val))
        self.canvas.drawText(lunghezza // 2, self.padding // 2, f"Mosse: {self.g.mosse}")



gui = Gui(Game(5, 5))