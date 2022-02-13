import sys
import puzz
import pdqpq
import time
MAX_SEARCH_ITERS = 100000
GOAL_STATE = puzz.EightPuzzleBoard("012345678")


# ----- HELPER FUNCTIONS -----

def findpath(parent, start, end):
   #print('PATHIFICATION')
   path = [end]
   #print(path)
   direction = []
   while path[-1] != start:
       direction.append(tuple([parent[path[-1]][1], path[-1]]))  # add direction
       #print(parent[path[-1]][1])
       path.append(parent[path[-1]][0])  # needs to be second because of condition
       #print(path[-1])
   direction.append(tuple(['start', start]))  # add direction
   direction.reverse()
   path = direction
   return path


def calculateCost(prev_state, state):
   x, y = prev_state.find('0')
   square = int(state._get_tile(x, y))
   return square ** 2


def calculateHeuristic(heuristic, state1, state2):
   if heuristic == 'h1':
       heuristic_value = calculateMisplacedTiles(state1, state2)
   elif heuristic == 'h2':
       heuristic_value = calculateManhattanDistance(state1, state2)
   else:
       heuristic_value = calculateWeightedManhattanDistance(state1, state2)
   return heuristic_value


def calculateMisplacedTiles(state1, state2):
   #print('entering misplacedTiles')
   misplaced_heuristic = 0
   for tile in range(9):
       if state1.find(str(tile)) != state2.find(str(tile)):
           misplaced_heuristic += 1
   return misplaced_heuristic


def calculateManhattanDistance(state1, state2):
   #print('entering manhattandistance')
   manhattan_distance = 0
   for tile in range(9):
       x1, y1 = state1.find(str(tile))
       x2, y2 = state2.find(str(tile))
       manhattan_distance += abs(x1-x2) + abs(y1-y2)
   return manhattan_distance


def calculateWeightedManhattanDistance(state1, state2):
   #print('entering weightedmanhattandistance')
   manhattan_distance = 0
   for tile in range(9):
       x1, y1 = state1.find(str(tile))
       x2, y2 = state2.find(str(tile))
       manhattan_distance += tile ** 2 * (abs(x1-x2) + abs(y1-y2))
   return manhattan_distance


# ----- SEARCH ALGORITHMS -----


def bfs(start_state, results):
   frontier = pdqpq.PriorityQueue()
   frontier.add(start_state)
   results['frontier_count'] += 1
   explored = set()
   parent = {start_state: [None, None, 0]}  # state: [parent, direction (n), cost]

   while not frontier.empty():
       node = frontier.pop()
       explored.add(node)  # add node to explored set
       successors = node.successors()  # successors of node that was just popped
       results['expanded_count'] += 1

       for n in successors:  # for each direction in successors
           prev_cost = int(parent[node][2])  # total cost up to the previous state
           cur_cost = calculateCost(node, successors[n])  # cost to get to this state from previous
           cost = cur_cost + prev_cost  # total cost from start to current state
           if (successors[n] not in frontier) and (successors[n] not in explored):
               if successors[n] == GOAL_STATE:
                   parent[successors[n]] = [node, n, cost]  # current_state : previous_state, direction of current
                   results['path'] = findpath(parent, start_state, GOAL_STATE)
                   results['path_cost'] = parent[GOAL_STATE][2]
                   return results
               else:
                   frontier.add(successors[n])
                   results['frontier_count'] += 1
                   parent[successors[n]] = [node, n, cost]
   del results['path']
   return results


def ucost(start_state, results):

   frontier = pdqpq.PriorityQueue()  # create the frontier
   frontier.add(start_state, 0)  # add start state to frontier
   results['frontier_count'] += 1

   explored = set()  # dictionary of explored states

   state_info = {start_state: [None, None, 0]}  # state: [parent, direction (n), cost]
   cost = 0

   while not frontier.empty():
       node = frontier.pop()

       explored.add(node)  # add node to explored set
       if str(node) == str(GOAL_STATE):  # if node and goal states are the same
           #print('solution found')
           results['path_cost'] = state_info[GOAL_STATE][2]  # add path cost to results
           #print(state_info)
           results['path'] = findpath(state_info, start_state, GOAL_STATE)
           return results

       explored.add(node)
       successors = node.successors()
       results['expanded_count'] += 1

       for n in successors:
           prev_cost = int(state_info[node][2])  # total cost up to the previous state
           cur_cost = calculateCost(node, successors[n])  # cost to get to this state from previous
           cost = cur_cost + prev_cost  # total cost from start to current state

           if (successors[n] not in frontier) and (successors[n] not in explored):
               frontier.add(successors[n], cost)
               state_info[successors[n]] = [node, n, cost]  # update dictionary
               results['frontier_count'] += 1

           elif (successors[n] in frontier) and (frontier.get(successors[n]) > cost):
               frontier.add(successors[n], cost)
               state_info[successors[n]] = [node, n, cost]  # update dictionary

   del results['path']
   del results['path_cost']
   return results


