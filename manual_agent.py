from knowledge_base import *
from mine_utils import *

"""
This file lets you play Minesweeper manually, without the aid of a CPU player
"""


def play_minesweeper(board, kb, dim, n):
    """
    Manually play Minesweeper

    :param board: The mine board
    :param kb: The knowledge base
    :param dim: The dimensions of the board/knowledge base
    :param n: Number of mines
    :return: Void, when the only uncovered elements are mines or entire board is searched
    """
    print("\nManually playing Minesweeper")
    while not is_solved(kb, n, dim):
        print("Here are your options")
        print("1 - Check cell for mine")
        print("2 - Mark a cell as dangerous")
        print("3 - Mark a cell as safe")
        print("4 - Print the knowledge base")
        print("Q - Quit the game")
        option = input("Which option do you want to choose? ")
        if option == '1':
            row = input("Select the row number, must be a number from 0 to " + str(int(dim) - 1) + " ")
            col = input("Select the col number, must be a number from 0 to " + str(int(dim) - 1) + " ")
            kb = reveal_space(kb, board, int(row), int(col), dim)

        elif option == '2':
            row = input("Select the row number, must be a number from 0 to " + str(int(dim) - 1) + " ")
            col = input("Select the col number, must be a number from 0 to " + str(int(dim) - 1) + " ")
            mark_mine(kb, int(row), int(col), dim)

        elif option == '3':
            row = input("Select the row number, must be a number from " + str(0) + " to " + str(dim - 1))
            col = input("Select the col number, must be a number from " + str(0) + " to " + str(dim - 1))
            mark_safe(kb, int(row), int(col), dim)

        elif option == '4':
            print_knowledge_base(kb)

        elif option == 'Q' or option == 'q' or option == 'Quit' or option == 'quit':
            print("Quit playing the game")
            break
        else:
            print("Oops, invalid option, try again!")

    return


def is_solved(kb, n, dim):
    """
    Check if board has been solved (for manual play)

    :param kb: Knowledge base
    :param n: Number of mines
    :param dim: Dimensions of the board
    :return: True if the number of unrevealed spaces is less than or equal to mines unrevealed, or if all mines have been tripped, False otherwise
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
        print("Game over, you tripped all the mines, stupid!")
        print("That means you dodged a grand total of 0 out of " + str(n) + " mines total")
        print_knowledge_base(kb)
        return True
    elif spaces_left <= mines_left:
        print("Game over! Only unrevealed spaces left are mines!")
        print("You dodged " + str(mines_left) + " out of " + str(n) + " mines total")
        print_knowledge_base(kb)
        return True

    else:
        return False
