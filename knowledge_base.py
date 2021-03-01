"""
Handles functionality related to the knowledge base
"""


def generate_knowledge_base(d: int):
    """
    Generates a blank knowledge base

    :param d: Array dimension
    :return: Blank knowledge base
    """
    arr = [['?' for i in range(d)] for j in range(d)]
    return arr


def mark_mine(kb, row, col, dim):
    """
    Marks a point as a potential mine (no impact on whether or not the mine explodes)

    :param kb: The knowledge base
    :param row: Row of the point I want to mark
    :param col: Col of the point I want to mark
    :param dim: Dimension of the knowledge base
    :return: True if point is marked as 'D' or False if failed
    """
    if row >= dim or col >= dim or row < 0 or col < 0:
        print("Out of bounds")
        return False
    if kb[row][col] == '?':
        kb[row][col] = 'D'
    return True


def mark_safe(kb, row, col, dim):
    """
    Marks a point as potentially safe (no impact on whether or not the mine explodes)

    :param kb: The knowledge base
    :param row: Row  of the point I want to mark
    :param col: Col of the point I want to mark
    :param dim: Dimension of the knowledge base
    :return: True if point is marked as 'S' or False if failed
    """
    if row >= dim or col >= dim or row < 0 or col < 0:
        print("Out of bounds")
        return False
    if kb[row][col] == '?':
        kb[row][col] = 'S'
    return True


def print_knowledge_base(kb):
    """
    Print what the player knows about the mine field

    :param kb: The knowledge base
    :return: Void, it just prints that knowledge base
    """
    print("This is the knowledge base:")
    print("Legend: '?' indicates unknown, 'D' is marked as dangerous, 'S' is marked as safe")
    print("'M' indicates revealed mine,'C' or a number indicates a revealed clear space")
    for row in kb:
        print(row)

    return


def count_neighbors(kb, d, row, col):
    """
    For the selected cell, count all neighbors
    :param kb: The knowledge base
    :param d: Dimension of the minefield
    :param row
    :param col
    :return: Number of neighbors I have
    """
    count = 0
    arr = kb
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for i in range(len(neighbors)):
        if isValid(kb, d, row + neighbors[i][0], col + neighbors[i][1]):
            count = count + 1

    return count


def count_unrevealed_neighbors(kb, d, row, col):
    """
    For the selected cell, count valid unrevealed neighbors
    :param kb: The knowledge base
    :param d: Dimension of the minefield
    :param row
    :param col
    :return: Number of neighbors I have
    """
    count = 0
    arr = kb
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for i in range(len(neighbors)):
        if isValid(kb, d, row + neighbors[i][0], col + neighbors[i][1]) and kb[row + neighbors[i][0]][col + neighbors[i][1]] == '?':
            count = count + 1

    return count


def count_revealed_neighbors(kb, d, row, col):
    """
        For the selected cell, count valid revealed neighbors
        :param kb: The knowledge base
        :param d: Dimension of the minefield
        :param row
        :param col
        :return: Number of neighbors I have
        """
    count = 0
    arr = kb
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for i in range(len(neighbors)):
        if isValid(kb, d, row + neighbors[i][0], col + neighbors[i][1]) and kb[row + neighbors[i][0]][col + neighbors[i][1]] != '?':
            count = count + 1

    return count


def count_safe_revealed_neighbors(kb, d, row, col):
    """
            For the selected cell, count valid revealed safe neighbors
            :param kb: The knowledge base
            :param d: Dimension of the minefield
            :param row
            :param col
            :return: Number of neighbors I have
            """
    count = 0
    arr = kb
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for i in range(len(neighbors)):
        if isValid(kb, d, row + neighbors[i][0], col + neighbors[i][1]) and kb[row + neighbors[i][0]][col + neighbors[i][1]] != '?' and kb[row + neighbors[i][0]][col + neighbors[i][1]] != 'M':
            count = count + 1

    return count


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