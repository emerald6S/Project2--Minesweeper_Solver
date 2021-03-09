# TODO:
# -- Do basic agent up to the point where I must randomly choose a new point
# -- The fun starts when I have run out of things in check (no cells where, taken alone, I can conclusively decide is safe or not).
# -- 1. Do a proof by contradiction foe each cell in fringe where I assume that the unrevealed space is a mine. If the board's information becomes incorrect, then that space must be safe safe
# -- 2. If the attempted proofs by contradiction fails to detect a safe cell, then create all possible mine configs. Obviously throw away any solution that makes the board incorrect
# -- 3. Now compare all the mine position configs. Reveal the space that has the least number of configs that mark it as a mine. In the case of a tie, choose randomly
#
# Potential time saver: if the fringe isn't contiguous, then I may split it
import gc
import itertools

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
        print("Checking element: (" + str(row) + ", " + str(col) + ")")
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

                if neighborMineCount - numRevealedMineNeighbors == numUnrevealedNeighbors:
                    markAllNeighborsDangerous(kb, dim, row, col)
                elif numNeighbors - neighborMineCount - count_safe_revealed_neighbors(kb, dim, row,
                                                                                      col) == numUnrevealedNeighbors:
                    markAllNeighborsSafe(kb, dim, row, col)

                fringe = addNeighborsToFringe(kb, dim, row, col, fringe)

            if p:
                print("-----------------")
                print("Current element: (" + str(row) + ", " + str(col) + ")")
                print("Contents are: " + kb[row][col])
                display_array(kb, dim, row, col)

        cleanFringe(check, fringe, kb, board, row, col, dim)
        check = cleanCheck(check, kb, dim)
        safe = hasSafe(kb, dim)

        #########
        if safe:  # there's safe cells I can reveal
            if p:
                print("-----------------")
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
                            print("-----------------")
                            print("By proof of contradiction, element (" + str(key[0]) + ", " + str(
                                key[1]) + ") should NOT be mine")
                        kb = reveal_space(kb, board, key[0], key[1], False, False)
                        flag_proof = True
                        break
            if not flag_proof:  # Failed proof by contradiction, do probability
                keys = list(fringe.keys())
                if keys:
                    x = len(keys)
                    permutations = generateAllBinaryStrings(x)
                    fringeCopies = []
                    for permutation in permutations:
                        fringeCopies = generateMineFromPermutation(kb, dim, check, fringe, permutation, fringeCopies)
                    fringeSpaceCount = getLeastMines(fringe, fringeCopies)
                    leastMines = min(fringeSpaceCount.values())
                    leastKeys = [key for key in fringeSpaceCount if fringeSpaceCount[key] == leastMines]
                    if len(leastKeys) == 1:
                        if p:
                            print("-----------------")
                            print("Element (" + str(leastKeys[0][0]) + ", " + str(
                                leastKeys[0][1]) + ") has lowest chance of being a mine")
                            print("Contents are actually: " + kb[row][col])
                        reveal_space(kb, board, leastKeys[0][0], leastKeys[0][1], dim, False, True)
                    elif len(leastKeys) > 1:
                        randomKey = random.choice(leastKeys)
                        row = randomKey[0]
                        col = randomKey[1]
                        kb = reveal_space(kb, board, row, col, dim, False, True)
                        if p:
                            print("-----------------")
                            print("Probability, chose: (" + str(row) + ", " + str(col) + ")")
                            print("Contents are actually: " + kb[row][col])

                else:
                    if p:
                        print("No fringe left, choosing randomly now")
                    unrevealed = getAllUnrevealedInKB(kb, dim)
                    keys = list(unrevealed.keys())
                    randomKey = random.choice(keys)
                    unrevealed.pop(randomKey)
                    row = randomKey[0]
                    col = randomKey[1]
                    kb = reveal_space(kb, board, row, col, dim, False, True)
                    if p:
                        print("-----------------")
                        print("Randomly chosen element: (" + str(row) + ", " + str(col) + ")")
                        print("Contents are: " + kb[row][col])


    if p:
        print("-----------------")
        print_knowledge_base(kb)
    sol = isAutoSolved(kb, n)
    gc.collect()
    return sol


#################################################
# HELPER FUNCTIONS
#################################################

