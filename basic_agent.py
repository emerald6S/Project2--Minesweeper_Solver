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
    if arr[row][col] == 'M':
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


def isValid(board, dim, row, col):
    if (row < 0) or (col < 0) or (row >= dim) or (col >= dim):
        return False
    else:
        return True


def fillInVisited(arr, dim, visited):
    for i in range(dim):
        for j in range(dim):
            if arr[i][j] == '-' and visited[i][j] == True:
                arr[i][j] = "V"
    return arr


def basic_agent(arr, dim, kb, n):
    print("In the basic agent")

    visited = [[False for i in range(dim)] for j in range(dim)]
    visited[0][0] = True

    num_hidden = dim * dim
    num_mines = 0
    num_safe = 0
    num_covered = 0
    num_revealed_mine = 0
    num_revealed_safe = 0
    hidden = []
    random_neighbors = []

    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    while num_hidden > 0:
        if num_hidden == dim * dim:  # if it is the first move choose any point randomly
            # while num_hidden != 0:
            dx = randint(0, dim - 1)
            dy = randint(0, dim - 1)

            # print("Printing the first random point chosen", dx, dy)
            if not visited[dx][dy]:
                if isSafe(arr, dim, dx, dy):
                    # kb[dx][dy] = arr[dx][dy]
                    mark_safe(kb, dx, dy, dim)
                    visited[dx][dy] = True
                    # print("Printing Kb")
                    # print_knowledge_base(kb)
                    num_revealed_safe = num_revealed_safe + 1
                    num_hidden = num_hidden - 1
                    for i in range(len(neighbors)):
                        newX = dx + neighbors[i][0]
                        newY = dy + neighbors[i][1]
                        if isValid(arr, dim, newX, newY):
                            # random_neighbors = [(newX, newY)]
                            random_neighbors.append((newX, newY))
                            print("Printing random neighbors:", random_neighbors)
                            if arr[newX][newY] == 'M':
                                num_mines = num_mines + 1
                            if kb[newX][newY] == '?':
                                hidden = [(newX, newY)]
                                num_covered = num_covered + 1
                            if arr[newX][newY] != 'M':
                                num_safe = num_safe + 1

                    n = arr[dx][dy]

                    if int(n) - num_revealed_mine == num_covered:
                        for i in range(len(hidden)):
                            x = hidden[i][0]
                            y = hidden[i][1]
                            # kb[x][y] = 'M'
                            mark_mine(kb, x, y, dim)
                            num_revealed_mine = num_revealed_mine + 1
                            num_hidden = num_hidden - 1

                    if num_safe - num_revealed_safe == num_hidden:
                        for i in range(len(hidden)):
                            x = hidden[i][0]
                            y = hidden[i][1]
                            # kb[x][y] = arr[x][y]
                            mark_safe(kb, x, y, dim)
                            num_revealed_safe = num_revealed_safe + 1
                            num_hidden = num_hidden - 1

                if isMine(arr, dim, dx, dy):
                    # print("In first check for mine")
                    # kb[dx][dy] = 'M'
                    visited[dx][dy] = True
                    mark_mine(kb, dx, dy, dim)
                    num_hidden = num_hidden - 1
                    num_revealed_mine = num_revealed_mine + 1
                    for i in range(len(neighbors)):
                        newX = dx + neighbors[i][0]
                        newY = dy + neighbors[i][1]
                        if isValid(arr, dim, newX, newY):
                            # random_neighbors = [(newX, newY)]
                            random_neighbors.append((newX, newY))

            # print("Printing the final KB")
            # print_knowledge_base(kb)
            # return

        else:
            random_point = random.choice(random_neighbors)
            dx = random_point[0]
            dy = random_point[1]
            if not visited[dx][dy]:
                if isSafe(arr, dim, dx, dy):
                    visited[dx][dy] = True
                    # kb[dx][dy] = arr[dx][dy]
                    mark_safe(kb, dx, dy, dim)
                    num_revealed_safe = num_revealed_safe + 1
                    num_hidden = num_hidden - 1
                    for i in range(len(neighbors)):
                        newX = dx + neighbors[i][0]
                        newY = dy + neighbors[i][1]
                        if isValid(arr, dim, newX, newY):
                            # random_neighbors = [(newX, newY)]
                            random_neighbors.append((newX, newY))
                            if arr[newX][newY] == 'M':
                                num_mines = num_mines + 1
                            if kb[newX][newY] == '?':
                                hidden = [(newX, newY)]
                                num_covered = num_covered + 1
                            if arr[newX][newY] != 'M':
                                num_safe = num_safe + 1

                    n = arr[dx][dy]

                    if int(n) - num_revealed_mine == num_covered:
                        for i in range(len(hidden)):
                            x = hidden[i][0]
                            y = hidden[i][1]
                            # kb[x][y] = 'M'
                            mark_mine(kb, x, y, dim)
                            # visited[dx][dy] = True
                            num_revealed_mine = num_revealed_mine + 1
                            num_hidden = num_hidden - 1

                    if num_safe - num_revealed_safe == num_hidden:
                        for i in range(len(hidden)):
                            x = hidden[i][0]
                            y = hidden[i][1]
                            # kb[x][y] = arr[x][y]
                            mark_safe(kb, x, y, dim)
                            # visited[dx][dy] = True
                            num_revealed_safe = num_revealed_safe + 1
                            num_hidden = num_hidden - 1

                if isMine(arr, dim, dx, dy):
                    visited[dx][dy] = True
                    # kb[dx][dy] = 'M'
                    mark_mine(kb, dx, dy, dim)
                    num_hidden = num_hidden - 1
                    num_revealed_mine = num_revealed_mine + 1
                    for i in range(len(neighbors)):
                        newX = dx + neighbors[i][0]
                        newY = dy + neighbors[i][1]
                        if isValid(arr, dim, newX, newY):
                            #random_neighbors = [(newX, newY)]
                            random_neighbors.append((newX, newY))

    print_knowledge_base(kb)
    return
