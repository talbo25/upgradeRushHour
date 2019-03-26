from Play_tools import Vehicle, Board
from State import State
from Astar import Astar
from IDAstar import IDAstar
from BiA import BiAstar
from DataBase import DataBase
from time import time
import hashlib
from collections import defaultdict
from heapq import heappush as push
from heapq import heappop as pop


def RUN(_time, _heuristic, option=1):
    total_time = 0
    count = 0
    total_steps = 0
    i = 1
    fh2 = open("solutions.txt", "r")
    my_DBs = {}
    with open("puzzles.txt") as fh:
        puzzle = fh.readline()
        while puzzle:
            p = Board(puzzle.rstrip('\n'))
            n = len(p.VehicleHash)
            if n not in my_DBs:
                my_DBs[n] = DataBase()

            if option == 1:
                AObj = Astar(p)
                results = AObj.solve(_time, _heuristic, my_DBs[n])
            elif option == 2:
                IDAObj = IDAstar(p)
                results = IDAObj.solve(_time, _heuristic, my_DBs[n])
            else:
                Astart = Astar(p)
                sol = fh2.readline()
                p = Board(sol.rstrip('\n'))
                Aend = Astar(p)
                BiObj = BiAstar(Astart, Aend)
                results = BiObj.solve(_time, _heuristic)

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
                                                                                           "Solution path - ",
                      solution_path, "\n"
                                     "==========================================")

                total_time += current_time
                count += 1
                total_steps += steps
            i += 1
            puzzle = fh.readline()
        fh.close()

    print("==========================================\n"
          "SUMMARY\n"
          "Solved ", count, " out of ", i - 1, " puzzles with heuristic number ", _heuristic, " with time limit of  ",
          _time, "\n"
                 "Total time - ", total_time, "\n"
                                              "Average time for one puzzle - ", total_time / count, "\n"
                                                                                                    "Average steps for one puzzle - ",
          total_steps / count, "\n")


def printAllStats(_time, _heuristic, option=1):
    i = 1
    fh2 = open("solutions.txt", "r")
    my_DBs = {}
    EBF = 0
    depth_ratio = 0
    avg_h = 0
    tree_depth = [0, 0, 0]
    puzzles = 40
    avg_n = 0
    with open("puzzles.txt") as fh:
        puzzle = fh.readline()
        while puzzle:
            p = Board(puzzle.rstrip('\n'))
            n = len(p.VehicleHash)
            if n not in my_DBs:
                my_DBs[n] = DataBase()

            if option == 1:
                AObj = Astar(p)
                S = AObj.solve(_time, _heuristic, my_DBs[n])
            elif option == 2:
                IDAObj = IDAstar(p)
                S = IDAObj.solve(_time, _heuristic, my_DBs[n])
            else:
                Astart = Astar(p)
                sol = fh2.readline()
                p = Board(sol.rstrip('\n'))
                Aend = Astar(p)
                BiObj = BiAstar(Astart, Aend)
                S = BiObj.solve(_time, _heuristic, True)

            # S:
            # [ebf, d/N ratio, average h, tree depth, N  time]
            #   0       1           2         3       4    5

            ebf = S[0]
            dN = S[1]
            h = S[2]
            depth = S[3]
            t = S[5]
            N = S[4]
            if (t > _time):
                status = 'Failed'
            else:
                status = 'Solved'

            print("Statistics for puzzle:  ", i )
            print("Status: " + status)
            print("Time : ", t)
            print("EBF: ", ebf)
            print("Average Heuristic: ", h)
            print("depth ratio (d/N): ", dN)
            print("Number of nodes searched: ", N)
            print("Minimum depth: ", depth[0], " Average Depth: ", depth[1], "Max Depth: ", depth[2])
            EBF += ebf
            depth_ratio += dN
            avg_h += h
            avg_n += N
            tree_depth[0] += depth[0]
            tree_depth[1] += depth[1]
            tree_depth[2] += depth[2]
            i += 1
            puzzle = fh.readline()
        fh.close()

    tree_depth[0] = tree_depth[0] / puzzles
    tree_depth[1] = tree_depth[1] / puzzles
    tree_depth[2] = tree_depth[2] / puzzles
    EBF = EBF / puzzles
    avg_h = avg_h / puzzles
    depth_ratio = depth_ratio / puzzles
    avg_n = avg_n / puzzles

    print("================================")
    print("Average Totals for: " + str(_heuristic))
    print("Total EBF: ", EBF)
    print("Total Heuristic Average: ", avg_h)
    print("Total depth ratio (d/N): ", depth_ratio)
    print("Total Nodes (N): ", avg_n)
    print("Total Min search depth: ", tree_depth[0])
    print("Total Average search depth: ", tree_depth[1])
    print("Total Max search depth: ", tree_depth[2])


# RUN(200, 2, 3)
printAllStats(200, 2, 3)
