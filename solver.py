import logging

from sudoku import *

logger = logging.getLogger(__name__)


def rcb_check(board: Board) -> bool:
    """
    simplest solve check
    looks through each cell checking its row, col, and block and determines if only one option is available
    If only one option is available for a cell, it fills it in

    :param board: sudoku.Board() object with zeroed cells
    :return: returns @code True if changes were made to the board
    """

    if board:
        logger.info('board complete on rcb check')
        return False

    changes = False

    for x, y, item in board:
        if item == 0:
            options = board.options_for_position(x, y)
            if len(options) == 1:
                logger.debug(f'''cell {x, y} has one available option... placing {options[0]}''')
                board[x, y] = options[0]
                changes = True

    return changes


if __name__ == '__main__':
    logging.basicConfig(filename='sudoku.log', filemode='w', level=logging.INFO)

