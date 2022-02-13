from collections import defaultdict


class MDP():
    """Class for representing a Gridworld MDP. 

    States are represented as (x, y) tuples, starting at (1, 1).  It is assumed that there are 
    four actions from each state (up, down, left, right), and that moving into a wall results in 
    no change of state.  The transition model is specified by the constants defined above.  With 
    probability prob_forw, the agent moves in the intended direction. It veers to either side with 
    probability of prob_side each.  If the agent runs into a wall, it stays in place.
    """
    
    def __init__(self, num_rows, num_cols, rewards, terminals, prob_forw, prob_side, 
                 reward_default=0.0):
        """
        Constructor for this MDP.

        Args:
            num_rows: the number of rows in the grid
            num_cols: the number of columns in the grid
            rewards: a dictionary specifying the reward function, with (x, y) state tuples as keys, 
                and rewards amounts as values.  If states are not specified, their reward is assumed
                to be equal to the REWARD_DEFAULT defined above
            terminals: a list of state (x, y) tuples specifying which states are terminal
            prob_forw: probability of going in the intended direction
            prob_side: probability of going 90 degrees to the side of the intended direction 
            reward_default: reward for any state not specified in rewards
        """
        self.nrows = num_rows
        self.ncols = num_cols
        self.states = []
        for i in range(num_cols):
            for j in range(num_rows):
                self.states.append((i+1, j+1))
        self.rewards = rewards
        self.terminals = terminals
        self.prob_forw = prob_forw
        self.prob_side = prob_side
        self.reward_def = reward_default
        self.actions = ['up', 'right', 'down', 'left']

    def get_states(self):
        """Return a list of all states as (x, y) tuples."""
        return self.states

    def get_actions(self, state):
        """Return list of possible actions from each state."""
        return self.actions

    def get_transition_prob(self, state, action, successor_state):
        """Returns the transition probability from a state to a successor state when action 
        is taken.
        """
        if self.is_terminal(state):
            return 0.0  # we cant move from terminal state since we end

        x, y = state
        succ_up = (x, min(self.nrows, y+1))
        succ_right = (min(self.ncols, x+1), y)
        succ_down = (x, max(1, y-1))
        succ_left = (max(1, x-1), y)

        succ__prob = defaultdict(float)
        if action == 'up':
            succ__prob[succ_up] = self.prob_forw
            succ__prob[succ_right] += self.prob_side
            succ__prob[succ_left] += self.prob_side
        elif action == 'right':
            succ__prob[succ_right] = self.prob_forw
            succ__prob[succ_up] += self.prob_side
            succ__prob[succ_down] += self.prob_side
        elif action == 'down':
            succ__prob[succ_down] = self.prob_forw
            succ__prob[succ_right] += self.prob_side
            succ__prob[succ_left] += self.prob_side
        elif action == 'left':
            succ__prob[succ_left] = self.prob_forw
            succ__prob[succ_up] += self.prob_side
            succ__prob[succ_down] += self.prob_side
        return succ__prob.get(successor_state, 0.0)
    
    def get_reward(self, state):
        """Get the reward for the state, return default if not specified in the constructor."""
        return self.rewards.get(state, self.reward_def)

    def is_terminal(self, state):
        """Returns True if the given state is a terminal state."""
        return state in self.terminals


def value_iteration(mdp, gamma, epsilon):
    """Calculate the utilities for the states of an MDP.

    Args:
        mdp: An instance of the MDP class defined above, describing the environment
        gamma: the discount factor
        epsilon: the change threshold to use when determining convergence.  The function returns
            when none of the states have a utility whose change from the previous iteration is more
            than epsilon

    Returns:
        A python dictionary, with state (x, y) tuples as keys, and converged utilities as values. 
    """

    utilityprime = {}
    prob = []
    maxprob = []
    # initialize utility prime, get the terminal states in
    for state in mdp.get_states():
        utilityprime[state] = mdp.get_reward(state)

    i = 0 # for printing numbering

    # go through
    while(True):
        # set utility equal to utility prime
        delta = 0
        utility = utilityprime.copy()
        # go through each state
        for state in mdp.get_states():
            # each action for each state: action
            for action in mdp.get_actions(state):
                # where that action would lead to: successor_state
                for successor_state in mdp.get_states():
                    # the transition probability from one state to all others with each action
                    prob.append(mdp.get_transition_prob(state, action, successor_state) * utility[successor_state])
                # the probability for each action
                maxprob.append(sum(prob))
                prob.clear() # clear prob for next round
            # next utility, using the max probability for an action
            utilityprime[state] = mdp.get_reward(state) + gamma * max(maxprob) # maximize utility
            maxprob.clear() # clear maxprob for next round
            delta = max(delta, abs(utilityprime[state] - utility[state])) # check change in utilities
        #print(i, '\n')
        i += 1 # printing counter
        #print(ascii_grid(utility)) # if want to see each step
        if (delta < epsilon):
            return utility


def ascii_grid(vals):
    """High-tech helper function for printing out utilities associated with a 3x2 MDP."""
    s = ""
    s += " ___________________  \n"
    s += "|         |         | \n"
    s += "| {:7.4f} | {:7.4f} | \n".format(vals[(1, 3)], vals[(2, 3)])
    s += "|_________|_________| \n"
    s += "|         |         | \n"
    s += "| {:7.4f} | {:7.4f} | \n".format(vals[(1, 2)], vals[(2, 2)])
    s += "|_________|_________| \n"
    s += "|         |         | \n"
    s += "| {:7.4f} | {:7.4f} | \n".format(vals[(1, 1)], vals[(2, 1)])
    s += "|_________|_________| \n"
    return s


##################################

if __name__ == "__main__":
    
    GAMMA = 0.9
    EPSILON = 0.01

    rewards = {(1,3): -2.0, (2,3): 2.0}
    terminals = [(1,3),(2,3)]
    gridworld = MDP(3, 2, rewards, terminals, 0.8, 0.1)  # put the correct args here or it will error out!

    utilities = value_iteration(gridworld, GAMMA, EPSILON)
    print(ascii_grid(utilities))


