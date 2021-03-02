from random import randint

from mine_utils import *

"""
Handles functionality related to creating a minefield
"""


def generate_board(d: int, n: int):
    """
    Randomly generate an empty minefield and populate with mines
    The legend:
    M is a mine
    C is clear
    a number 0-8 represents how many neighbor mines I have
    ? is unrevealed
    D is marked as dangerous
    S is marked as safe

    :param d: The dimension of the array you want to generate, must be a whole number
    :param n: The number of mines, must also be a whole number
    :return: Generated array of dimension d*d with n randomly placed mines
    """

    if (d <= 0):
        print("Dimension must be greater than 0")
        return

    if (d <= 0):
        print("There must be at least 1 mine!")
        return

    arr = [['C' for i in range(d)] for j in range(d)]  # prevents shallow lists
    # C for clear, M for mine

    mines_left = n
    while mines_left > 0:
        x = randint(0, d - 1)
        y = randint(0, d - 1)

        if arr[x][y] != 'M':
            arr[x][y] = 'M'
            mines_left = mines_left - 1

    arr = count_mine_neighbors(arr, d)
    return arr


##################
# HELPER FUNCTIONS
##################
def count_mine_neighbors(board, d):
    """
    For the empty cells of the minefield, count number of mines
    :param board: The minefield
    :param d: Dimension of the minefield
    :return: The minefield but empty cells have mine neighbor count
    """
    arr = board
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for i in range(d):
        for j in range(d):
            if board[i][j] == 'C':
                mine_count = 0
                for k in range(len(neighbors)):
                    newX = i + neighbors[k][0]
                    newY = j + neighbors[k][1]
                    if isValid(board, d, newX, newY):
                        if board[newX][newY] == 'M':
                            mine_count = mine_count + 1
                arr[i][j] = str(mine_count)

    return arr


def print_board(board):
    """
    Print the mine field

    :param board: The minefield
    :return: Void, it just prints a mine field
    """
    print("This is the minefield:")
    print("Legend: 'M = mine, C = clear, printed number is also clear and indicates how many of the neighbors are mines")
    for row in board:
        print(row)

    return

