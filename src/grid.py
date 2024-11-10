from case import Case
from stack import Stack

class Grid:
    
    def __init__(self, puzzle=81 * '.'):
        """
        Constructeur par défaut
        :param puzzle: chaîne de 81 caractères représentant la grille (par défaut, une grille vide)
        """
        self.puzzle = puzzle
        self.full = self.puzzle.count('.') == 0
        self.initCases()
        self.puzzleNow = self.casesToString()
        self.stack = Stack()

    @staticmethod
    def loadFromFile(num):
        """
        Charger un puzzle depuis le fichier `grids.sud`
        :param num: numéro du puzzle à charger
        """
        with open("./data/grids.sud", 'r') as f:
            buff = f.readlines()
        return Grid(buff[num][:-1])

    def initCases(self):
        """
        Initialise une liste de 81 cases avec leur valeur suivant le puzzle.
        """
        self.cases = []
        for i in range(81):
            if self.puzzle[i] == '.':
                self.cases.append(Case(i))
            else:
                self.cases.append(Case(i, int(self.puzzle[i])))

    def casesToString(self):
        """
        Retourne une chaîne de caractères représentant le Sudoku.
        """
        return ''.join(str(c.value) if c.value is not None else '.' for c in self.cases)

    def setValue(self, position, value):
        """
        Méthode permettant de modifier la valeur d'une case à une position donnée.
        """
        if self.puzzle[position] == '.':  # Seules les cases vides peuvent être modifiées
            self.stack.push((position, self.cases[position].value, value))
            self.cases[position].setValue(value)
            self.puzzleNow = self.casesToString()
            self.cases[position].valid = True  # Réinitialiser la validité de la case
            self.verif(position)

    def undo(self):
        """
        Méthode permettant d'annuler les coups (empilement inverse).
        """
        if not self.stack.empty():
            old = self.stack.pop()
            self.setValue(old[0], old[1])

    def verifLine(self, position):
        """
        Vérifie la validité de la ligne après une modification.
        """
        case = self.cases[position]
        listCases = [c for c in self.cases if c.row == case.row and c != case]
        for c in listCases:
            case.valid = case.valid and (c.value != case.value)

    def verifRow(self, position):
        """
        Vérifie la validité de la colonne après une modification.
        """
        case = self.cases[position]
        listCases = [c for c in self.cases if c.col == case.col and c != case]
        for c in listCases:
            case.valid = case.valid and (c.value != case.value)

    def verifRegion(self, position):
        """
        Vérifie la validité de la région (9x9) après une modification.
        """
        case = self.cases[position]
        start_row = (case.row // 3) * 3
        start_col = (case.col // 3) * 3
        listCases = [c for c in self.cases if start_row <= c.row < start_row + 3 and start_col <= c.col < start_col + 3 and c != case]
        for c in listCases:
            case.valid = case.valid and (c.value != case.value)

    def verif(self, position):
        """
        Vérifie la validité d'une case (ligne, colonne et région).
        """
        self.verifLine(position)
        self.verifRow(position)
        self.verifRegion(position)

    def checkWin(self):
        """
        Vérifie si la grille est gagnante.
        Une grille est gagnante si elle est remplie et toutes les cases sont valides.
        """
        for case in self.cases:
            if case.value is None or not case.valid:
                return False
        return True

    def __repr__(self):
        """
        Représentation du Sudoku sous forme de chaîne de caractères.
        """
        S = ''
        for i in range(81):
            if (i + 1) % 9 == 0:
                S += f'|{self.puzzleNow[i]}|\n'
            else:
                S += f'|{self.puzzleNow[i]}'
        return S

if __name__ == '__main__':
    import doctest
    doctest.testmod()
