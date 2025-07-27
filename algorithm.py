"""
✔️ La classe SolveBoard est utilisée pour résoudre le jeu Skyscrapers de taille N.
Elle prend en compte le plateau actuel, les indices horizontaux et verticaux
du jeu pour trouver une solution.

✔️ Cette classe utilise une approche récursive pour explorer les différentes combinaisons
possibles et sélectionne la meilleure solution qui respecte les règles du jeu.
Le backtracking est utilisé pour revenir en arrière lorsque des combinaisons
incompatibles sont détectées.
"""

from abc import ABC, abstractmethod
from copy import deepcopy
from enum import Enum

BoardType = list[list[int]]


class Axis(Enum):
    """Axe qu'on utilise dans l'algorithme de résolution.
    Soit ROW: 0
    Soit COLUMN: 1

    Args:
        Enum (_type_): Enum
    """

    ROW = 0
    COLUMN = 1


class BaseSolver(ABC):
    """Template pour la classe de la résolution du jeu

    Args:
        ABC (_type_): Abstract Base Class
    """

    def __init__(self, board: BoardType):
        self.board = deepcopy(board)
        self.board_size = len(board)  # board is always square (NxN)

    def solve(self) -> BoardType:
        self.place_obvious_numbers()
        return self.search_solution(self.board)

    @abstractmethod
    def place_obvious_numbers(self) -> None:
        pass

    @abstractmethod
    def search_solution(self, board: BoardType) -> None:
        pass


class ValidatorStrategy(ABC):
    """Template pour la classe de la validation du jeu

    Args:
        ABC (_type_): Abstract Base Class
    """

    @abstractmethod
    def can_place_number(self, board: BoardType, row: int, col: int, num: int) -> bool:
        pass

    @abstractmethod
    def is_valid_solution(self, board: BoardType) -> bool:
        pass


class SkyscraperValidator(ValidatorStrategy):
    def __init__(
        self,
        left_clues: list[int],
        top_clues: list[int],
        right_clues: list[int],
        bottom_clues: list[int],
    ):
        """Classe pour regrouper toutes les fonctions du validation d'une configuration d'un jeu

        Args:
            left_clues (list[int]): Les nombres de skyscrapers qu'on voit en placant à gauche
            top_clues (list[int]): Les nombres de skyscrapers qu'on voit en placant en haut
            right_clues (list[int]): Les nombres de skyscrapers qu'on voit en placant à droite
            bottom_clues (list[int]): Les nombres de skyscrapers qu'on voit en placant en bas
        """
        self.left_clues = left_clues
        self.top_clues = top_clues
        self.right_clues = right_clues
        self.bottom_clues = bottom_clues
        self.clues_len = len(top_clues)  # all clues have the same length

    def can_place_number(self, board: BoardType, row: int, col: int, num: int) -> bool:
        """Place temporairement le nombre `num` dans la cellule (r, c) du `board`,
        puis vérifie si les indices sont respectées. Si oui, retourne True.
        Sinon, return False

        Args:
            board (BoardType): Le plateau du jeu actuel
            row (int): indice de la cellule sur la ligne
            col (int): indice de la cellule sur la colonne
            num (int): le nombre à placer sur la cellule (r, c)

        Returns:
            bool: Return True si on peu placer le num dans la cellule. Sinon, False
        """
        for i in range(self.clues_len):
            if board[i][col] == num or board[row][i] == num:
                return False

        board[row][col] = num
        return self.is_valid_solution(board, row, col)

    def is_valid_solution(self, board: BoardType, row: int, col: int) -> bool:
        """Checker si la configuration du jeu actuelle est valide.

        Args:
            board (BoardType): La configuration actuelle du jeu
            row (int): L'indice du ligne
            col (int): L'indice du colonne

        Returns:
            bool: True si la configuration actuelle est valide, c-à-d qui respecte
            les règles du jeu.
            False sinon.
        """
        for i in range(self.clues_len):
            if self._respect_clues(board, row, Axis.ROW) and self._respect_clues(
                board, col, Axis.COLUMN
            ):
                return True
        return False

    def is_full(self, board: BoardType, index: int, axis: Axis) -> bool:
        """Checker si une rangée ou colonne est remplie.

        Args:
            board (BoardType): plateau du jeu
            index (int): indice dans le plateau du jeu à checker
            axis (Axis): l'axe où on va checker (ligne ou colonne)

        Returns:
            bool: True si la rangée ou colonne est remplie
        """
        if axis == Axis.ROW:
            return all(val != 0 for val in board[index])
        else:
            return all(board[i][index] != 0 for i in range(self.clues_len))

    def _respect_clues(self, board: BoardType, index: int, axis: Axis) -> bool:
        """Checker si la configuration du board respecte les contraintes (clues)

        Args:
            board (BoardType): le plateau du jeu
            index (int): indice dans le plateau du jeu
            axis (Axis): axe à checker

        Returns:
            bool: True si la configuration respecte les contraintes. Sinon, False.
        """

        def count_visible(values: list[int]) -> int:
            """Compter les nombres de skyscrapers dans une position

            Args:
                values (list[int]): les hauteurs des skyscrapers

            Returns:
                int: le nombre des skyscrapers vu dans une position
            """
            count = 0
            max_height = -float("inf")
            for val in values:
                if val > max_height:
                    max_height = val
                    count += 1
            return count

        if axis == Axis.ROW:
            values = board[index]
            start_clue = self.left_clues[index]
            end_clue = self.right_clues[index]
        elif axis == Axis.COLUMN:
            values = [board[r][index] for r in range(self.clues_len)]
            start_clue = self.top_clues[index]
            end_clue = self.bottom_clues[index]

        start_count = count_visible(values)

        if self.is_full(board, index, axis):
            end_count = count_visible(values[::-1])
            return start_count == start_clue and end_count == end_clue
        else:
            return start_count <= start_clue


