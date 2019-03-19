# from Play_tools import Vehicle, Board


def string_modify(_string, _index, _new_value):
    _string = _string[:_index] + _new_value + _string[_index + 1:]
    return _string


def string_switch(_string, _index1, _index2):
    helper = _string[_index1]
    _string = string_modify(_string, _index1, _string[_index2])
    _string = string_modify(_string, _index2, helper)
    return _string


def encode_board(_state):
    # 3 bit solution - 1. regular/special 2. H/V 3.2/3
    bin_state = ''
    for c in _state.get_string_board():
        first_bit = str(int(c == '.' or c == 'X'))
        if c != '.':
            second_bit = str(int(_state.get_board().get_vehicle(c).get_direction() == 'V'))
            third_bit = str(int(_state.get_board().get_vehicle(c).get_length() == 3))
        else:
            second_bit = '0'
            third_bit = '1'
        bin_state += first_bit + second_bit + third_bit
    dec_state = int(bin_state, 2)
    return dec_state


def encode_move(_state, _next):
    # get car RB index in binary
    # get direction U=00 D=01 L=10 R=11
    # get steps in binary
    e_vehicle_id = _state.get_board().get_vehicle(_next[0]).bottom_right
    e_vehicle_id = bin(e_vehicle_id)[2:]

    if _next[1] == 'U':
        e_direction = '00'
    elif _next[1] == 'D':
        e_direction = '01'
    elif _next[1] == 'L':
        e_direction = '10'
    else:
        e_direction = '11'

    steps = bin(int(_next[2]))[2:]
    steps = steps.zfill(3)

    bin_move = e_vehicle_id + e_direction + steps

    e_move = int(bin_move, 2)
    return e_move


def decode_move(_e_move, _boardobj):
    move = str(bin(_e_move)[2:]).zfill(11)
    vehicle_index = int(move[0:6], 2)
    vehicle_id = _boardobj.get_board()[vehicle_index]

    if move[6:8] == '00':
        direction = 'U'
    elif move[6:8] == '01':
        direction = 'D'
    elif move[6:8] == '10':
        direction = 'L'
    else:
        direction = 'R'

    steps = int(move[8:], 2)

    new_move = vehicle_id + direction + str(steps)
    return new_move
