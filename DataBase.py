from State import State
from Play_tools import Board, Vehicle
from utils import *


class DataBase:
    def __init__(self):
        self.Encoded_States = {}

    def get_dict(self):
        return self.Encoded_States

    def add(self, _new_encoded):
        self.Encoded_States[_new_encoded] = 0

    def set_next(self, _state, _next):
        e_state = encode_board(_state)
        e_move = encode_move(_state, _next)
        self.Encoded_States[e_state] = e_move

    def get_next(self, _state):
        # check if in dict
        # if not -> add(_state) -> return 1 (expand)
        # else get next
        # if 0 -> return 0 (dead end)
        # else decode next nove and make it relevant to _state -> return next
        e_state = encode_board(_state)
        if e_state not in self.Encoded_States:
            self.add(e_state)
            return 1

        if self.Encoded_States[e_state] == 0:
            return 0

        d_move = decode_move(self.Encoded_States[e_state], _state.get_board())

        return d_move
