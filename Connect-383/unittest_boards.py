"""
Central storage for the test boards needed for the private tests.
"""


def convert_string_to_board(s):
    """
    Convert a string to the respective board representation,
    ignoring extra whitespaces.
    Rows should be newline delimited, while spaces between pieces in each row
    should be space delimited.
    """

    conversion_dict = {
        'O': -1,
        'X': 1,
        '-': 0,
        '#': -2
    }

    # preventing misplaced o and x instead of O and X from causing issues
    s = s.upper()
    board = []

    for line in reversed(s.split('\n')):
        # ignore extra white spaces
        line = line.strip()
        # ignore blank lines
        if line == "":
            continue

        row = [conversion_dict[space] for space in line.split(' ')]
        board.append(row)

    return board


def generate_test_boards_basic():
    """
    Return a bunch of boards with predetermined utility.
    """

    b_sure_win_1 = {
        "desc": "X for sure wins by 18",
        "board": convert_string_to_board("""
            # O - -
            # X X -
            # X X O
            O O # #
        """),
        "utility": 18,
    }

    b_sure_win_2 = {
        "desc": "X for sure wins by 18",
        "board": [list(reversed(row)) for row in b_sure_win_1["board"]],
        "utility": 18,
    }

    b_sure_win_3 = {
        "desc": "O for sure wins by 18",
        "board": convert_string_to_board("""
            # X - -
            # O O -
            X O O X
            X X # #
        """),
        "utility": -18,
    }

    b_sure_win_4 = {
        "desc": "O for sure wins by 18",
        "board": [list(reversed(row)) for row in b_sure_win_3["board"]],
        "utility": -18,
    }

    b_sure_lose_1 = {
        "desc": "X for sure loses by 14",
        "board": convert_string_to_board("""
            O O O -
            X O X -
            X O X -
            X O X -
        """),
        "utility": -14,
    }

    b_sure_lose_2 = {
        "desc": "X for sure loses by 14",
        "board": [list(reversed(row)) for row in b_sure_lose_1["board"]],
        "utility": -14,
    }

    b_sure_lose_3 = {
        "desc": "O for sure loses by 23",
        "board": convert_string_to_board("""
            X X X -
            O X O -
            O X O -
            # X O -
        """),
        "utility": 23,
    }

    b_sure_lose_4 = {
        "desc": "O for sure loses by 23",
        "board": [list(reversed(row)) for row in b_sure_lose_3["board"]],
        "utility": 23,
    }

    return [
        b_sure_win_1,
        b_sure_win_2,
        b_sure_win_3,
        b_sure_win_4,
        b_sure_lose_1,
        b_sure_lose_2,
        b_sure_lose_3,
        b_sure_lose_4,
    ]


def generate_test_boards_easy():
    """
    Return a bunch of boards with utility depending on one move only.
    """

    b_win_1 = {
        "desc": "X wins by 9 if played right.",
        "board": convert_string_to_board("""
            # O - -
            # O X O
            # X O X
            # X # #
        """),
        "utility": 9,
    }

    b_win_2 = {
        "desc": "X wins by 9 if played right.",
        "board": [list(reversed(row)) for row in b_win_1["board"]],
        "utility": 9,
    }

    b_win_3 = {
        "desc": "O wins by 9 if played right.",
        "board": convert_string_to_board("""
            # X - -
            # X O X
            # O X O
            X O # #
        """),
        "utility": -9,
    }

    b_win_4 = {
        "desc": "O wins by 9 if played right.",
        "board": [list(reversed(row)) for row in b_win_3["board"]],
        "utility": -9,
    }

    # maximize long term instead of immediate reward

    b_lose_1 = {
        "desc": "X loses by only 9 if played right.",
        "board": convert_string_to_board("""
            - O X -
            O O X X
            O X O #
            # X X O
        """),
        "utility": -9,
    }

    b_lose_2 = {
        "desc": "X loses by only 9 if played right.",
        "board": [list(reversed(row)) for row in b_lose_1["board"]],
        "utility": -9,
    }

    b_lose_3 = {
        "desc": "O loses by only 9 if played right.",
        "board": convert_string_to_board("""
            - X O -
            X X O O
            X O X #
            # O # X
        """),
        "utility": 9,
    }

    b_lose_4 = {
        "desc": "O loses by only 9 if played right.",
        "board": [list(reversed(row)) for row in b_lose_3["board"]],
        "utility": 9,
    }

    return [
        b_win_1,
        b_win_2,
        b_win_3,
        b_win_4,
        b_lose_1,
        b_lose_2,
        b_lose_3,
        b_lose_4,
    ]


def generate_test_boards_intermediate():
    """
    Return a bunch of boards with utility depending on an medium amount of minimax.
    """

    b_win_1 = {
        "desc": "X wins by 18 if played right.",
        "board": convert_string_to_board("""
            X - -
            O X -
            O O X
        """),
        "utility": 18,
    }

    b_win_2 = {
        "desc": "X wins by 9 if played right.",
        "board": convert_string_to_board("""
            - - -
            - - -
            - X O
        """),
        "utility": 9,
    }

    b_win_3 = {
        "desc": "O wins by 25 if played right.",
        "board": convert_string_to_board("""
            - - - -
            - O - -
            X O - - 
            X O X X
        """),
        "utility": -25,
    }

    b_win_4 = {
        "desc": "O wins by 27 if played right.",
        "board": convert_string_to_board("""
            - X - -
            - O - -
            - O - - 
            X O X X
        """),
        "utility": -27,
    }

    b_lose_1 = {
        "desc": "O loses by 9 if played right.",
        "board": convert_string_to_board("""
            - - -
            - X -
            - X O
        """),
        "utility": 9,
    }

    b_lose_2 = {
        "desc": "X loses by 25 if played right.",
        "board": convert_string_to_board("""
            - - - -
            - O - -
            - O - - 
            X O X X
        """),
        "utility": -25,
    }

    b_lose_3 = {
        "desc": "X loses by 7 if played right.",
        "board": convert_string_to_board("""
            - - - -
            - O - -
            - O - - 
            O X X X
        """),
        "utility": -7,
    }

    b_lose_4 = {
        "desc": "O loses by 18 if played right.",
        "board": convert_string_to_board("""
            - - - -
            - X - -
            O X - - 
            O X - -
        """),
        "utility": 18,
    }

    return [
        b_win_1,
        b_win_2,
        b_win_3,
        b_win_4,
        b_lose_1,
        b_lose_2,
        b_lose_3,
        b_lose_4,
    ]

def generate_test_boards_hard():
    """
    Return a bunch of mostly empty boards requiring pruning.
    """

    b_win_1 = {
        "desc": "X wins by 9 if both played optimally",
        "board": convert_string_to_board("""
            - - - -
            - - - -
            - - - -
            O - # X
        """),
        "utility": 9,
    }

    b_win_2 = {
        "desc": "O wins by 16 if both played optimally",
        "board": convert_string_to_board("""
            - - - -
            - - - -
            - - # -
            - - # X
        """),
        "utility": -16,
    }


    b_lose_1 = {
        "desc": "O loses by 16 if both played optimally",
        "board": convert_string_to_board("""
            - - - -
            - - - -
            - - X -
            - - # -
        """),
        "utility": 16,
    }

    b_lose_2 = {
        "desc": "X loses by 9 if both played optimally",
        "board": convert_string_to_board("""
            - - - -
            - - - #
            - - - #
            # - - #
        """),
        "utility": -9,
    }
    return [
        b_win_1,
        b_win_2,
        b_lose_1,
        b_lose_2,
    ]