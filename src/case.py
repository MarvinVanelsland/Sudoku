class Case:
    def __init__(self, position, value=None):
        """
        Constructeur pour la classe Case.
        :param position: indice de la case (0 à 80)
        :param value: valeur de la case (par défaut None)
        """
        self.position = position
        self.value = value
        self.row = position // 9  # Calcul de la ligne, valeur entre 0 et 8
        self.col = position % 9   # Calcul de la colonne, valeur entre 0 et 8
        self.valid = True         # Par défaut, la case est valide

    def setValue(self, value):
        """
        Méthode pour définir la valeur de la case.
        """
        self.value = value
