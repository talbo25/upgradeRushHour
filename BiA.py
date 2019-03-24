from Play_tools import Board
from State import State
from heapq import heappop as pop
from heapq import heappush as push
import math
import copy
from time import time
from utils import *


class BiAstar:

    def __init__(self, _start, _end):
        self.startObj = _start
        self.endObj = _end
        self.start_nodes = dict()
        self.end_nodes = dict()
        self.final_steps= 0

        self.update_start_dict(self.startObj.first_node)
        self.update_end_dict(self.endObj.first_node)

    def update_start_dict(self, _new):
        self.start_nodes.update({_new.name: _new})

    def update_end_dict(self, _new):
        self.end_nodes.update({_new.name: _new})

    def initiate_first_node(self, _heuristic):
        if _heuristic == 1:
            self.startObj.first_node.F = self.startObj.heuristic1(self.startObj.first_node.state)
            self.endObj.first_node.F = self.endObj.heuristic1(self.endObj.first_node.state)
        elif _heuristic == 2:
            self.startObj.first_node.F = self.startObj.heuristic2(self.startObj.first_node.state)
            self.endObj.first_node.F = self.endObj.heuristic2(self.endObj.first_node.state)
        elif _heuristic == 3:
            self.startObj.first_node.F = self.startObj.heuristic3(self.startObj.first_node.state)
            self.endObj.first_node.F = self.endObj.heuristic3(self.endObj.first_node.state)
        else:
            self.startObj.first_node.F = self.startObj.heuristic4(self.startObj.first_node.state)
            self.endObj.first_node.F = self.endObj.heuristic4(self.endObj.first_node.state)

        # insert beginning of puzzle to Open
        self.startObj.open_push(self.startObj.first_node)
        self.startObj.Open_dic.update({self.startObj.first_node.name: self.startObj.first_node.F})

        self.endObj.open_push(self.endObj.first_node)
        self.endObj.Open_dic.update({self.endObj.first_node.name: self.endObj.first_node.F})

    def reverse_command(self, _com):
        if _com[1] == 'U':
            new_dir = 'D'
        elif _com[1] == 'D':
            new_dir = 'U'
        elif _com[1] == 'R':
            new_dir = 'L'
        else:
            new_dir = 'R'

        return _com[0] + new_dir + _com[2]

    def printSolutionHeap(self, flag, _sn, _en):
        solution = ""
        head = copy.deepcopy(_en)
        path = []

        if _sn.name != _en.name:
            if flag:
                _en = self.end_nodes[_sn.name]
            else:
                _sn = self.start_nodes[_en.name]
        else:
            if _sn.parent is not None:
                _sn = _sn.parent

        self.final_steps = _sn.depth + _en.depth
        self.final_steps += 1 if _sn.name == _en.name else 2

        while _sn.parent is not None:
            path.append(_sn)
            _sn = _sn.parent

        for i in range(0, len(path)):
            solution = path[i].previous_move[-3:] + " " + solution

        solution = solution + " connection "
        path = []
        while _en.parent is not None:
            path.append(_en)
            _en = _en.parent

        for i in range(0, len(path)):
            solution = solution + " " + self.reverse_command(path[i].previous_move[-3:])

        solution = solution + " " + self.startObj.set_final_move(head)

        return solution

    def check_if_done(self, flag, _sn, _en):
        if flag and (_sn.name in self.end_nodes.keys()):
            return True
        if (not flag) and (_en.name in self.start_nodes.keys()):
            return True

        return False

    def solve(self, max_time, _heuristic):
        self.initiate_first_node(_heuristic)

        start = time()
        flag = True
        s_curr_node = self.startObj.open_pop()
        e_curr_node = self.endObj.open_pop()
        while time() - start < max_time:

            # check if solved
            if self.check_if_done(flag, s_curr_node, e_curr_node):
                # DONE:
                end = time()
                t = end - start
                result = [self.printSolutionHeap(flag, s_curr_node, e_curr_node), self.final_steps, t]
                return result

            # put node in CLOSED
            if flag:
                self.startObj.close_push(s_curr_node)
                self.startObj.Close_dic.update({s_curr_node.name: s_curr_node.F})
            else:
                self.endObj.close_push(e_curr_node)
                self.endObj.Close_dic.update({e_curr_node.name: e_curr_node.F})

            # Expand node
            if flag:
                self.startObj.expand(s_curr_node, _heuristic, "start", self.start_nodes)
            else:
                self.endObj.expand(e_curr_node, _heuristic, "close", self.end_nodes)

            if self.startObj.Open and flag:
                s_curr_node = self.startObj.open_pop()
            elif self.endObj.Open:
                e_curr_node = self.endObj.open_pop()

            flag = not flag

        if not self.startObj.Open and not self.endObj.Open:
            print("Open empty; solution not found")

        result = None

        return result
