from copy import deepcopy


class Board:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for __ in range(9)]

    def __getitem__(self, item):
        if not isinstance(item, tuple):
            raise TypeError("The values inside brackets must be separated with commas - Ex. sudoku[1, 2]")
        elif len(item) != 2:
            raise IndexError("Two values must be provided (the coordinates of the item) - Ex. sudoku[1, 2]")
        else:
            return self.board[item[1]][item[0]]

    def __setitem__(self, key, value):
        if not isinstance(key, tuple) or not isinstance(value, int):
            raise TypeError("The values inside brackets must be separated with commas and the right side of the equal "
                            "sign must be an int (0-9) - Ex. sudoku[1, 2] = 3")
        elif len(key) != 2:
            raise IndexError("Two values must be provided (the coordinates of the item) - Ex. sudoku[1, 2]")
        else:
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
        return output.replace('0', '_')

    def __eq__(self, other):
        if isinstance(other, Board):
            if other.board == self.board:
                return True
        return False

    def copy(self):
        output = Board()
        output.board = deepcopy(self.board)
        return output

    def is_row_complete(self, row_index):
        r = self.board[row_index]
        r.sort()
        return r == [i for i in range(1, 10)]

    def is_column_complete(self, column_index):
        c = [self.board[i][column_index] for i in range(9)]
        c.sort()
        return c == [i for i in range(1, 10)]

    def check_block(self, block_index):
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
