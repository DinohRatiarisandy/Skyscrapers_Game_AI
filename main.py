import time

from algorithm import SkyscraperSolver


class Game:
    def __init__(self, size: int, clues: tuple[list[int], list[int]]):
        self.size = size
        self.top_clues = clues[0]
        self.bottom_clues = clues[1]
        self.left_clues = clues[2]
        self.right_clues = clues[3]
        self.board = [[0 for _ in range(size)] for _ in range(size)]


class BoardView:
    def __init__(self, game: Game):
        self.game = game
        N = self.game.size
        self.view = [[0 for _ in range(N + 2)] for _ in range(N + 2)]
        self._place_clues()
        self.update_board()

    def _place_clues(self) -> None:
        N = self.game.size
        self.view[0][1 : N + 1] = self.game.top_clues
        self.view[N + 1][1 : N + 1] = self.game.bottom_clues

        for r in range(1, N + 1):
            self.view[r][0] = self.game.left_clues[r - 1]
            self.view[r][N + 1] = self.game.right_clues[r - 1]

    def update_board(self) -> None:
        for r in range(self.game.size):
            for c in range(self.game.size):
                self.view[r + 1][c + 1] = self.game.board[r][c]

    def show(self) -> None:
        for row in self.view:
            print(row)


if __name__ == "__main__":
    t0 = time.time()

    # Initialisation
    size = 6
    left = [2, 3, 3, 5, 1, 3]
    top = [2, 1, 3, 2, 2, 4]
    right = [5, 2, 2, 1, 4, 3]
    bottom = [2, 5, 1, 2, 4, 2]

    game = Game(size, (top, bottom, left, right))

    # Initialisasion for big skyscraper state
    game.board[2][4] = 1
    game.board[4][1] = 3

    view = BoardView(game)
    print("Plateau initial :")
    view.show()
    print("\nRésolution en cours...\n")

    solver = SkyscraperSolver(
        board=game.board,
        left_clues=game.left_clues,
        top_clues=game.top_clues,
        right_clues=game.right_clues,
        bottom_clues=game.bottom_clues,
    )

    solution = solver.search_solution(solver.board)

    if solution:
        game.board = solution
        view.update_board()
        print("Solution :")
        view.show()
    else:
        print("❌ Aucune solution trouvée.")

    print(f"\nTemps d'exécution : {time.time() - t0:.3f} s")
