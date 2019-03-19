from Play_tools import Vehicle, Board
from State import State
from Astar import Astar
from DataBase import DataBase
from time import time
import hashlib
from collections import defaultdict
from heapq import heappush as push
from heapq import heappop as pop


def RUN(_time, _heuristic):
    total_time = 0
    count = 0
    total_steps = 0
    i = 1

    my_DBs = {}
    with open("puzzles.txt") as fh:
        puzzle = fh.readline()
        while puzzle:
            p = Board(puzzle.rstrip('\n'))
            n = len(p.VehicleHash)
            if n not in my_DBs:
                my_DBs[n] = DataBase()

            AObj = Astar(p)
            results = AObj.solve(_time, _heuristic, my_DBs[n])

            if results is None:
                print("-E- Could not solve puzzle number ", i, " due to time limit\n"
                      "==========================================")

            else:
                solution_path = results[0]
                steps = results[1]
                current_time = results[2]

                print("For puzzle number ", i, ":\n"
                      "Time - ", current_time, "\n"
                      "Steps - ", steps, "\n"
                      "Solution path - ", solution_path, "\n"
                      "==========================================")

                total_time += current_time
                count += 1
                total_steps += steps
            i += 1
            puzzle = fh.readline()
        fh.close()

    print("==========================================\n"
          "SUMMARY\n"
          "Solved ", count, " out of ", i - 1, " puzzles with heuristic number ", _heuristic, " with time limit of  ",_time, "\n"
          "Total time - ", total_time, "\n"
           "Average time for one puzzle - ", total_time / count, "\n"
           "Average steps for one puzzle - ", total_steps / count, "\n")


RUN(20, 2)
