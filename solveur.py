"""
✔️ La classe SolveBoard est utilisée pour résoudre le jeu Skyscrapers de taille N.
Elle prend en compte le plateau actuel, les indices horizontaux et verticaux 
du jeu pour trouver une solution.

✔️ Cette classe utilise une approche récursive pour explorer les différentes combinaisons
possibles et sélectionne la meilleure solution qui respecte les règles du jeu.
Le backtracking est utilisé pour revenir en arrière lorsque des combinaisons 
incompatibles sont détectées.
"""

from copy import deepcopy

class SolveBoard:
    def __init__(self, board, clues_horiz, clues_verti):
        """
        Initialise un SolveBoard avec un plateau, des indices horizontaux et verticaux.
        
        Args:
            board (list[list[int]]): Le plateau de Skyscrapers initial.
            clues_horiz (list[list[int]]): Les indices horizontaux du Skyscrapers.
            clues_verti (list[list[int]]): Les indices verticaux du Skyscrapers.
        """
        self.N = len(board)
        self.board = board
        self.clues_horiz = clues_horiz
        self.clues_verti = clues_verti
        self.place_obvious_numbers()

    def place_obvious_numbers(self):
        """
        Place les nombres évidents sur le plateau en utilisant les indices horizontaux et verticaux.
        """
        self.place_obvious_numbers_horizontal()
        self.place_obvious_numbers_vertical()

    def place_obvious_numbers_horizontal(self):
        """
        Place les nombres évidents dans les lignes du plateau en fonction des indices horizontaux.
        """
        for idx, (top_clue, down_clue) in enumerate(zip(self.clues_horiz[0], self.clues_horiz[1])):
            if top_clue == 1:
                self.board[0][idx] = self.N
            elif top_clue == self.N:
                for r in range(self.N):
                    self.board[r][idx] = r + 1

            if down_clue == 1:
                self.board[self.N-1][idx] = self.N
            elif down_clue == self.N:
                for r in range(self.N-1, -1, -1):
                    self.board[r][idx] = self.N - r

    def place_obvious_numbers_vertical(self):
        """
        Place les nombres évidents dans les colonnes du plateau en fonction des indices verticaux.
        """
        for idx, (left_clue, right_clue) in enumerate(zip(self.clues_verti[0], self.clues_verti[1])):
            if left_clue == 1:
                self.board[idx][0] = self.N
            elif left_clue == self.N:
                for c in range(self.N):
                    self.board[idx][c] = c + 1

            if right_clue == 1:
                self.board[idx][self.N-1] = self.N
            elif right_clue == self.N:
                for c in range(self.N-1, -1, -1):
                    self.board[idx][c] = self.N - c

    def full(self, current_board, i, to_check):
        """
        Vérifie si une ligne ou une colonne spécifiée dans le plateau est complète (toutes les cases remplies).

        Args:
            current_board (list[list[int]]): Le plateau actuel.
            i (int): L'indice de la ligne ou de la colonne à vérifier.
            to_check (str): "row" pour vérifier une ligne, "col" pour vérifier une colonne.

        Returns:
            bool: True si la ligne ou la colonne est complète, False sinon.
        """
        if to_check == "row":
            # Vérifie si toutes les valeurs dans la ligne spécifiée sont différentes de zéro
            return all(val != 0 for val in current_board[i])
        else:  # to_check == "col"
            # Vérifie s'il y a une valeur nulle dans la colonne spécifiée
            return all(current_board[c][i] != 0 for c in range(self.N))


    def is_valid(self, current_board, r, c, num):
        """
        Vérifie si placer un nombre dans la cellule (r, c) est une configuration valide.

        Args:
            current_board (list[list[int]]): Le plateau actuel.
            r (int): L'indice de ligne.
            c (int): L'indice de colonne.
            num (int): Le nombre à placer.

        Returns:
            bool: True si la configuration est valide, False sinon.
        """
        for i in range(self.N):
            if current_board[i][c] == num or current_board[r][i] == num:
                return False

        current_board[r][c] = num
        return self.respect_clues_horiz(current_board, r) and self.respect_clues_verti(current_board, c)

    def respect_clues_horiz(self, current_board, r):
        """
        Vérifie si les indices horizontaux sont respectés pour une ligne donnée.

        Args:
            current_board (list[list[int]]): Le plateau actuel.
            r (int): L'indice de ligne.

        Returns:
            bool: True si les indices horizontaux sont respectés, False sinon.
        """
        left = 0
        max_ = -float("inf")

        for i in range(self.N):
            if current_board[r][i] > max_:
                left += 1
                max_ = current_board[r][i]

        if self.full(current_board, r, "row"):
            right = 0
            max_ = -float("inf")
            for i in range(self.N-1, -1, -1):
                if current_board[r][i] > max_:
                    right += 1
                    max_ = current_board[r][i]
            return left == self.clues_verti[0][r] and right == self.clues_verti[1][r]

        return left <= self.clues_verti[0][r]

    def respect_clues_verti(self, current_board, c):
        """
        Vérifie si les indices verticaux sont respectés pour une colonne donnée.

        Args:
            current_board (list[list[int]]): Le plateau actuel.
            c (int): L'indice de colonne.

        Returns:
            bool: True si les indices verticaux sont respectés, False sinon.
        """
        top = 0
        max_ = -float("inf")

        for j in range(self.N):
            if current_board[j][c] > max_:
                top += 1
                max_ = current_board[j][c]

        if self.full(current_board, c, "col"):
            max_ = -float("inf")
            down = 0
            for j in range(self.N-1, -1, -1):
                if current_board[j][c] > max_:
                    down += 1
                    max_ = current_board[j][c]
            return top == self.clues_horiz[0][c] and down == self.clues_horiz[1][c]

        return top <= self.clues_horiz[0][c]

    def find_empty_cell(self, current_board):
        """
        Trouve la première cellule vide dans le plateau.

        Args:
            current_board (list[list[int]]): Le plateau actuel.

        Returns:
            tuple: Coordonnées de la première cellule vide, ou None si aucune cellule n'est vide.
        """
        for r in range(self.N):
            for c in range(self.N):
                if current_board[r][c] == 0:
                    return (r, c)
        return None

    def solve_recursive(self, current_board, r, c):
        """
        Fonction récursive pour résoudre le Skyscrapers.

        Args:
            current_board (list[list[int]]): Le plateau actuel.
            r (int): L'indice de ligne.
            c (int): L'indice de colonne.

        Returns:
            list[list[int]]: Le plateau résolu, ou None si aucune solution n'est trouvée.
        """
        empty_cell = self.find_empty_cell(current_board)

        if empty_cell is None:
            for i in range(self.N):
                if not (self.respect_clues_horiz(current_board, i) and self.respect_clues_verti(current_board, i)):
                    return None

            return current_board

        r, c = empty_cell
        for num in range(1, self.N+1):
            if self.is_valid(current_board, r, c, num):
                new_board = deepcopy(current_board)
                new_board[r][c] = num

                # Appel récursif avec la nouvelle configuration
                result = self.solve_recursive(new_board, r, c + 1)
                if result is not None:
                    return result

                result = self.solve_recursive(new_board, r + 1, c)
                if result is not None:
                    return result

        return None  # Aucune solution trouvée

    def solve(self):
        """
        Fonction principale pour résoudre le Skyscrapers.

        Returns:
            list[list[int]]: Le plateau résolu, ou None si aucune solution n'est trouvée.
        """
        initial_board = deepcopy(self.board)
        return self.solve_recursive(initial_board, 0, 0)