class SkyscraperSolver(BaseSolver):
    def __init__(
        self,
        board: BoardType,
        left_clues: list[int],
        top_clues: list[int],
        right_clues: list[int],
        bottom_clues: list[int],
    ):
        """Classe pour la résolution d'un plateau de jeu.

        Args:
            board (BoardType): configuration du plateau de jeu
            left_clues (list[int]): Les nombres de skyscrapers qu'on voit en placant à gauche
            top_clues (list[int]): Les nombres de skyscrapers qu'on voit en placant en haut
            right_clues (list[int]): Les nombres de skyscrapers qu'on voit en placant à droite
            bottom_clues (list[int]): Les nombres de skyscrapers qu'on voit en placant en bas
        """
        super().__init__(board)
        # So, SkyscraperSolver have `board`` and `board_size` attributes.
        self.left_clues = left_clues
        self.top_clues = top_clues
        self.right_clues = right_clues
        self.bottom_clues = bottom_clues
        self.validator = SkyscraperValidator(
            left_clues, top_clues, right_clues, bottom_clues
        )
        self.place_obvious_numbers()

    def place_obvious_numbers(self) -> None:
        """Placer les nombres évidentes dans le plateau du jeu dans les 2 axes (ligne et colonne)"""
        self._place_obvious_by_axis(Axis.ROW, self.left_clues, self.right_clues)
        self._place_obvious_by_axis(Axis.COLUMN, self.top_clues, self.bottom_clues)

    def _place_obvious_by_axis(
        self, axis: Axis, clues_start: list[int], clues_end: list[int]
    ) -> None:
        """Placer les nombres évidentes dans le plateau du jeu.

        Args:
            axis (Axis): On place les nombres sur la ligne ou colonne, selon l'axis.
            clues_start (list[int]): left_clues ou top_clues
            clues_end (list[int]): right_clues ou bottom_clues
        """
        for index in range(self.board_size):
            # Clue from the start
            if clues_start[index] == 1:
                if axis == Axis.ROW:
                    self.board[index][0] = self.board_size
                else:
                    self.board[0][index] = self.board_size
            elif clues_start[index] == self.board_size:
                for i in range(self.board_size):
                    if axis == Axis.ROW:
                        self.board[index][i] = i + 1
                    else:
                        self.board[i][index] = i + 1

            # Clue from the end
            if clues_end[index] == 1:
                if axis == Axis.ROW:
                    self.board[index][-1] = self.board_size
                else:
                    self.board[-1][index] = self.board_size
            elif clues_end[index] == self.board_size:
                for i in range(self.board_size):
                    if axis == Axis.ROW:
                        self.board[index][self.board_size - 1 - i] = i + 1
                    else:
                        self.board[self.board_size - 1 - i][index] = i + 1

    def _find_empty_cell(self, board: BoardType) -> tuple[int, int] | None:
        """Chercher une cellule vide dans la configuration du plateau du jeu passé en argument.

        Args:
            board (BoardType): La configuration du plateau du jeu

        Returns:
            tuple[int, int] | None: Return la coordonnée de la première cellule vide (r, c)
        """
        for r in range(self.board_size):
            for c in range(self.board_size):
                if board[r][c] == 0:
                    return (r, c)
        return None

    def search_solution(self, board: BoardType) -> BoardType | None:
        """La méthode/fonction déclencheur de la recherche de solution.

        Args:
            board (BoardType): La configuration du plateau de jeu.

        Returns:
            BoardType | None: Retourner une configuration de plateau de jeu valide,
            ou None s'il n'y en a pas.
        """
        empty_cell = self._find_empty_cell(board)
        if empty_cell is None:
            for i in range(self.board_size):
                if self.validator.is_valid_solution(board, i, i):
                    return board
            return None

        r, c = empty_cell
        for num in range(1, self.board_size + 1):
            copied_board = deepcopy(board)
            if self.validator.can_place_number(copied_board, r, c, num):
                copied_board[r][c] = num
                result = self.search_solution(copied_board)
                if result is not None:
                    return result
        return None
