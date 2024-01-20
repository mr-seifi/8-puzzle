from random import sample
from copy import deepcopy
from priority_queue import PriorityQueue
import sys
from math import sqrt
import numpy as np


BOARD_SIZE = 3
class Game:
    def __init__(self, board=None, verbose=True) -> None:
        self._stop = BOARD_SIZE*BOARD_SIZE
        self._all_numbers = np.arange(start=0, stop=self._stop, step=1)
        if board is None:
            self._choices = np.random.choice(self._all_numbers, self._stop, replace=False)
            self.board = self.create_board(self._choices)
        else:
            self._choices = board.reshape(self._stop)
            self.board = board

        while not self.is_solvable(self.board):
            if verbose:
                print('not solvable', self.board)
            self._choices = np.random.choice(self._all_numbers, self._stop, replace=False)
            self.board = self.create_board(self._choices) if not board else board

        if verbose:
            print("board created", self.board)
        self.closet_set = set()
        self.goal = self.create_board(self._all_numbers)

    def create_board(self, choices):
        return choices.reshape(BOARD_SIZE, BOARD_SIZE)
    
    def get_board(self):
        return deepcopy(self.board)
    
    def get_inv_count(self, arr):
        if BOARD_SIZE == 3:
            inv_count = 0
            for i in range(0, self._stop):
                inv_count += (arr[i+1:][arr[i+1:] > 0] < arr[i]).sum()
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
    
    def is_solvable(self, puzzle) :
        if BOARD_SIZE == 3:
            inv_count = self.get_inv_count(self._choices)
            return (inv_count % 2 == 0)
        elif BOARD_SIZE == 4:
            invCount = self.get_inv_count(puzzle)
            if (BOARD_SIZE & 1):
                return ~(invCount & 1)
        
            else:
                pos = self.find_x_position(puzzle)
                if (pos & 1):
                    return ~(invCount & 1)
                else:
                    return invCount & 1
    
 
    def find_x_position(self, _):
        return BOARD_SIZE - (np.where(self._choices == 0)[0][0] // BOARD_SIZE)
                

    def get_empty_position(self, board):
        index = np.where(board == 0)
        return index[0][0], index[1][0]

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
        goal_test = lambda x: (x[-1] == self.goal).all()

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
    def __init__(self) -> None:
        self.goal = np.arange(start=0, stop=BOARD_SIZE*BOARD_SIZE, step=1).reshape(BOARD_SIZE, BOARD_SIZE)

    def calculate(self):
        ...
    
    def __str__(self) -> str:
        return ""


class NumberOfWrongTiles(Huristic):
    def calculate(self, board):
        hu = (board != self.goal).sum()
        return hu
    
    def __str__(self) -> str:
        return "----- NumberOfWrongTiles -----"

class NumberOfWrongTilesDividesTwo(Huristic):
    def calculate(self, board):
        hu = (board != self.goal).sum()
        return hu // 2
    
    def __str__(self) -> str:
        return "----- NumberOfWrongTilesDividesTwo -----"


class NumberOfWrongTilesTimesTwo(Huristic):
    def calculate(self, board):
        hu = (board != self.goal).sum()
        return hu * 2
    
    def __str__(self) -> str:
        return "----- NumberOfWrongTilesTimesTwo -----"
    
class EuclideanDistance(Huristic):
    def calculate(self, board):
        hu = 0
        for k in range(0, BOARD_SIZE*BOARD_SIZE):
            current = np.where(board == k)
            goal = np.where(self.goal == k)
            hu += np.sqrt(np.power(current[0][0] - goal[0][0], 2) + np.power(current[1][0] - goal[1][0], 2))
        return hu
    
    def __str__(self) -> str:
        return "----- EuclideanDistance -----"
    

class ManhattanDistance(Huristic):
    def calculate(self, board):
        hu = 0
        for k in range(0, BOARD_SIZE*BOARD_SIZE):
            current = np.where(board == k)
            goal = np.where(self.goal == k)
            hu += np.abs(current[0][0] - goal[0][0]) + np.abs(current[1][0] - goal[1][0])
        return hu
    
    def __str__(self) -> str:
        return "----- ManhattanDistance -----"