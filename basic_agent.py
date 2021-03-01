from random import randint
import random
from manual_agent import *
from knowledge_base import *
from mine_utils import *

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


# TODO: Fix infinite loop where I keep selecting the same element over and over again
def basic_agent(board, kb, dim, n, p=False):
    """
        Automatically solve Minesweeper using the most basic way described by Dr Cowan

        :param board: The mine board
        :param kb: The knowledge base
        :param dim: The dimensions of the board/knowledge base
        :param n: Number of mines, only used to determine when the game ends. The agent themself doesn't take this into account.
        :param p: If I want to print the final knowledge base, defaults to False
        :return: Void, when the only uncovered elements are mines or entire board is searched
        """
    check = {}  # these are the REVEALED cells I have to check neighbors of
    fringe = {}  # these are UNREVEALED neighbors of cells I revealed
    # It's necessary to generate random coords the first time around
    row = randint(0, dim - 1)
    col = randint(0, dim - 1)
    kb = reveal_space(kb, board, row, col, dim)

    while not isAutoSolved(kb, n, dim):
        # print("Current element: (" + str(row) + ", " + str(col) + ")")
        neighborMineCount = 0
        numUnrevealedNeighbors = count_unrevealed_neighbors(kb, dim, row, col)
        numRevealedNeighbors = count_revealed_neighbors(kb, dim, row, col)
        numNeighbors = count_neighbors(kb, dim, row, col)
        if kb[row][col] != 'M':
            if kb[row][col] == 'C':
                neighborMineCount = 0
            else:
                neighborMineCount = int(kb[row][col])

            if neighborMineCount - numRevealedNeighbors == numUnrevealedNeighbors:
                markAllNeighborsDangerous(kb, dim, row, col)
            elif numNeighbors - neighborMineCount - count_safe_revealed_neighbors(kb, dim, row, col) == numUnrevealedNeighbors:
                markAllNeighborsSafe(kb, dim, row, col)

        fringe = addToFringe(kb, dim, row, col, fringe)
        cleanFringe(check, fringe, kb, board, row, col, dim)
        updateAllSafe(kb, board, dim)
        if check:
            current = check.popitem()
            row = current[0][0]
            col = current[0][1]
        else:  # Must now randomly choose something from fringe, as I've exhausted all the conclusive elements
            keys = list(fringe.keys())
            if keys:
                randomKey = random.choice(keys)
                fringe.pop(randomKey)
            else:
                unrevealed = getAllUnrevealedinKB(kb, dim)
                keys = list(unrevealed.keys())
                randomKey = random.choice(keys)
                unrevealed.pop(randomKey)
            row = randomKey[0]
            col = randomKey[1]
            kb = reveal_space(kb, board, row, col, dim)
    if p:
        print_knowledge_base(kb)
    return isAutoSolved(kb, n, dim)


#################################################
# HELPER FUNCTIONS
#################################################


def addToFringe(kb, dim, row, col, fringe: dict):
    """
    Add all unrevealed neighbors to the fringe

    :param kb: The knowledge base
    :param dim: The dimensions of the board
    :param row:
    :param col:
    :param fringe: The fringe, where I store all cells that are unrevealed and border cells I checked
    :return: dict, which is the updated fringe
    """
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for i in range(len(neighbors)):
        if isValid(kb, dim, row + neighbors[i][0], col + neighbors[i][1]) and (kb[row + neighbors[i][0]][col + neighbors[i][1]] == '?' or kb[row + neighbors[i][0]][col + neighbors[i][1]] == 'S'):
            fringe[(row + neighbors[i][0], col + neighbors[i][1])] = kb[row + neighbors[i][0]][col + neighbors[i][1]]
    return fringe


def cleanFringe(check: dict, fringe: dict, kb, board, row, col, dim):
    """
        Removes revealed safe and marked mine cells from fringe, reveal their contents, then adds their neighbors to the fringe

        :param check: The dict that stores all cells I must check later
        :param fringe: The fringe, where I store all cells that are unrevealed and border cells I checked
        :param kb
        :param board
        :param row
        :param col
        :param dim
        :return: dict, which is the updated fringe
        """
    for key in list(fringe):
        if fringe[key] == 'S' or fringe[key] == 'D' or fringe[key] == 'M':
            check[key] = fringe[key]
            del fringe[key]

    return fringe


def markAllNeighborsSafe(kb, dim, row, col):
    """
    Marks all unrevealed neighbors as safe

    :param kb: The knowledge base
    :param dim: The dimensions of the board
    :param row:
    :param col:
    :return: The updated knowledge base
    """
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for i in range(len(neighbors)):
        if isValid(kb, dim, row + neighbors[i][0], col + neighbors[i][1]) and kb[row + neighbors[i][0]][
            col + neighbors[i][1]] == '?':
            mark_safe(kb, row + neighbors[i][0], col + neighbors[i][1], dim)
    return kb


def markAllNeighborsDangerous(kb, dim, row, col):
    """
    Marks all unrevealed neighbors as dangerous

    :param kb: The knowledge base
    :param dim: The dimensions of the board
    :param row:
    :param col:
    :return: The updated knowledge base
    """
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for i in range(len(neighbors)):
        if isValid(kb, dim, row + neighbors[i][0], col + neighbors[i][1]) and kb[row + neighbors[i][0]][
            col + neighbors[i][1]] == '?':
            mark_mine(kb, row + neighbors[i][0], col + neighbors[i][1], dim)
    return kb


def getAllUnrevealedinKB(kb, dim):
    """
    Gets all unrevealed and unmarked elements of the kb

    :param kb: The knowledge base
    :param dim: the dimensions of the kb
    :return: dictionary that contains all unrevealed and unmarked elements of kb
    """
    unrevealed = {}
    for i in range(dim):
        for j in range(dim):
            if kb[i][j] == '?':
                unrevealed[(i, j)] = kb[i][j]

    return unrevealed


def updateAllSafe(kb, board, dim):
    """
    Updates all safe elements in kb

    :param kb: The knowledge base
    :param board:
    :param dim: the dimensions of the kb
    :return: Updated kb
    """
    for i in range(dim):
        for j in range(dim):
            if kb[i][j] == 'S':
                kb = reveal_space(kb, board, i, j, dim)

    return kb


def isAutoSolved(kb, n, dim):
    """
    Check if board has been solved (for auto play)

    :param kb: Knowledge base
    :param n: Number of mines
    :param dim: Dimensions of the board
    :return: A tuple of the format (mines left, total number of mines) that represents the score, none otherwise
    """
    mines_left = n
    spaces_left = 0
    for row in kb:
        for i in row:
            if i == '?' or i == 'D' or i == "S":
                # if space is revealed to be safe
                spaces_left = spaces_left + 1
            elif i == 'M':
                # if space is revealed to be a mine
                mines_left = mines_left - 1

    if mines_left == 0:
        return mines_left, n
    elif spaces_left <= mines_left:
        return mines_left, n

    else:
        return
