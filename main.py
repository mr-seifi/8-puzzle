from game import Game, NumberOfWrongTiles, NumberOfWrongTilesDividesTwo, NumberOfWrongTilesTimesTwo, EuclideanDistance, ManhattanDistance
from gui import PuzzleGame
from copy import deepcopy


def solve_infinity_puzzles():
    while True:
        puzzle = Game()
        solution = puzzle.solve()

def solve_infinity_puzzles_all_huristics():
    huristics = [
        NumberOfWrongTiles(),
        NumberOfWrongTilesDividesTwo(),
        NumberOfWrongTilesTimesTwo(),
        EuclideanDistance(),
        ManhattanDistance(),
    ]

    while True:
        puzzle_temp = Game(verbose=False)
        board = puzzle_temp.get_board()
        for h in huristics:
            print('BOARD:', board)
            puzzle = Game(board=deepcopy(board))
            solution = puzzle.solve(huristic=h)
        
        print('--------------------------------------')

def animate(board=None, huristic=None):
    puzzle = Game(board)
    solution = puzzle.solve(huristic=huristic)
    initial_state = [
        solution[0]
    ]

    game = PuzzleGame(initial_state)

    for i in range(1, len(solution)):
        game.animate_solver(solution[i])

    game.start()

def main():

    solve_infinity_puzzles_all_huristics()
    # animate(huristic=NumberOfWrongTiles())


if __name__ == '__main__':
    main()