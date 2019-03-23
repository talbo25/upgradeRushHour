from Play_tools import Vehicle, Board
import math
from utils import string_modify, string_switch


class State:
    def __init__(self, _board_obj):
        self.board_state = _board_obj
        self.e_version = None

    def get_string_board(self):
        return self.board_state.get_board()

    def get_board(self):
        return self.board_state

    def find_next_steps(self):
        board = self.board_state.get_board()
        side = int(math.sqrt(len(board)))
        next_states = []

        # check horizontal
        for i in range(0, (len(board)), side):  # run over rows
            j = 0
            while j < side:  # run over columns
                p = i + j  # set p as position on board
                if board[p] == '.':  # empty square
                    j += 1
                    continue
                if self.board_state.get_vehicle(board[p]).get_direction() == 'V':  # check if vertical
                    j += 1
                    continue

                v_len = self.board_state.get_vehicle(board[p]).get_length()

                # check right
                steps = 0
                temp_state = board
                p_next = p + 1
                while (p_next % side != 0) and (p_next < len(board)) and (board[p_next] == '.'):
                    temp_state = string_switch(temp_state, p_next, p - (v_len - 1))
                    steps += 1
                    next_states.append(temp_state + ',' + temp_state[p] + 'R' + str(steps))
                    p = p_next
                    p_next += 1
                    j += 1

                p = i+j  # set p as position on board
                if (p >= len(board)) or \
                        (board[p] == '.') or \
                        (self.board_state.get_vehicle(board[p]).get_direction() == 'V'):  # check if vertical
                    j += 1
                    continue
                # check left
                temp_state = board
                p_next = p - 1
                steps = 0
                while (p_next % side != side - 1) and (board[p_next] == '.'):
                    temp_state = string_switch(temp_state, p_next, p + (v_len - 1))
                    steps += 1
                    next_states.append(temp_state + ',' + temp_state[p] + 'L' + str(steps))
                    p = p_next
                    p_next -= 1
                j += 1

        # check vertical
        for i in range(0, side):  # run over columns
            j = 0
            while j < len(board):  # run over rows
                p = i + j  # set p as position on board
                if board[p] == '.':  # empty square
                    j += side
                    continue
                if self.board_state.get_vehicle(board[p]).get_direction() == 'H':  # check if horizontal
                    j += side
                    continue

                v_len = self.board_state.get_vehicle(board[p]).get_length()

                # check down
                temp_state = board
                steps = 0
                p_next = p + side
                while (p_next < len(board)) and (board[p_next] == '.'):
                    temp_state = string_switch(temp_state, p_next, p - ((v_len - 1)*side))
                    steps += 1
                    next_states.append(temp_state + ',' + temp_state[p] + 'D' + str(steps))
                    p = p_next
                    p_next += side
                    j += side

                p = i+j  # set p as position on board

                if (p >= len(board)) or \
                        (board[p] == '.') or \
                        (self.board_state.get_vehicle(board[p]).get_direction() == 'H'):  # check if horizontal
                    j += side
                    continue
                # check up
                temp_state = board
                p_next = p - side
                steps = 0
                while (p_next >= 0) and (board[p_next] == '.'):
                    temp_state = string_switch(temp_state, p_next, p + ((v_len - 1)*side))
                    steps += 1
                    next_states.append(temp_state + ',' + temp_state[p] + 'U' + str(steps))
                    p = p_next
                    p_next -= side
                j += side

        return next_states

    def get_new_blocked(self, _parent_state, _command):
        vehicle = _command[-3]
        com_direction = _command[-2]
        steps = int(_command[-1])
        v_direction = self.get_board().get_vehicle(vehicle).direction
        s_board = self.get_string_board()

        if (com_direction == 'R') or (com_direction == 'D'):  # bottom-right new index
            start_index = self.get_board().get_vehicle(vehicle).bottom_right
        else:  # top-left new index
            start_index = self.get_board().get_vehicle(vehicle).top_left

        counter = 0

        if v_direction == 'H':
            run = start_index
            # check left
            while run % 6 != 5:
                if (s_board[run] != '.') and (s_board[run] != vehicle):  # found
                    if self.get_board().get_vehicle(s_board[run]).direction == 'H':
                        counter += 1
                    break
                run -= 1

            run = start_index
            # check right
            while run % 6 != 0:
                if (s_board[run] != '.') and (s_board[run] != vehicle):  # found
                    if self.get_board().get_vehicle(s_board[run]).direction == 'H':
                        counter += 1
                    break
                run += 1
        else:
            run = start_index
            # check up
            while run >= 0:
                if (s_board[run] != '.') and (s_board[run] != vehicle):  # found
                    if self.get_board().get_vehicle(s_board[run]).direction == 'V':
                        counter += 1
                    break
                run -= 6

            run = start_index
            # check down
            while run < 36:
                if (s_board[run] != '.') and (s_board[run] != vehicle):  # found
                    if self.get_board().get_vehicle(s_board[run]).direction == 'V':
                        counter += 1
                    break
                run += 6

        while steps > 0:
            if v_direction == 'H':
                run = start_index
                # check up
                while run >= 0:
                    if (s_board[run] != '.') and (s_board[run] != vehicle):  # found
                        if self.get_board().get_vehicle(s_board[run]).direction == 'V':
                            counter += 1
                        break
                    run -= 6

                run = start_index
                # check down
                while run < 36:
                    if (s_board[run] != '.') and (s_board[run] != vehicle):  # found
                        if self.get_board().get_vehicle(s_board[run]).direction == 'V':
                            counter += 1
                        break
                    run += 6
            else:
                run = start_index
                # check left
                while run % 6 != 5:
                    if (s_board[run] != '.') and (s_board[run] != vehicle):  # found
                        if self.get_board().get_vehicle(s_board[run]).direction == 'H':
                            counter += 1
                        break
                    run -= 1

                run = start_index
                # check right
                while run % 6 != 0:
                    if (s_board[run] != '.') and (s_board[run] != vehicle):  # found
                        if self.get_board().get_vehicle(s_board[run]).direction == 'H':
                            counter += 1
                        break
                    run += 1
            steps -= 1

        return counter

    def final_move(self):
        vehicle = self.board_state.get_vehicle('X')
        start_point = vehicle.top_left + vehicle.get_length()
        steps_to_end = 6 - ((vehicle.top_left + vehicle.get_length()) % 6)

        for i in range(0, steps_to_end):
            if self.get_string_board()[start_point+i] != '.':
                return False

        return True

    def run_command(self, _command):
        if len(_command) != 3:
            print("-E- Wrong command length")

        self.board_state.update_board(_command)
        self.BF = len(self.find_next_steps())


