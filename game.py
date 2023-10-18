from random import sample
from copy import deepcopy
from priority_queue import PriorityQueue
import sys

# Define the game board size
BOARD_SIZE = 3


class Game:
    def __init__(self, board=None, verbose=True) -> None:
        self._all_numbers = list(range(BOARD_SIZE ** 2))
        self._choices = sample(self._all_numbers, k=BOARD_SIZE**2)
        self.board = self.create_board(self._choices) if not board else board
        while not self.is_solvable(self.board):
            if verbose:
                print('not solvable', self.board)
            self._choices = sample(self._all_numbers, k=BOARD_SIZE**2)
            self.board = self.create_board(self._choices)

        if verbose:
            print("board created", self.board)
        self.closet_set = set()
        self.goal = self.create_board(self._all_numbers)

    def create_board(self, choices):
        board = []
        _temp = []
        for it, s in enumerate(choices):
            _temp.append(s)
            if (it + 1) % BOARD_SIZE == 0:
                board.append(deepcopy(_temp))
                _temp.clear()
        return board
    
    def get_board(self):
        return deepcopy(self.board)
    
    def get_inv_count(self, arr):
        if BOARD_SIZE == 3:
            inv_count = 0   
            empty_value = 0
            for i in range(0, 9):
                for j in range(i + 1, 9):
                    if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                        inv_count += 1
            return inv_count
        elif BOARD_SIZE == 4:
            arr1=[]
            for y in arr:
                for x in y:
                    arr1.append(x)
            arr=arr1
            inv_count = 0
            for i in range(BOARD_SIZE * BOARD_SIZE - 1):
                for j in range(i + 1,BOARD_SIZE * BOARD_SIZE):
                    if (arr[j] and arr[i] and arr[i] > arr[j]):
                        inv_count+=1
            return inv_count
    
 
     
    # This function returns true
    # if given 8 puzzle is solvable.
    def is_solvable(self, puzzle) :
        if BOARD_SIZE == 3:
            # Count inversions in given 8 puzzle
            inv_count = self.get_inv_count([j for sub in puzzle for j in sub])
        
            # return true if inversion count is even.
            return (inv_count % 2 == 0)
        elif BOARD_SIZE == 4:
                # Count inversions in given puzzle
            invCount = self.get_inv_count(puzzle)
        
            # If grid is odd, return true if inversion
            # count is even.
            if (BOARD_SIZE & 1):
                return ~(invCount & 1)
        
            else:    # grid is even
                pos = self.find_x_position(puzzle)
                if (pos & 1):
                    return ~(invCount & 1)
                else:
                    return invCount & 1
    
 
    # find Position of blank from bottom
    def find_x_position(self, puzzle):
        # start from bottom-right corner of matrix
        for i in range(BOARD_SIZE - 1,-1,-1):
            for j in range(BOARD_SIZE - 1,-1,-1):
                if (puzzle[i][j] == 0):
                    return BOARD_SIZE - i
                
        


    def get_empty_position(self, board):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == 0:
                    return row, col

    def get_valid_moves(self, row, col):
        valid_moves = []
        if row > 0:
            valid_moves.append("up")
        if row < BOARD_SIZE - 1:
            valid_moves.append("down")
        if col > 0:
            valid_moves.append("left")
        if col < BOARD_SIZE - 1:
            valid_moves.append("right")
        return valid_moves
    
    def get_all_possible_states(self, board, huristic):
        row, col = self.get_empty_position(board)
        valid_moves = self.get_valid_moves(row, col)
        states = []
        if 'right' in valid_moves:
            _state = deepcopy(board)
            _state[row][col], _state[row][col + 1] = _state[row][col + 1], _state[row][col]
            states.append((_state, huristic.calculate(_state)))
        if 'left' in valid_moves:
            _state = deepcopy(board)
            _state[row][col], _state[row][col - 1] = _state[row][col - 1], _state[row][col]
            states.append((_state, huristic.calculate(_state)))
        if 'up' in valid_moves:
            _state = deepcopy(board)
            _state[row][col], _state[row - 1][col] = _state[row - 1][col], _state[row][col]
            states.append((_state, huristic.calculate(_state)))
        if 'down' in valid_moves:
            _state = deepcopy(board)
            _state[row][col], _state[row + 1][col] = _state[row + 1][col], _state[row][col]
            states.append((_state, huristic.calculate(_state)))
        return states

    def solve(self, huristic=None):
        priorityq = PriorityQueue()
        start_state = [self.board]
        goal_test = lambda x: x[-1] == self.goal

        if not huristic:
            huristic = NumberOfWrongTiles()
        print(str(huristic))

        it = 1
        priorityq.insert(start_state, huristic.calculate(start_state[0]))
        while True:
            current_state = priorityq.remove()
            it += 1
            while tuple(map(lambda x: tuple(x), current_state[-1])) in self.closet_set:
                current_state = priorityq.remove()

            print(f'\rIteration: {it} -- Huristic: {huristic.calculate(current_state[-1])} -- Cost: {len(current_state) - 1}', end=' ')
            if goal_test(current_state):
                print('\n[+] Board is solved')
                return current_state

            sys.stdout.flush()
            all_states = self.get_all_possible_states(current_state[-1], huristic)
            for state, hur in all_states:
                _current_state = deepcopy(current_state)
                _current_state.append(state)
                priorityq.insert(_current_state, hur + len(current_state) + 1)
            self.closet_set.add(tuple(map(lambda x: tuple(x), current_state[-1])))


class Huristic:
    def calculate(self):
        ...
    
    def __str__(self) -> str:
        return ""


class NumberOfWrongTiles(Huristic):
    def calculate(self, board):
        hu = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if i * BOARD_SIZE + j != board[i][j]:
                    hu += 1
        return hu
    
    def __str__(self) -> str:
        return "----- NumberOfWrongTiles -----"

class NumberOfWrongTilesDividesTwo(Huristic):
    def calculate(self, board):
        hu = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if i * BOARD_SIZE + j != board[i][j]:
                    hu += 1
        return hu // 2
    
    def __str__(self) -> str:
        return "----- NumberOfWrongTilesDividesTwo -----"
    
class NumberOfWrongTilesDividesThree(Huristic):
    def calculate(self, board):
        hu = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if i * BOARD_SIZE + j != board[i][j]:
                    hu += 1
        return hu // 3

class NumberOfWrongTilesTimesTwo(Huristic):
    def calculate(self, board):
        hu = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if i * BOARD_SIZE + j != board[i][j]:
                    hu += 1
        return hu * 2
    
    def __str__(self) -> str:
        return "----- NumberOfWrongTilesTimesTwo -----"