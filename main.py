"""
✔️ Le script principal (main.py) utilise la classe Game
pour créer un jeu Skyscrapers de taille N avec des indices donnés.
✔️ Il utilise également la classe SolveBoard pour résoudre le jeu 
et affiche la solution, le cas échéant.
Le temps d'exécution est également mesuré.
"""

import time

from solveur import SolveBoard


class Game:
    def __init__(self, N, clues):
        """
        Initialise un jeu Skyscrapers avec la taille N et les indices donnés.

        Args:
            N (int): La taille du Skyscrapers.
            clues (tuple): Indices horizontaux et verticaux du Skyscrapers.
        """
        self.N = N
        self.clues_horiz = clues[0]
        self.clues_verti = clues[1]
        self.board = [[0 for _ in range(N)] for _ in range(N)]
        self.board_view = [[0 for _ in range(N + 2)] for _ in range(N + 2)]
        self.place_clue_horiz()
        self.place_clue_verti()

    def show_board(self):
        """
        Affiche le plateau actuel.
        """
        for row in self.board_view:
            print(row)

    def place_clue_horiz(self):
        """
        Place les indices horizontaux sur le plateau.
        """
        self.board_view[0][1 : self.N + 1] = self.clues_horiz[0]
        self.board_view[self.N + 1][1 : self.N + 1] = self.clues_horiz[1]

    def place_clue_verti(self):
        """
        Place les indices verticaux sur le plateau.
        """
        for r in range(1, self.N + 1):
            self.board_view[r][0] = self.clues_verti[0][r - 1]
            self.board_view[r][self.N + 1] = self.clues_verti[1][r - 1]

    def show_solution(self):
        """
        Affiche la solution sur le plateau.
        """
        for r in range(1, self.N + 1):
            for c in range(1, self.N + 1):
                self.board_view[r][c] = self.board[r - 1][c - 1]

        self.show_board()


if __name__ == "__main__":
    t0 = time.time()

    # Crée un jeu Skyscrapers avec des indices initiaux
    game = Game(
        5, [([2, 3, 2, 4, 1], [3, 3, 2, 1, 3]), ([2, 1, 2, 3, 3], [1, 4, 2, 3, 2])]
    )
    #           ^          ^                ^                  ^                 ^
    #           N         TOP             DOWN               LEFT              RIGHT

    # Affiche le plateau avec les conditions initiales.
    game.show_board()

    # Résout le Skyscrapers
    solve = SolveBoard(game.board, game.clues_horiz, game.clues_verti)

    print("\n------------------\n")

    solution = solve.solve()

    if solution:
        print("Solution:\n")
        game.board = solution
        game.show_solution()
    else:
        print("Aucune solution trouvée !")

    t1 = time.time()

    # Affiche le temps d'exécution
    print(f"\nTemps d'exécution: {t1-t0:.3f} s")
