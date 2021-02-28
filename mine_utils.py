"""
Contains some functions I couldn't decide where else to put yet
"""
# will need a function to check if a cell is safe or not


def reveal_space(kb, board, row, col, dim):
    """
    Reveal the chosen space on the minefield

    :param kb: Kknowledge base
    :param board: Minefield board
    :param row: Row of the point I want to uncover
    :param col: Col of the point I want to uncover
    :param dim: Dimensions of the board
    :return: The new knowledge base, or the original knowledge base if the X or Y coord is out of bounds or space already revealed
    """
    if row >= dim or col >= dim or row < 0 or col < 0:
        print("Out of bounds")
    else:
        if kb[row][col] == board[row][col]:
            print("That space was already revealed!")
        else:
            kb[row][col] = board[row][col]
            if board[row][col] == 'M':
                print("BOOM! Mine revealed!")
            else:
                print("Mine not detected")

    return kb
