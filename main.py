"""
Rutgers CS440-Intro to Artificial Intelligence
Project 2: Minesweeper solver

Authors: Siddhi Kasera, Em Shi
"""

# Return a tuple for the AI agents (number of unrevealed mines , total number of mines) for mathplotlib purposes
import gc
import time
import sys

from adv_agent import *
from auto_test import automate_test
from generate_board import *
from manual_agent import *
from knowledge_base import *
from basic_agent import *

auto = input("First, select if you want to automate a lot of test cases: Y/N: ")
if auto == "Y" or auto == "y" or auto == "yes" or auto == "automate":
    automate_test()

else:
    d = input("What is the square dimensions of the mine field? ")
    n = input("How many mines do you want to put in the field? ")
    board = generate_board(int(d), int(n))
    print_init_mine = input(
        "Would you like to print the mine field? Y/N (if you want to play manually, I recommend typing in 'N') ")
    if print_init_mine == 'Y' or print_init_mine == 'y' or print_init_mine == 'Yes':
        print_board(board)
        print("\n")

    kb = generate_knowledge_base(int(d))

    agent = input(
        "Select the agent you want to use, M for manual (player controlled), B for basic, or A for advanced: ")
    if agent == 'M' or agent == 'm' or agent == 'manual':
        play_minesweeper(board, kb, int(d), int(n))

    if agent == 'B' or agent == 'b' or agent == 'basic':
        print_final_kb = input("Would you like to print output? Y/N ")
        if print_final_kb == 'Y' or print_final_kb == 'y' or print_final_kb == 'Yes':
            high_score = basic_agent(board, kb, int(d), int(n), True)
            print("High score: " + str(high_score[0]) + " / " + str(high_score[1]) + " mines dodged")
        else:
            start = time.time()
            high_score = basic_agent(board, kb, int(d), int(n))
            end = time.time()
            print("High score: " + str(high_score[0]) + " / " + str(high_score[1]) + " mines dodged")
            print("Elapsed time: ", end-start, " s")

    elif agent == "A" or agent == 'a' or agent == 'advanced':
        print_final_kb = input("Would you like to print output? Y/N ")
        if print_final_kb == 'Y' or print_final_kb == 'y' or print_final_kb == 'Yes':
            high_score = adv_agent(board, kb, int(d), int(n), True)
            print("High score: " + str(high_score[0]) + " / " + str(high_score[1]) + " mines dodged")
        else:
            start = time.time()
            high_score = adv_agent(board, kb, int(d), int(n))
            end = time.time()
            print("High score: " + str(high_score[0]) + " / " + str(high_score[1]) + " mines dodged")
            print("Elapsed time: ", end - start, " s")

print("Exiting the program")
sys.exit()
