from game import Game, NumberOfWrongTiles, NumberOfWrongTilesDividesTwo, NumberOfWrongTilesTimesTwo
from gui import PuzzleGame


def solve_infinity_puzzles():
    while True:
        puzzle = Game()
        solution = puzzle.solve()

def solve_infinity_puzzles_all_huristics():
    huristics = [
        NumberOfWrongTiles(),
        NumberOfWrongTilesDividesTwo(),
        NumberOfWrongTilesTimesTwo()
    ]

    while True:
        puzzle_temp = Game(verbose=False)
        board = puzzle_temp.get_board()
        for h in huristics:
            puzzle = Game(board=board)
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

    # solve_infinity_puzzles_all_huristics()
    animate()


if __name__ == '__main__':
    main()