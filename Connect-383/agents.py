import random
import math

BOT_NAME = "sudo rm -rf /*"  # jk lol


class RandomAgent:
    """Agent that picks a random available move.  You should be able to beat it."""

    def __init__(self, sd=None):
        if sd is None:
            self.st = None
        else:
            random.seed(sd)
            self.st = random.getstate()

    def get_move(self, state):
        if self.st is not None:
            random.setstate(self.st)
        return random.choice(state.successors())


class HumanAgent:
    """Prompts user to supply a valid move."""

    def get_move(self, state, depth=None):
        move__state = dict(state.successors())
        prompt = "Kindly enter your move {}: ".format(sorted(move__state.keys()))
        move = None
        while move not in move__state:
            try:
                move = int(input(prompt))
            except ValueError:
                continue
        return move, move__state[move]


class MinimaxAgent:
    """Artificially intelligent agent that uses minimax to optimally select the best move."""

    def get_move(self, state):
        """Select the best available move, based on minimax value."""
        nextp = state.next_player()
        best_util = -math.inf if nextp == 1 else math.inf
        best_move = None
        best_state = None

        for move, state in state.successors():
            util = self.minimax(state)
            if ((nextp == 1) and (util > best_util)) or ((nextp == -1) and (util < best_util)):
                best_util, best_move, best_state = util, move, state
        return best_move, best_state

    def minimax(self, state):
        """Determine the minimax utility value of the given state.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the exact minimax utility value of the state
        """

        def maxValue(state):
            if state.is_full():
                v = state.utility()
            else:
                v = float('-inf')  # https://www.geeksforgeeks.org/python-infinity/
                for move, s in state.successors():
                    v = max(v, minValue(s))
            return v

        def minValue(state):
            if state.is_full():
                v = state.utility()
            else:
                v = float('inf')
                for move, s in state.successors():
                    v = min(v, maxValue(s))
            return v

        if state.is_full():
            v = state.utility()
        else:
            if state.next_player() == 1:
                v = maxValue(state)
            else:
                v = minValue(state)
        return v


class MinimaxHeuristicAgent(MinimaxAgent):
    """Artificially intelligent agent that uses depth-limited minimax to select the best move."""

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def minimax(self, state):
        """Determine the heuristically estimated minimax utility value of the given state.

        The depth data member (set in the constructor) determines the maximum depth of the game 
        tree that gets explored before estimating the state utilities using the evaluation() 
        function.  If depth is 0, no traversal is performed, and minimax returns the results of 
        a call to evaluation().  If depth is None, the entire game tree is traversed.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """

        def maxValue(state, depth):
            if state.is_full() or depth == 0:
                v = self.evaluation(state)
            else:
                v = float('-inf')  # https://www.geeksforgeeks.org/python-infinity/
                for move, s in state.successors():
                    v = max(v, minValue(s, depth-1))
            return v

        def minValue(state, depth):
            if state.is_full() or depth == 0:
                v = self.evaluation(state)
            else:
                v = float('inf')
                for move, s in state.successors():
                    v = min(v, maxValue(s, depth-1))
            return v

        if state.is_full() or self.depth_limit == 0:
            v = self.evaluation(state)
        else:
            if state.next_player() == 1:
                v = minValue(state, self.depth_limit-1)
            else:
                v = maxValue(state, self.depth_limit-1)
        return v

    def evaluation(self, state):

        """Estimate the utility value of the game state based on features.

        N.B.: This method must run in O(1) time!

        Args:
            state: a connect383.GameState object representing the current board

        Returns: a heusristic estimate of the utility value of the state
        """

        def lineCalc(state_thing):
            value = 0
            for line in state_thing:
                streak = streaks(line)  # streak is list of tuples (value, streak)
                for i in range(len(streak) - 1):
                    # check for "gap" between streak
                    current_streak_value = streak[i][0]
                    current_streak_length = streak[i][1]
                    prev_streak_value = streak[i - 1][0]
                    prev_streak_length = streak[i - 1][1]
                    next_streak_value = streak[i + 1][0]
                    next_streak_length = streak[i + 1][1]
                    if (current_streak_value == 0 and current_streak_length == 1 and (abs(prev_streak_value) == 1) and (
                            prev_streak_value == next_streak_value)):
                        connector_value = prev_streak_value * (
                                    prev_streak_length + next_streak_length + 1) ** 2  # score if completed
                        if prev_streak_length > 2:
                            connector_value -= prev_streak_value * prev_streak_length ** 2
                        if next_streak_length > 2:
                            connector_value -= next_streak_value * next_streak_length ** 2
                        value += connector_value
                    # if there was a streak that got blocked by the other player
                    if (current_streak_length >= 2) & (current_streak_value == -1 * next_streak_value):
                        block_value = next_streak_value * (
                                    current_streak_length + 1) ** 2  # the blocker's player times the length of the streak that was prevented
                        if current_streak_length > 2:  # don't subtract if blocked a potential 3
                            block_value -= next_streak_value * current_streak_length ** 2
                        value += block_value
                    # if there is a streak
                    if current_streak_length > 2:
                        value += current_streak_value * current_streak_length ** 2
                if streak[-1][1] > 2:
                    value += streak[-1][0] * streak[-1][1] ** 2
            return value

        def centerScore(state_rows, state_cols):  # preference to middle values
            center_value = 0

            for i in range(len(state_rows)):
                counter = 0
                for j in state_rows[i]:
                    center_value += j * (-1 * abs(counter - int(len(state_rows) / 2)) + int(len(state_rows) / 2)) # slight preference towards middle (triangle, higher values towards middle)
                    counter += 1
            return center_value

        state_rows = state.get_rows()
        state_cols = state.get_cols()
        state_diags = state.get_diags()

        row_value = lineCalc(state_rows)
        col_value = lineCalc(state_cols)
        diag_value = lineCalc(state_diags)
        center_value = centerScore(state_rows, state_cols)

        eval = row_value + col_value + diag_value + center_value

        return eval


