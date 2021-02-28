"""
Rutgers CS440-Intro to Artificial Intelligence
Project 2: Minesweeper solver

Authors: Siddhi Kasera, Em Shi
"""

# TODO: Implement the Basic Agent, Implement the Advanced Agent, set up testing script, set up graphing script
# I may want to return a tuple for the AI agents (number of unrevealed mines , total number of mines) for graph purposes

from generate_board import *
from manual_agent import *
from knowledge_base import *
from basic_agent import *

d = input("What is the square dimensions of the mine field? ")
n = input("How many mines do you want to put in the field? ")
board = generate_board(int(d), int(n))
print_init_mine = input("Would you like to print the mine field? Y/N (if you want to play manually, I recommend typing in 'N') ")
if print_init_mine == 'Y' or print_init_mine == 'y' or print_init_mine == 'Yes':
    print_board(board)
    print("\n")

kb = generate_knowledge_base(int(d))
print_knowledge_base(kb)

agent = input("Select the agent you want to use, M for manual (player controlled), B for basic, or A for advanced: ")
if agent == 'M' or agent == 'm' or agent == 'manual':
    play_minesweeper(board, kb, int(d), int(n))

if agent == 'B' or agent == 'b' or agent == 'basic':
    basic_agent(board, int(d), kb, n)

print("Exiting the program")