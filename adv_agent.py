# TODO:
# -- Do basic agent up to the point where I must randomly choose a new point
# -- The fun starts when I have run out of things in check (no cells where, taken alone, I can conclusively decide is safe or not).
# -- 1. Do a proof by contradiction foe each cell in fringe where I assume that the unrevealed space is a mine. If the board's information becomes incorrect, then that space must be safe safe
# -- 2. If the attempted proofs by contradiction fails to detect a safe cell, then create all possible mine configs. Obviously throw away any solution that makes the board incorrect
# -- 3. Now compare all the mine position configs. Reveal the space that has the least number of configs that mark it as a mine. In the case of a tie, choose randomly
#
# Potential time saver: if the fringe isn't contiguous, then I may split it

from basic_agent import *
from display_array import *
from copy import *


def adv_agent(board, kb, dim, n, p=False):
    """
            Automatically solve Minesweeper using the more advanced agent.

            :param board: The mine board
            :param kb: The knowledge base
            :param dim: The dimensions of the board/knowledge base
            :param n: Number of mines, only used to determine when the game ends. The agent themself doesn't take this into account.
            :param p: If I want to print the final knowledge base, defaults to False
            :return: A tuple of the format (number unrevealed mines, number total mines)
            """
    # It's necessary to generate random coords the first time around
    row = randint(0, dim - 1)
    col = randint(0, dim - 1)
    kb = reveal_space(kb, board, row, col, dim, False, True)
    if p:
        print("-----------------")
        print("Current element: (" + str(row) + ", " + str(col) + ")")
        print("Contents are: " + kb[row][col])
        display_array(kb, dim, row, col)

    while not isAutoSolved(kb, n):
        check = getAllCheck(kb, dim)
        fringe = {}  # these are UNREVEALED neighbors of cells I revealed
        # Check all cells in check
        for key in list(check):
            row = key[0]
            col = key[1]
            if kb[row][col] != 'M' or kb[row][col] != 'D':
                numUnrevealedNeighbors = count_unrevealed_neighbors(kb, dim, row, col)
                numRevealedMineNeighbors = count_revealed_mine_neighbors(kb, dim, row, col)
                numNeighbors = count_neighbors(kb, dim, row, col)
                if kb[row][col] == 'C':
                    neighborMineCount = 0
                else:
                    neighborMineCount = int(kb[row][col])

                if neighborMineCount-numRevealedMineNeighbors == numUnrevealedNeighbors:
                    markAllNeighborsDangerous(kb, dim, row, col)
                elif numNeighbors - neighborMineCount - count_safe_revealed_neighbors(kb, dim, row, col) == numUnrevealedNeighbors:
                    markAllNeighborsSafe(kb, dim, row, col)

                fringe = addNeighborsToFringe(kb, dim, row, col, fringe)

            if p:
                print("-----------------")
                print("Current element: (" + str(row) + ", " + str(col) + ")")
                print("Contents are: " + kb[row][col])
                display_array(kb, dim, row, col)

        cleanFringe(check, fringe, kb, board, row, col, dim)
        safe = hasSafe(kb, dim)
        #########
        if safe:  # there's safe cells I can reveal
            if p:
                print("There's still cells that can be conclusively id'd")
            revealAllSafe(kb, board, dim, fringe, check, True)

        else:  # Must now randomly choose something from fringe, as I've exhausted all the conclusive elements
            # The trouble starts here, as the basic agent has zero way of figuring out probability
            keys = list(fringe.keys())
            flag_proof = False
            if keys:
                for key in list(fringe):
                    if proofByContradiction(kb, dim, check, key):
                        if p:
                            print("By proof of contradiction, element (" + str(key[0]) + ", " + str(
                                key[1]) + ") is NOT a mine")
                        kb = reveal_space(kb, board, key[0], key[1], False, False)
                        flag_proof = True
                        break
            if not flag_proof:
                keys = list(fringe.keys())
                if p:
                    print("Choosing randomly now")
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
                kb = reveal_space(kb, board, row, col, dim, False, True)
                if p:
                    print("-----------------")
                    print("Current element: (" + str(row) + ", " + str(col) + ")")
                    print("Contents are: " + kb[row][col])
                    display_array(kb, dim, row, col)

    if p:
        print("-----------------")
        print_knowledge_base(kb)
    return isAutoSolved(kb, n)


#################################################
# HELPER FUNCTIONS
#################################################


def proofByContradiction(kb, dim, check: dict, key):
    """
    Performs a proof by contradiction on the selected fringe key (doesn't accept fringe as input)
    This function will assume that the key is a mine, and create a copy of the kb except update the key so that it's a mine
    If at least 1 element in the check changes due to the new information, return True and reveal this cell
    Else return false

    :param kb:
    :param dim:
    :param check:
    :param key: A tuple, the key of the cell I want to see if is mine or not
    :return: boolean, true if proven to be safe and false otherwise
    """
    kbCopy = deepcopy(kb)  # I only should edit this one
    kbCopy[key[0]][key[1]] = 'D'
    checkCopy = {}

    row = key[0]
    col = key[1]
    numUnrevealedNeighbors = count_unrevealed_neighbors(kbCopy, dim, row, col)
    numRevealedNeighbors = count_revealed_mine_neighbors(kbCopy, dim, row, col)
    numNeighbors = count_neighbors(kbCopy, dim, row, col)
    # Change the copy of the knowledge base to reflect the assumption
    for key in list(check):
        thisRow = key[0]
        thisCol = key[1]
        if kbCopy[thisRow][thisCol] != 'M' or kbCopy[thisRow][thisCol] != 'D':
            if kbCopy[thisRow][thisCol] == 'C':
                neighborMineCount = 0
            else:
                neighborMineCount = int(kb[thisRow][thisCol])

            if neighborMineCount - numRevealedNeighbors == numUnrevealedNeighbors:
                markAllNeighborsDangerous(kbCopy, dim, thisRow, thisCol)
            elif numNeighbors - neighborMineCount - count_safe_revealed_neighbors(kbCopy, dim, thisRow,
                                                                                  thisCol) == numUnrevealedNeighbors:
                markAllNeighborsSafe(kbCopy, dim, thisRow, thisCol)

    for key in list(check):
        checkCopy[key] = kbCopy[key[0]][key[1]]
    if check == checkCopy:
        return False
    else:
        return True

