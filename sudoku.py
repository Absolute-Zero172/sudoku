from copy import deepcopy
from random import choice, randint

import logging

logger = logging.getLogger(__name__)


class Board:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for __ in range(9)]

        self.x, self.y = 0, 0

        logger.debug('made sudoku board object')

    def __getitem__(self, item):
        if not isinstance(item, tuple):
            logger.warning('tried to get cell with incorrect item')
            raise TypeError("The values inside brackets must be separated with commas - Ex. sudoku[1, 2]")
        elif len(item) != 2:
            logger.warning('tried to get cell with incorrect item')
            raise IndexError("Two values must be provided (the coordinates of the item) - Ex. sudoku[1, 2]")
        else:
            logger.debug(f'returned board item at {item}')
            return self.board[item[1]][item[0]]

    def __setitem__(self, key, value):
        if not isinstance(key, tuple) or not isinstance(value, int):
            logger.warning('tried to get set with incorrect item')
            raise TypeError("The values inside brackets must be separated with commas and the right side of the equal "
                            "sign must be an int (0-9) - Ex. sudoku[1, 2] = 3")
        elif len(key) != 2:
            logger.warning('tried to get set with incorrect item')
            raise IndexError("Two values must be provided (the coordinates of the item) - Ex. sudoku[1, 2]")
        else:
            logger.debug(f'set board cell at {key} to {value}')
            self.board[key[1]][key[0]] = value

    def __str__(self):
        output = '\n'
        b = self.board
        for row in range(9):
            if row % 3 == 0 and row != 0 and row != 9:
                output += '--------|---------|--------\n'
            output += ' ' + str(b[row][0]) + ' ' + str(b[row][1]) + ' ' + str(b[row][2]) + ' ' + ' | ' + ' ' + str(
                b[row][3]) + ' ' + str(b[row][4]) + ' ' + str(b[row][5]) + ' ' + ' | ' + ' ' + str(
                b[row][6]) + ' ' + str(b[row][7]) + ' ' + str(b[row][8]) + ' \n'
        logger.debug('returned string object')
        return output.replace('0', '_')

    def __eq__(self, other):
        logger.debug('determining board equality')
        if isinstance(other, Board):
            if other.board == self.board:
                return True
        return False

    def __bool__(self):
        logger.debug('identifying board state')
        for idx in range(9):
            if not self.is_row_complete(idx):
                return False
            if not self.is_column_complete(idx):
                return False
            if not self.is_block_complete(idx):
                return False

        return True

    def copy(self):
        logger.debug('copied board')
        output = Board()
        output.board = deepcopy(self.board)
        return output

    def clear(self):
        logger.debug('cleared board')
        self.board = [[0 for _ in range(9)] for __ in range(9)]

    def __iter__(self):
        return self

    def __next__(self):
        logger.debug('next cell accessed')

        x, y = self.x, self.y

        self.x += 1
        if self.x > 8:
            self.y += 1
            self.x = 0

        if self.y > 8 and self.x > 0:
            self.x, self.y = 0, 0
            raise StopIteration()

        return x, y, self[x, y]

    def is_row_complete(self, row_index):
        logger.debug(f'determining if row {row_index} is complete')
        r = self.board[row_index].copy()
        r.sort()
        return r == [i for i in range(1, 10)]

    def is_column_complete(self, column_index):
        logger.debug(f'determining if column {column_index} is complete')
        c = [self.board[i][column_index] for i in range(9)]
        c.sort()
        return c == [i for i in range(1, 10)]

    def is_block_complete(self, block_index):
        logger.debug(f'determining if block {block_index} is complete')
        block_list = []
        xst = 0
        yst = 0
        if 0 <= block_index <= 2:
            x_index = block_index
            xst = x_index * 3
            yst = 0
        elif 3 <= block_index <= 5:
            x_index = block_index - 3
            xst = x_index * 3
            yst = 3
        elif 6 <= block_index <= 8:
            x_index = block_index - 6
            xst = x_index * 3
            yst = 6

        for y in range(3):
            for x in range(3):
                block_list.append(self.board[yst + y][xst + x])

        block_list.sort()

        return block_list == [i for i in range(1, 10)]

    def options_for_position(self, x, y):
        ideal = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        row_index = y
        column_index = x
        block_index = (x // 3) + (3 * (y // 3))

        row = self.board[row_index]
        column = [self.board[i][column_index] for i in range(9)]

        block_list = []
        xst = 0
        yst = 0
        if 0 <= block_index <= 2:
            x_index = block_index
            xst = x_index * 3
            yst = 0
        elif 3 <= block_index <= 5:
            x_index = block_index - 3
            xst = x_index * 3
            yst = 3
        elif 6 <= block_index <= 8:
            x_index = block_index - 6
            xst = x_index * 3
            yst = 6

        for y in range(3):
            for x in range(3):
                block_list.append(self.board[yst + y][xst + x])

        taken = []
        for item in row:
            if item != 0 and item not in taken:
                taken.append(item)
                ideal.pop(ideal.index(item))
        for item in column:
            if item != 0 and item not in taken:
                taken.append(item)
                ideal.pop(ideal.index(item))
        for item in block_list:
            if item != 0 and item not in taken:
                taken.append(item)
                ideal.pop(ideal.index(item))

        logger.debug(f'determined options for {x, y} as {ideal}')
        return ideal

    def get_random_option(self, x, y):
        return choice(self.options_for_position(x, y))

    def random_populate(self):
        logger.debug('randomly populating board')
        success = False

        while not success:
            self.clear()

            x, y = 0, 0

            while y <= 8 and len(self.options_for_position(x, y)) > 0:
                random_option = self.get_random_option(x, y)

                self[x, y] = random_option

                x += 1
                if x > 8:
                    x = 0
                    y += 1

            if self:
                logger.debug('board randomly set')
                success = True

    def get_zeroes(self):
        logger.debug('determining zeroes in board')
        zeroes = []

        for y in range(9):
            for x in range(9):
                if self[x, y] == 0:
                    zeroes.append((x, y))

        return zeroes


def place_random_zero(board: Board) -> None:
    zeroes = board.get_zeroes()

    if len(zeroes) == 81:
        return None

    coordinates = randint(0, 8), randint(0, 8)
    while coordinates in zeroes:
        coordinates = randint(0, 8), randint(0, 8)

    board[coordinates] = 0
    logger.debug('placed random zero in board')


def place_zeroes(board: Board, number_of_zeroes: int) -> None:
    for _ in range(number_of_zeroes):
        place_random_zero(board)

    logger.debug(f'placed {number_of_zeroes} in board')


def prepare_board(zeroes=50) -> Board:
    board = Board()
    board.random_populate()
    place_zeroes(board, zeroes)

    logger.info('zeroed board prepared')

    return board
