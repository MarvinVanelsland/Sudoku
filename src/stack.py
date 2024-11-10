class Stack:
    def __init__(self):
        """
        Constructeur pour la classe Stack.
        Initialise une pile vide.
        """
        self.stack = []

    def push(self, item):
        """
        Ajouter un élément à la pile.
        """
        self.stack.append(item)

    def pop(self):
        """
        Retirer et retourner l'élément du sommet de la pile.
        """
        if not self.empty():
            return self.stack.pop()
        return None

    def empty(self):
        """
        Vérifie si la pile est vide.
        """
        return len(self.stack) == 0

    def __repr__(self):
        """
        Représentation sous forme de chaîne de caractères.
        """
        return repr(self.stack)
