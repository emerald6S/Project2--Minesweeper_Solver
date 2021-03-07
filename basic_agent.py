from random import randint
import random

from display_array import display_array
from manual_agent import *
from knowledge_base import *
from mine_utils import *


def basic_agent(board, kb, dim, n, p=False):
    """
        Automatically solve Minesweeper using the most basic way described by Dr Cowan
        :param board: The mine board
        :param kb: The knowledge base
        :param dim: The dimensions of the board/knowledge base
        :param n: Number of mines, only used to determine when the game ends. The agent themself doesn't take this into account.
        :param p: If I want to print the final knowledge base, defaults to False
        :return: A tuple of the format (number unrevealed mines, number total mines)
        """
    check = {}  # these are the REVEALED cells I have to check neighbors of
    fringe = {}  # these are UNREVEALED neighbors of cells I revealed
    # It's necessary to generate random coords the first time around
    row = randint(0, dim - 1)
    col = randint(0, dim - 1)
    kb = reveal_space(kb, board, row, col, dim)

    while not isAutoSolved(kb, n):
        # print("Current element: (" + str(row) + ", " + str(col) + ")")
        neighborMineCount = 0
        numUnrevealedNeighbors = count_unrevealed_neighbors(kb, dim, row, col)
        numRevealedNeighbors = count_revealed_mine_neighbors(kb, dim, row, col)
        numNeighbors = count_neighbors(kb, dim, row, col)
        if kb[row][col] != 'M' and kb[row][col] != 'D':
            if kb[row][col] == 'C':
                neighborMineCount = 0
            else:
                neighborMineCount = int(kb[row][col])

            if neighborMineCount - numRevealedNeighbors == numUnrevealedNeighbors:
                markAllNeighborsDangerous(kb, dim, row, col)
            elif numNeighbors - neighborMineCount - count_safe_revealed_neighbors(kb, dim, row,
                                                                                  col) == numUnrevealedNeighbors:
                markAllNeighborsSafe(kb, dim, row, col)

            fringe = addNeighborsToFringe(kb, dim, row, col, fringe)
            cleanFringe(check, fringe, kb, board, row, col, dim)
            revealAllSafe(kb, board, dim, fringe, check)

        if check:  # there's still a neighbor who I can check
            current = check.popitem()
            row = current[0][0]
            col = current[0][1]
        else:  # Must now randomly choose something from fringe, as I've exhausted all the conclusive elements
            # The trouble starts here
            keys = list(fringe.keys())
            if keys:
                randomKey = random.choice(keys)
                fringe.pop(randomKey)
            else:
                unrevealed = getAllUnrevealedInKB(kb, dim)
                keys = list(unrevealed.keys())
                randomKey = random.choice(keys)
                unrevealed.pop(randomKey)
            row = randomKey[0]
            col = randomKey[1]
            kb = reveal_space(kb, board, row, col, dim)
    if p:
        print_knowledge_base(kb)
    return isAutoSolved(kb, n)



#################################################
# HELPER FUNCTIONS
#################################################


def addNeighborsToFringe(kb, dim, row, col, fringe: dict):
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
        if isValid(kb, dim, row + neighbors[i][0], col + neighbors[i][1]) and (
                kb[row + neighbors[i][0]][col + neighbors[i][1]] == '?' or kb[row + neighbors[i][0]][
            col + neighbors[i][1]] == 'S'):
            fringe[(row + neighbors[i][0], col + neighbors[i][1])] = kb[row + neighbors[i][0]][col + neighbors[i][1]]
    return fringe


def cleanFringe(check: dict, fringe: dict, kb, board, row, col, dim):
    """
        Removes revealed safe and marked mine cells from fringe, and updates check

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
        if kb[key[0]][key[1]] == 'S' or kb[key[0]][key[1]] == 'D' or kb[key[0]][key[1]] == 'M':
            check[key] = fringe[key]
            del fringe[key]

    return fringe


def getAllCheck(kb, dim):
    """
    Adds all revealed elements with unrevealed neighbors to check

    :param kb:
    :param dim:
    :return:The new check dict
    """
    newCheck = {}
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for i in range(dim):
        for j in range(dim):

            for k in range(len(neighbors)):
                if isValid(kb, dim, i + neighbors[k][0], j + neighbors[k][1]) and kb[i][j] != "?" and kb[i][j] != "M" and kb[i][j] != 'D' and kb[i + neighbors[k][0]][j + neighbors[k][1]] == '?':
                    newCheck[(i, j)] = kb[i][j]

    return newCheck


def cleanCheck(check: dict, kb, dim):
    """
        Removes cells in check that lack hidden neighbors, and "D" or "M" cells in check

        :param check: The dict that stores all cells I must check later
        :param kb
        :param row
        :param col
        :param dim
        :return: dict, which is the updated fringe
        """
    for key in list(check):
        row = key[0]
        col = key[1]
        mineCell = False
        numHidden = 0
        if kb[row][col] == 'M' or kb[row][col] == 'D':
            mineCell = True
        if not mineCell:
            neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for i in range(len(neighbors)):
                if isValid(kb, dim, row + neighbors[i][0], col + neighbors[i][1]) and (
                        kb[row + neighbors[i][0]][col + neighbors[i][1]] == '?'):
                    numHidden = numHidden + 1
                    break
        if numHidden == 0 or mineCell == True:
            del check[key]

    return check


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
        if isValid(kb, dim, row + neighbors[i][0], col + neighbors[i][1]) and kb[row + neighbors[i][0]][col + neighbors[i][1]] == '?':
            mark_mine(kb, row + neighbors[i][0], col + neighbors[i][1], dim)
    return kb


def getAllUnrevealedInKB(kb, dim):
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


def revealAllSafe(kb, board, dim, fringe, check, autoReveal=False):
    """
    Reveals all marked safe elements in kb

    :param kb: The knowledge base
    :param board:
    :param dim: the dimensions of the kb
    :param fringe
    :param check
    :param autoReveal
    :return: Updated kb
    """
    for i in range(dim):
        for j in range(dim):
            if kb[i][j] == 'S':
                kb = reveal_space(kb, board, i, j, dim, False, autoReveal)
                fringe = addNeighborsToFringe(kb, dim, i, j, fringe)
                fringe = cleanFringe(check, fringe, kb, board, i, j, dim)

    return kb


def isAutoSolved(kb, n):
    """
    Check if board has been solved (for auto play)

    :param kb: Knowledge base
    :param n: Number of mines
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


def hasSafe(kb, dim):
    """
    Checks if kb has safe

    :param kb:
    :param dim:
    :return: True if safe, false otherwise
    """

    for i in range(dim):
        for j in range(dim):
            if kb[i][j] == 'S':
                return True

    return False
