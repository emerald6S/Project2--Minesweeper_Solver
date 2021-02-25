"""
Contains some functions I couldn't decide where else to put yet
"""
# will need a function to check if a cell is safe or not
"""


def isValid(board, dim, row, col):
    if (row < 0) or (col < 0) or (row >= dim) or (col >= dim):
        return False
    else:
        return True
    
def isMine(board, dim, row, col):
    if board[row][col] == 'M':
        return true
    else:
        return false
def check_safe(kb,row,col, board, dim):
    ##for i in range of(dim):
      
      ##  for j in range of(dim):
            if board[i][j] == 'M':
                return 2
            if board[i][j] == '?':
                return 0
            if(! not M and F) 
                return 1

def compare_agent(kb,board,dim):
    dx = [] #for neighbors
    dy= []
    for i in range of dim:
        for j in range of dim:
            if (check_safe(kb, roq,col,board,dim) == 1):
                for i in ramge of 4
    
"""

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
