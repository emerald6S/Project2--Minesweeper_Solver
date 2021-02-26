from mine_utils import *
from knowledge_base import *

"""
1. check is a given cell is safe or mine or currently covered
    --write a check_cell method
2. if safe check the number of neighbors that are mine. 
    -- function to check the num of mines
    -- function to check the num of safe cells
    -- function to check the cell with num
    -- function to check the hidden cells
3. randomly choose


"""
num_mines = 0
num_safe = 0
num_covered = 0


def isMine(arr, dim, row, col):
    """
    Check to see if the selected cell is a mine or not
    :param arr: the array we want to check
    :param dim:  the dimension of the array
    :param row:  X coordinate
    :param col:  Y coordinate
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
    :param row:  X coordinate
    :param col:  Y coordinate
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
    :param row:  X coordinate
    :param col:  Y coordinate
    :return: True if is covered else false
    """
    if arr[row][col] == '?':
        return True
    else:
        return False