class MinimaxHeuristicPruneAgent(MinimaxHeuristicAgent):
    """Smarter computer agent that uses minimax with alpha-beta pruning to select the best move."""

    def minimax(self, state):
        """Determine the minimax utility value the given state using alpha-beta pruning.

        The value should be equal to the one determined by MinimaxAgent.minimax(), but the 
        algorithm should do less work.  You can check this by inspecting the value of the class 
        variable GameState.state_count, which keeps track of how many GameState objects have been 
        created over time.  This agent should also respect the depth limit like HeuristicAgent.

        N.B.: When exploring the game tree and expanding nodes, you must consider the child nodes
        in the order that they are returned by GameState.successors().  That is, you cannot prune
        the state reached by moving to column 4 before you've explored the state reached by a move
        to to column 1.

        Args: 
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """

        def maxValue(state, depth, alpha, beta):
            if state.is_full() or depth == 0:
                v = self.evaluation(state)
            else:
                v = float('-inf')  # https://www.geeksforgeeks.org/python-infinity/
                for move, s in state.successors():
                    v = max(v, minValue(s, depth - 1, alpha, beta))
                    alpha = max(v, alpha)
                    if beta <= alpha:
                        break
            return v

        def minValue(state, depth, alpha, beta):
            if state.is_full() or depth == 0:
                v = self.evaluation(state)
            else:
                v = float('inf')
                for move, s in state.successors():
                    v = min(v, maxValue(s, depth - 1, alpha, beta))
                    beta = min(v, beta)
                    if beta <= alpha:
                        break
            return v

        alpha = float('-inf')
        beta = float('inf')

        if state.is_full() or self.depth_limit == 0:
            v = self.evaluation(state)
        else:
            if state.next_player() == 1:
                v = minValue(state, self.depth_limit - 1, alpha, beta)
            else:
                v = maxValue(state, self.depth_limit - 1, alpha, beta)
        return v


def streaks(lst):  # taken from connect383.py
    """Get the lengths of all the streaks of the same element in a sequence."""
    rets = []  # list of (element, length) tuples
    prev = lst[0]
    curr_len = 1
    for curr in lst[1:]:
        if curr == prev:
            curr_len += 1
        else:
            rets.append((prev, curr_len))
            prev = curr
            curr_len = 1
    rets.append((prev, curr_len))
    return rets