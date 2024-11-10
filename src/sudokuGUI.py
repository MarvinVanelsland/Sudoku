from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM
from grid import Grid

MARGIN = 20
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9 

class SudokuGUI(Frame):

    def __init__(self, parent, game):
        self.game = game
        Frame.__init__(self, parent)
        self.parent = parent
        self.row, self.col = -1, -1
        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,
                             width=WIDTH,
                             height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        clear_button = Button(self,
                              text="Clear answers",
                              command=self.__clear_answers)
        clear_button.pack(fill=BOTH, side=BOTTOM)

        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __draw_grid(self):
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")  # Effacer les anciens chiffres
        for i in range(9):
            for j in range(9):
                answer = self.game.cases[i*9+j].value  # Récupérer la valeur de la case
                
                # Si la case a une valeur, la dessiner
                if answer is not None:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    # Vérifier si la case est initiale (partie du puzzle) ou modifiable
                    if self.game.puzzle[i*9+j] != '.':  # Case initiale
                        color = 'black'
                    else:
                        # Vérifier si la valeur entrée est correcte
                        if self.game.cases[i*9+j].valid:
                            color = "green"  # Bonne valeur (valid)
                        else:
                            color = "red"  # Mauvaise valeur (invalid)
    
                    # Afficher le texte (chiffre) sur la case
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=color
                    )


    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )

    def __draw_victory(self):
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="victory", fill="dark orange", outline="orange"
        )
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(
            x, y,
            text="You win!", tags="victory",
            fill="white", font=("Arial", 32)
        )

    def __cell_clicked(self, event):
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE

            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.puzzle[row*9+col] == '.':
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__draw_cursor()

    def __key_pressed(self, event):
        if event.keysym == 'BackSpace':  # Annuler la dernière action
            self.game.undo()
            self.__draw_puzzle()
            self.__draw_cursor()

        # Vérifier si une cellule est sélectionnée
        if self.row >= 0 and self.col >= 0:
            # Vérifier si la touche est un chiffre entre 1 et 9
            if event.keysym in ['KP_1', 'KP_2', 'KP_3', 'KP_4', 'KP_5', 'KP_6', 'KP_7', 'KP_8', 'KP_9']:
                value = int(event.char)  # Convertir le caractère en entier
                # Vérifier si la case est modifiable (elle ne doit pas être protégée)
                if self.game.puzzle[self.row * 9 + self.col] == '.':
                    self.game.setValue(self.row * 9 + self.col, value)  # Mettre la valeur dans la grille
                    self.__draw_puzzle()  # Redessiner le puzzle avec la nouvelle valeur
                    self.__draw_cursor()  # Redessiner le curseur

                    # Vérifier si le joueur a gagné
                    if self.game.checkWin():
                        self.__draw_victory()  # Afficher la victoire

    def __clear_answers(self):
        self.game = Grid(self.game.puzzle)
        self.__draw_puzzle()
        
if __name__ == '__main__':
    
    game = Grid.loadFromFile(2)

    root = Tk()
    SudokuGUI(root, game)
    root.geometry(f"{WIDTH}x{HEIGHT+40}")
    root.mainloop()