def greedy(start_state, heuristic, results):
   frontier = pdqpq.PriorityQueue()  # create the frontier
   frontier.add(start_state, 0)  # add start state to frontier
   results['frontier_count'] += 1

   explored = set()  # dictionary of explored states

   state_info = {start_state: [None, None, 0]}  # state: [parent, direction (n), cost]
   cost = 0

   while not frontier.empty():
       node = frontier.pop()

       if str(node) == str(GOAL_STATE):  # if node and goal states are the same
           results['path_cost'] = state_info[GOAL_STATE][2]  # add path cost to results
           #state_info[successors[n]] = [node, n, cost]  # update dictionary
           results['path'] = findpath(state_info, start_state, GOAL_STATE)
           return results

       explored.add(node)
       successors = node.successors()
       results['expanded_count'] += 1

       for n in successors:
           prev_cost = int(state_info[node][2])  # total cost up to the previous state
           cur_cost = calculateCost(node, successors[n])  # cost to get to this state from previous
           cost = cur_cost + prev_cost  # total cost from start to current state
           heuristic_value = calculateHeuristic(heuristic, successors[n], GOAL_STATE)
           if (successors[n] not in frontier) and (successors[n] not in explored):
               frontier.add(successors[n], heuristic_value)
               state_info[successors[n]] = [node, n, cost]  # update dictionary
               results['frontier_count'] += 1

           elif (successors[n] in frontier) and (frontier.get(successors[n]) > heuristic_value):
               frontier.add(successors[n], heuristic_value)
               state_info[successors[n]] = [node, n, cost]  # update dictionary

   del results['path']
   del results['path_cost']
   return results


def astar(start_state, heuristic, results):
   frontier = pdqpq.PriorityQueue()  # create the frontier
   frontier.add(start_state, 0)  # add start state to frontier
   results['frontier_count'] += 1

   explored = set()  # dictionary of explored states

   state_info = {start_state: [None, None, 0]}  # state: [parent, direction (n), cost]
   cost = 0

   while not frontier.empty():
       node = frontier.pop()


       if str(node) == str(GOAL_STATE):  # if node and goal states are the same
           print('solution found')
           results['path_cost'] = state_info[GOAL_STATE][2]  # add path cost to results
           #state_info[successors[n]] = [node, n, cost]  # update dictionary
           results['path'] = findpath(state_info, start_state, GOAL_STATE)
           return results

       explored.add(node)
       successors = node.successors()
       results['expanded_count'] += 1

       for n in successors:
           prev_cost = int(state_info[node][2])  # total cost up to the previous state
           cur_cost = calculateCost(node, successors[n])  # cost to get to this state from previous
           cost = cur_cost + prev_cost  # total cost from start to current state

           heuristic_value = calculateHeuristic(heuristic, successors[n], GOAL_STATE)
           priority = cost + heuristic_value
           if (successors[n] not in frontier) and (successors[n] not in explored):
               frontier.add(successors[n], priority)
               state_info[successors[n]] = [node, n, cost]  # update dictionary
               results['frontier_count'] += 1

           elif (successors[n] in frontier) and (frontier.get(successors[n]) > priority):
               frontier.add(successors[n], priority)
               state_info[successors[n]] = [node, n, cost]  # update dictionary

   del results['path']
   del results['path_cost']
   return results


def solve_puzzle(start_state, strategy):
   """Perform a search to find a solution to a puzzle.

   Args:
       start_state: an EightPuzzleBoard object indicating the start state for the search
       flavor: a string indicating which type of search to run.  Can be one of the following:
           'bfs' - breadth-first search
           'ucost' - uniform-cost search
           'greedy-h1' - Greedy best-first search using a misplaced tile count heuristic
           'greedy-h2' - Greedy best-first search using a Manhattan distance heuristic
           'greedy-h3' - Greedy best-first search using a weighted Manhattan distance heuristic
           'astar-h1' - A* search using a misplaced tile count heuristic
           'astar-h2' - A* search using a Manhattan distance heuristic
           'astar-h3' - A* search using a weighted Manhattan distance heuristic

   Returns:
       A dictionary containing describing the search performed, containing the following entries:
           'path' - a list of 2-tuples representing the path from the start state to the goal state
               (both should be included), with each entry being a (str, EightPuzzleBoard) pair
               indicating the move and resulting state for each action.  Omitted if the search
               fails.
           'path_cost' - the total cost of the path, taking into account the costs associated
               with each state transition.  Omitted if the search fails.
           'frontier_count' - the number of unique states added to the search frontier at any
               point during the search.
           'expanded_count' - the number of unique states removed from the frontier and expanded
               (successors generated).
   """

   results = {
       'path': [],
       'path_cost': 0,
       'frontier_count': 0,
       'expanded_count': 0,
   }

   if strategy == 'bfs':  # breadth-first
       results = bfs(start_state, results)
   elif strategy == 'ucost':  # uniform cost
       results = ucost(start_state, results)
   elif strategy[:-3] == 'greedy':  # greedy best-first
       results = greedy(start_state, strategy[-2:], results)
   elif strategy[:-3] == 'astar':  # astar
       results = astar(start_state, strategy[-2:], results)
   else:
       del results['path']
       del results['path_cost']
   return results


def print_summary(results):
   if 'path' in results:
       print("found solution of length {}, cost {}".format(len(results['path']),
                                                           results['path_cost']))
       for move, state in results['path']:
           print("  {:5} {}".format(move, state))
   else:
       print("no solution found")
   print("{} states placed on frontier, {} states expanded".format(results['frontier_count'],
                                                                   results['expanded_count']))


############################################

if __name__ == '__main__':
   start = puzz.EightPuzzleBoard(sys.argv[1])
   method = sys.argv[2]

   print("solving puzzle {} -> {}".format(start, GOAL_STATE))
   results = solve_puzzle(start, method)
   print_summary(results)
