"""
Contains utility functions that I couldn't neatly categorize
"""
# will need a function to check if a cell is safe or not
from knowledge_base import *
from knowledge_base import print_knowledge_base


def reveal_space(kb, board, row, col, dim, p=False):
    """
    Reveal the chosen space on the minefield

    :param kb: Knowledge base
    :param board: Minefield board
    :param row: Row of the point I want to uncover
    :param col: Col of the point I want to uncover
    :param dim: Dimensions of the board
    :param p: whether or not I should print the results, defaults to False
    :return: The new knowledge base, or the original knowledge base if the X or Y coord is out of bounds or space already revealed
    """

    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    if p == True and (row >= dim or col >= dim or row < 0 or col < 0):
        print("Out of bounds")
    else:
        if kb[row][col] == board[row][col]:
            if p:
                print("That space was already revealed!")
        else:
            kb[row][col] = board[row][col]
            if board[row][col] == 'M':
                if p:
                    print("BOOM! Mine revealed!")
            elif board[row][col] != 'M':
                if p:
                    print("Mine not detected")
                for i in range(len(neighbors)):
                    # reveal all neighbor cells that aren't mines and have no neighboring mines
                    newRow = row + neighbors[i][0]
                    newCol = col + neighbors[i][1]
                    if isValid(board, dim, newRow, newCol) and (board[row][col] == "0" or board[row][col] == 'C') and board[newRow][newCol] != 'M' and kb[row][col] == board[row][col]:
                        kb = reveal_space(kb, board, newRow, newCol, dim, False)

    return kb


def isMine(arr, dim, row, col):
    """
    Check to see if the selected cell is a mine or not
    :param arr: the array we want to check
    :param dim:  the dimension of the array
    :param row:
    :param col:
    :return: True if is a mine else false
    """
    if arr[row][col] == 'M':
        return True
    else:
        return False


def isSafe(arr, dim, row, col):
    """
    Check to see if the selected cell is safe or not
    :param arr: the array we want to check
    :param dim:  the dimension of the array
    :param row:
    :param col:
    :return: True if is safe else false
    """
    if arr[row][col] == 'M' or arr[row][col] == '?':
        return False
    else:
        return True


def isCovered(arr, dim, row, col):
    """
    Check to see if the selected cell is covered or not
    :param arr: the array we want to check
    :param dim:  the dimension of the array
    :param row:
    :param col:
    :return: True if is covered else false
    """
    if arr[row][col] == '?':
        return True
    else:
        return False


def isValid(arr, dim, row, col):
    """
    Check to see if the selected list element is in bounds

    :param arr: The array I want to check
    :param dim: The square dimensions of the array
    :param row:
    :param col:
    :return: True if in bounds, or False if out of bounds
    """
    if (row < 0) or (col < 0) or (row >= dim) or (col >= dim):
        return False
    else:
        return True