def proofByContradiction(kb, dim, check: dict, k):
    """
    Performs a proof by contradiction on the selected fringe key (doesn't accept fringe as input)
    This function will assume that the key is a mine, and create a copy of the kb except update the key so that it's a mine
    If at least 1 element in the check changes due to the new information, return True and reveal this cell
    Else return false

    :param kb:
    :param dim:
    :param check:
    :param k: A tuple, the key of the cell I want to see if is mine or not
    :return: boolean, true if proven to be safe and false otherwise
    """
    kbClone = deepcopy(kb)  # I only should edit this one
    kbClone[k[0]][k[1]] = 'D'
    checkClone = {}

    # Change the copy of the knowledge base to reflect the assumption
    for key in list(check):
        row = key[0]
        col = key[1]
        if kbClone[row][col] != 'M' or kbClone[row][col] != 'D':
            numUnrevealedNeighbors = count_unrevealed_neighbors(kbClone, dim, row, col)
            numRevealedMineNeighbors = count_revealed_mine_neighbors(kbClone, dim, row, col)
            numNeighbors = count_neighbors(kbClone, dim, row, col)
            if kbClone[row][col] == 'C':
                neighborMineCount = 0
            else:
                neighborMineCount = int(kbClone[row][col])

            if neighborMineCount - numRevealedMineNeighbors == numUnrevealedNeighbors:
                markAllNeighborsDangerous(kbClone, dim, row, col)
            elif numNeighbors - neighborMineCount - count_safe_revealed_neighbors(kbClone, dim, row,
                                                                                  col) == numUnrevealedNeighbors:
                markAllNeighborsSafe(kbClone, dim, row, col)

    kbClone = updateMineNeighbors(kbClone, dim)
    for key in list(check):
        checkClone[key] = kbClone[key[0]][key[1]]
    del kbClone
    if check == checkClone:
        return False
    else:
        return True


def updateMineNeighbors(kb, dim):
    """
    Update mine neighbors based on what has been revealed. If a neighbor is hidden, do not change what has been revealed

    :param kb:
    :param dim:
    :return: the updated kb
    """
    for row in range(dim):
        for col in range(dim):
            if kb[row][col] != "?" and kb[row][col] != 'D' and kb[row][col] != 'M' and kb[row][col] != 'S':
                neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
                mineCount = 0
                hasChanged = True
                for i in range(len(neighbors)):
                    if isValid(kb, dim, row + neighbors[i][0], col + neighbors[i][1]):
                        if kb[row + neighbors[i][0]][col + neighbors[i][1]] == '?':
                            hasChanged = False
                            break
                        elif kb[row + neighbors[i][0]][col + neighbors[i][1]] == 'M' or kb[row + neighbors[i][0]][
                            col + neighbors[i][1]] == 'D':
                            mineCount = mineCount + 1
                if hasChanged:
                    kb[row][col] = str(mineCount)

    return kb


def generateAllBinaryStrings(n):
    """
    Generate all binary strings up to length n

    :param n:
    :return:
    """
    result = []
    k = 0
    while k <= n:
        for bits in itertools.combinations(range(n), k):
            s = ['0'] * n
            for b in bits:
                s[b] = '1'
            result.append("".join(s))
            del s
        k = k + 1
    return result


def generateMineFromPermutation(kb, dim, check, fringe, permutation, fringeCopies):
    """
    From given permutations, update a copy of kb: 0 is safe and 1 is mine
    Generate a new fringe and check based off this information
    If check == checkClone, add new fringe to fringeCopies

    :param kb:
    :param dim:
    :param check:
    :param fringe:
    :param permutation:
    :param fringeCopies:
    :return: Update fringeCopies
    """
    kbClone = deepcopy(kb)
    checkClone = {}
    fringeClone = {}
    i = 0
    for key in fringe:
        if permutation[i] == '1':
            fringeClone[key] = 'D'
        else:
            fringeClone[key] = 'S'
        kbClone[key[0]][key[1]] = fringeClone[key]

    kbClone = updateMineNeighbors(kbClone, dim)

    for key in list(check):
        checkClone[key] = kbClone[key[0]][key[1]]

    if check == checkClone: # If checkClone is wrong, throw it away
        fringeCopies.append(checkClone)
    del kbClone
    return fringeCopies


def getLeastMines(fringe, fringeCopies):
    """
    From fringe copies, select the spaces that have the least amount of mines in them

    :param fringe
    :param fringeCopies:
    :return: A dict of spaces
    """
    fringeSpaces = deepcopy(fringe)
    for space in fringeSpaces:
        mineCount = 0
        for i in fringeCopies:
            if fringeCopies[i][space] == 'D':
                mineCount = mineCount + 1
        fringeSpaces[space] = mineCount

    return fringeSpaces