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
    # First, copy the code from the basic agent
    check = {}  # these are the REVEALED cells I have to check neighbors of
    fringe = {}  # these are UNREVEALED neighbors of cells I revealed
    # It's necessary to generate random coords the first time around
    row = randint(0, dim - 1)
    col = randint(0, dim - 1)
    kb = reveal_space(kb, board, row, col, dim)

    while not isAutoSolved(kb, n):
        if p:
            print("Current element: (" + str(row) + ", " + str(col) + ")")
            print("Contents are: " + kb[row][col])
            display_array(kb, dim, row, col)
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
            elif numNeighbors - neighborMineCount - count_safe_revealed_neighbors(kb, dim, row,
                                                                                  col) == numUnrevealedNeighbors:
                markAllNeighborsSafe(kb, dim, row, col)
            # what if I don't add the mine's neighbors to fringe?
            fringe = addNeighborsToFringe(kb, dim, row, col, fringe)
            cleanFringe(check, fringe, kb, board, row, col, dim)
            revealAllSafe(kb, board, dim, fringe)

        if check:  # there's still a neighbor who I can check
            current = check.popitem()
            row = current[0][0]
            col = current[0][1]
        else:  # Must now randomly choose something from fringe, as I've exhausted all the conclusive elements
            # The trouble starts here, as the basic agent has zero way of figuring out probability
            # Add functionality for adv agent here
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
