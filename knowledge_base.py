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
