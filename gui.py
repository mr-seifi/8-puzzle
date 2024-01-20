import tkinter as tk
import time
from tkinter.ttk import Style
from game import BOARD_SIZE

class PuzzleGame:
    def __init__(self, initial_state):
        self.root = tk.Tk()
        self.tiles = []
        self.state_history = initial_state

        for row in range(BOARD_SIZE):
            row_tiles = []
            for col in range(BOARD_SIZE):
                tile = tk.Button(self.root, width=10, height=5)
                tile.grid(row=row, column=col)
                row_tiles.append(tile)
            self.tiles.append(row_tiles)

        style = Style()

        style.configure('TButton', font =
                    ('calibri', 20, 'bold'),
                            borderwidth = '4')

    def animate_solver(self, next_state):
        self.update_tiles(next_state)
        self.root.update()
        time.sleep(0.5)
        self.state_history.append(next_state)

    def update_tiles(self, state):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                value = state[row][col]
                if value != 0:
                    self.tiles[row][col].config(text=str(value))
                else:
                    self.tiles[row][col].config(text="")

    def start(self):
        self.root.mainloop()