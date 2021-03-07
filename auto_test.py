import sys

import matplotlib.pyplot as plt

from adv_agent import adv_agent
from basic_agent import *
from generate_board import generate_board


# TODO: After advanced agent is implemented, give option to print both agents' data on the same plot

def automate_test():
    print("AUTOMATED TESTING SCRIPT")

    agent = input("Select the agent you want to use: B for basic, A for advanced, or All for both: ")
    strategy = ""
    if agent == 'B' or agent == 'b' or agent == 'basic':
        strategy = "Basic"
    elif agent == "A" or agent == 'a' or agent == 'advanced':
        strategy = "Advanced"
    elif agent == "All" or agent == 'all' or agent == 'Both' or agent == 'both':
        strategy = "All"
    else:
        print("Invalid strategy")

    if strategy == 'Basic' or strategy == 'Advanced' or strategy == 'All':
        d = input("What is the square dimensions of the mine field? ")
        print("There's " + str(int(d)*int(d) ) + " spaces total")
        min_density = input("What is the LOWEST number of mines you want to put in the field? ")
        max_density = input("What is the HIGHEST number of mines you want to put in the field? ")
        num_attempts = input("How many attempts for each density? ")
        file_name = input("Input the name of the file you want to store the raw output, and remember extensions:\n")
        print("Starting tests...")

        scoresBasic = []  # This stores high score of basic
        xBasic = []  # This stores mine density of basic
        yBasic = []  # This stores high score of basic in fraction form

        scoresAdv = [] # This scores high score of advanced
        xAdv = []  # This stores mine density of advanced
        yAdv = []  # This stores high score of advanced in fraction form
        a = int(min_density)
        i = 1
        j = 1

        orig_stdout = sys.stdout
        f = open(file_name, "w")
        sys.stdout = f
        print("AUTOMATED TEST RESULT DATA")
        print("Credits: Siddhi Kasera and Em Shi")
        print("Dimension of:", d)
        print("Min density: ", min_density)
        print("Max density: ", max_density)
        print("----------------------------")

        while a <= int(max_density):
            board = generate_board(int(d), a)
            kb = generate_knowledge_base(int(d))
            if strategy == "Basic":
                high_score = basic_agent(board, kb, int(d), a)
                print("Basic agent attempt ", i)
                print("Density ", a)
                print("High score: " + str(high_score[0]) + " / " + str(high_score[1]) + " mines dodged\n")
                scoresBasic.append(high_score[0])
                xBasic.append(high_score[1])
                yBasic.append(high_score[0] / high_score[1])

            elif strategy == "Advanced":
                high_score = adv_agent(board, kb, int(d), a)
                print("Advanced agent attempt ", i)
                print("Density ", a)
                print("High score: " + str(high_score[0]) + " / " + str(high_score[1]) + " mines dodged\n")
                scoresAdv.append(high_score[0])
                xAdv.append(high_score[1])
                yAdv.append(high_score[0] / high_score[1])

            elif strategy == "All":
                high_score = basic_agent(board, kb, int(d), a)
                print("Basic agent attempt ", i)
                print("Density ", a)
                print("High score: " + str(high_score[0]) + " / " + str(high_score[1]) + " mines dodged\n")
                scoresBasic.append(high_score[0])
                xBasic.append(high_score[1])
                yBasic.append(high_score[0] / high_score[1])

                high_score2 = adv_agent(board, kb, int(d), a)
                print("Advanced agent attempt ", i)
                print("Density ", a)
                print("High score: " + str(high_score2[0]) + " / " + str(high_score2[1]) + " mines dodged\n")
                scoresAdv.append(high_score2[0])
                xAdv.append(high_score2[1])
                yAdv.append(high_score2[0] / high_score2[1])

            j = j + 1
            i = i + 1
            if j > int(num_attempts):
                j = 1
                a = a + 1

        if yBasic:
            print("scoresBasic: ", scoresBasic)
            print("xBasic = ", xBasic)
            print("yBasic = ", yBasic)
            print("\n")
        if yAdv:
            print("scoresAdv: ", scoresAdv)
            print("xAdv = ", xAdv)
            print("yAdv = ", yAdv)
            print("\n")
        print("End of raw data")

        if yBasic:
            maxB = max(scoresBasic)
            print("Most mines dodged for basic agent: ", maxB)
            max_indexB = scoresBasic.index(maxB)
            print("This happened at density ", xBasic[max_indexB])
        if yAdv:
            maxA = max(scoresAdv)
            print("Most mines dodged for advanced agent: ", maxA)
            max_indexA = scoresAdv.index(maxA)
            print("This happened at density ", xAdv[max_indexA])

        sys.stdout = orig_stdout
        f.close()

        if strategy == "Basic" and yBasic:
            print("Now creating a scatter plot for the basic agent:")
            plt.scatter(xBasic, yBasic, label="density_vs_highScore", color='red', alpha=0.5)
            plt.xlabel("Mine density")
            plt.ylabel("Fraction of dodged mines")
            plt.title(strategy + " Agent")
            plt.legend(["Basic agent"], loc = "best")
            plt.show()

        if strategy == "Advanced":
            print("Now creating a scatter plot for the advanced agent:")
            plt.scatter(xAdv, yAdv, label="density_vs_highScore", color='green', alpha=0.5)
            plt.xlabel("Mine density")
            plt.ylabel("Fraction of dodged mines")
            plt.title(strategy + " Agent")
            plt.legend(["Advanced agent"], loc="best")
            plt.show()

        if strategy == "All":
            print("Now creating a scatter plot for both agents:")
            plt.scatter(xBasic, yBasic, label="density_vs_highScore", color='red', alpha=0.5)
            plt.scatter(xAdv, yAdv, label="density_vs_highScore", color='green', alpha=0.5)
            plt.xlabel("Mine density")
            plt.ylabel("Fraction of dodged mines")
            plt.title("All Agents")
            plt.legend(["Basic", "Advanced"], loc="best")
            plt.show()

    return
