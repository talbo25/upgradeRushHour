from Play_tools import Board
from State import State
from heapq import heappop as pop
from heapq import heappush as push
import math
import copy
from time import time


class Astar:

    def __init__(self, puzzle):
        curr_state = State(puzzle)
        self.first_node = Node(curr_state, 0)

        self.path = []
        self.path.append(self.first_node)

        self.d = dict()
        self.Open_dic = dict()
        self.Close_dic = dict()
        self.state_id = 1
        self.Close = []
        self.Open = []

    def open_push(self, node):
        key = node.F
        push(self.Open, (key, node))

    def open_pop(self):
        v = pop(self.Open)
        if v is None:
            return v

        return v[1]

    def close_push(self, node):
        key = node.F
        push(self.Close, (key, node))

    def remove_node(self, l, value):
        n = len(l)
        # Open heap:

        for i in range(0, n):
            if (l[i][1].name == value):
                l.pop(i)
                return

    def solve(self, max_time, _heuristic, DB):

        if _heuristic == 1:
            self.first_node.F = self.heuristic1(self.first_node.state)
        else:
            self.first_node.F = self.heuristic2(self.first_node.state)

        start = time()
        flag = 0
        # insert beginning of puzzle to Open
        self.open_push(self.first_node)
        self.Open_dic.update({self.first_node.name: self.first_node.F})

        while (self.Open) and (time()-start < max_time):
            curr_node = self.open_pop()
            res = DB.get_next(curr_node.state)
            if res == 0:
                continue
            if res != 1:
                while True:
                    self.close_push(curr_node)
                    self.Close_dic.update({curr_node.name: curr_node.F})
                    self.expand_from_DB(curr_node, _heuristic, res)
                    curr_node = self.open_pop()
                    res = DB.get_next(curr_node.state)
                    if res == 1:
                        flag = 1
                        break

            # check if solved
            if (flag == 1) or (curr_node.state.final_move()):
                # DONE:
                end = time()
                t = end - start
                result = [self.printSolutionHeap(curr_node, DB, flag), curr_node.depth + 1, t]
                return result

            # put node in CLOSED
            self.close_push(curr_node)
            self.Close_dic.update({curr_node.name: curr_node.F})

            # Expand node
            self.expand(curr_node, _heuristic)

        end = time()
        if not self.Open:
            print("Open empty; solution not found")

        result = None

        return result

    def expand(self, node, _heuristic):
        moves = node.moves
        n = len(moves)
        depth = node.depth

        curr_state = node.state

        if n == 0:
            print("Solution not found")
            return False

        for i in range(0, n):
            next_state = copy.deepcopy(curr_state)
            next_state.run_command(moves[i][-3:])
            s = next_state.get_string_board()
            if _heuristic == 1:
                h = self.heuristic1(next_state)
            else:
                h = self.heuristic2(next_state)

            f = h + depth + 1

            # CASE 1 : new state is neither in OPEN nor in CLOSE"""
            if (s not in self.Open_dic) and (s not in self.Close_dic):
                next_node = Node(next_state, depth + 1)
                next_node.F = f
                next_node.parent = node
                next_node.previous_move = moves[i]

                self.open_push(next_node)
                self.Open_dic.update({s: f})


            # CASE 2: next_state in OPEN and our value is better
            elif s in self.Open_dic:
                other_F = self.Open_dic.get(s)
                if other_F > f:
                    # DO: Repalce previous state with this state

                    # Create child node
                    next_node = Node(next_state, depth + 1)
                    next_node.F = f
                    next_node.parent = node
                    next_node.previous_move = moves[i]

                    # Replace nodes
                    self.remove_node(self.Open, s)
                    self.open_push(next_node)

                    # update dic
                    self.Open_dic.update({s: f})


            # CASE 3: next_state in CLOSE and our value is better
            elif s in self.Close_dic:
                other_F = self.Close_dic.get(s)
                if other_F > f:
                    next_node = Node(next_state, depth + 1)
                    next_node.F = f
                    next_node.parent = node
                    next_node.previous_move = moves[i]

                    self.remove_node(self.Close, s)
                    self.open_push(next_node)

                    self.Open_dic.update({s: f})
                    self.Close_dic.pop(s)

        return True

    def expand_from_DB(self, node, _heuristic, _command):
        depth = node.depth

        curr_state = node.state

        next_state = copy.deepcopy(curr_state)

        next_state.run_command(_command)
        s = next_state.get_string_board()

        if _heuristic == 1:
            h = self.heuristic1(next_state)
        else:
            h = self.heuristic2(next_state)

        f = h + depth + 1

        if (s not in self.Open_dic) and (s not in self.Close_dic):
            next_node = Node(next_state, depth + 1)
            next_node.F = f
            next_node.parent = node
            next_node.previous_move = s + _command

            self.open_push(next_node)
            self.Open_dic.update({s: f})

        return True

    def heuristic1(self, _state):  # this heuristic returns the number of blocked squares for the red car
        h = 0
        vehicle = _state.get_board().get_vehicle('X')
        x = int(vehicle.top_left / 6)
        y = vehicle.top_left % 6
        y = y + vehicle.get_length()

        for i in range(y, 6):
            if _state.get_string_board()[x * 6 + i] != '.':
                h += 1

        return h

    def heuristic2(self, _state):  # this heuristic returns the number of blocked squares for the red car + blocking car sizes
        h = 0

        vehicle = _state.get_board().get_vehicle('X')
        start_point = vehicle.top_left + vehicle.get_length()
        steps_to_end = 6 - ((vehicle.top_left + vehicle.get_length()) % 6)

        for i in range(0, steps_to_end+1):
            c = _state.get_string_board()[start_point + i]
            if c != '.':
                blocking_vehicle = _state.get_board().get_vehicle(c)
                h += blocking_vehicle.get_length() + 1

        return h

    def heuristic3(self, _state):  # 1
        h = 0
        vehicle = _state.get_board().get_vehicle('X')
        start_point = vehicle.top_left + vehicle.get_length()
        steps_to_end = 6 - (start_point % 6)
        for i in range(0, steps_to_end+1):
            c = _state.get_string_board()[start_point + i]
            if c != '.':
                blocking_vehicle = _state.get_board().get_vehicle(c)
                vehicle_len = blocking_vehicle.get_legth()
                if vehicle_len == 3:   # truck down
                    h += 5 - (blocking_vehicle.bottom_right/6)
                else:                   # car up
                    h += blocking_vehicle.top_left / 6

        return h

    def heuristic4(self, _state):  # 2
        h = 0
        vehicle = _state.get_board().get_vehicle('X')
        start_point = vehicle.top_left + vehicle.get_length()
        steps_to_end = 6 - (start_point % 6)
        for i in range(0, steps_to_end+1):
            c = _state.get_string_board()[start_point + i]
            if c != '.':
                blocking_vehicle = _state.get_board().get_vehicle(c)
                vehicle_len = blocking_vehicle.get_legth()
                if vehicle_len == 3:   # truck down
                    h += 5 - (blocking_vehicle.bottom_right/6)
                    for j in range(blocking_vehicle.bottom_right + 6, 36, 6):
                        c2 = _state.get_string_board()[j]
                        if c2 != '.':
                            h += 1
                else:                   # car up/down
                    h_up = 5 - (blocking_vehicle.bottom_right / 6)
                    for j in range(blocking_vehicle.bottom_right + 6, 36, 6):    # check down
                        c2 = _state.get_string_board()[j]
                        if c2 != '.':
                            h_up += 1
                    h_down = blocking_vehicle.top_left / 6
                    for j in range(blocking_vehicle.top_left - 6, -1, -6):    # check up
                        c2 = _state.get_string_board()[j]
                        if c2 != '.':
                            h_down += 1
                    h += h_up if h_up < h_down else h_down

        return h

    def updateDict(self, obj, key):
        if type(obj) is State:
            s = obj.boardToString()
        elif type(obj) is Node:
            s = obj.state.boardToString()
        else:
            print("UpdateDict: unknown object type")
            return False

        self.d.update({s: key})
        self.state_id += 1

    def printSolution(self):
        solution = ""
        i = self.path.__len__() - 1
        while i > 0:
            solution = self.path[i].previous_move[-3:] + " " + solution
            i -= 1

        return solution

    def printSolutionHeap(self, node, _DB, _flag):
        solution = ""
        ebf = 0
        head = copy.deepcopy(node)
        path = []
        if _flag == 0:
            next_move = self.set_final_move(head)
        else:
            mext_move = ""

        while node.parent is not None:
            if _flag == 0:
                _DB.set_next(node.state, next_move)
                next_move = node.previous_move[-3:]
            path.append(node)
            ebf += node.BF
            node = node.parent

        if _flag == 0:
            _DB.set_next(node.state, next_move)

        for i in range(0, len(path)):
            solution = path[i].previous_move[-3:] + " " + solution

        if head is None:
            print("HEAD NONE")

        if _flag == 0:
            solution = solution + " " + self.set_final_move(head)

        return solution

    def set_final_move(self, node):
        steps_to_end = 6 - (node.state.get_board().get_vehicle('X').bottom_right % 6)

        return "XR" + str(steps_to_end + 1)


class Node:

    # Build node
    def __init__(self, _state, _depth):

        self.state = _state
        self.name = _state.get_string_board()
        self.moves = self.state.find_next_steps()
        self.previous_move = None
        self.move_index = 0
        self.BF = len(self.moves)
        self.depth = _depth
        self.F = 0
        self.parent = None

    def __lt__(self, other):
        return self.F < other.F
