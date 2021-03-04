# TODO:
# -- Randomly choose the first space as usual, except this time I can reveal safe neighbors as I'm free from the block by block requirement
# -- For each revealed or marked cell that has a neighbor cell that's not revealed, add the neighbor cell to the fringe and the revealed cell to check
# This is where the loop starts:
# While board not solved:
# -- For each cell in check, repeat the first 2 tests in the basic agent to determine if all neighbors should be safe or mines
# -- If the revealed contents aren't a mine, then perform addToFringe, cleanFringe, and updateAllSafe
# -- The fun starts when I have run out of things in check (no cells where, taken alone, I can conclusively decide is safe or not)
# -- 1. Do a proof by contradiction foe each cell in fringe where I assume that the unrevealed space is a mine. If the board's information becomes incorrect, then that space must be safe safe
# -- 2. If the attempted proof by contradiction fails to detect a safe cell, then create all possible mine configs. Obviously throw away any solution that makes the board incorrect
# -- 3. Now compare all the mine position configs. Reveal the space that has the least number of configs that mark it as a mine. In the case of a tie, choose randomly
#
# Potential time saver: if the fringe isn't contiguous, then I may split it

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
    return
