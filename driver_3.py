import sys
from math import sqrt
import resource
import time

class Moves:

    UP = 'Up'
    DOWN = 'Down'
    LEFT = 'Left'
    RIGHT = 'Right'

class State:

    HOLE = 0

    def __init__(self, board=None, sequence=[]):
        self.board = board if board is not None else [i for i in range(9)]
        self.width = sqrt(len(self.board))
        self.goal_state_board = [i for i in range(len(self.board))]
        self.hole_index = self.board.index(State.HOLE)
        self.sequence = sequence

    def __str__(self):
        return str('Board:{}\nSequence:{}'.format(self.board, self.sequence))

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.board == other.board

    def __hash__(self):
        return hash(tuple(self.board))

    def board_string(self):
        return str(self.board)

    def is_solvable(self):
        inversion_count = 0
        for i in range(len(self.board) - 1):
            for j in range(i + 1, len(self.board)):
                if self.board[i] and self.board[j] and self.board[i] > self.board[j]:
                    inversion_count += 1
        return inversion_count % 2 == 0

    def is_solved(self):
        return self.board == self.goal_state_board

    def possible_moves(self):
        if self.hole_index >= self.width:
            yield Moves.UP
        if self.hole_index < (len(self.board) - self.width):
            yield Moves.DOWN
        if self.hole_index % self.width != 0:
            yield Moves.LEFT
        if (self.hole_index + 1) % self.width != 0:
            yield Moves.RIGHT

    def generate_next_state(self, move):
        new_sequence = self.sequence[::]
        new_sequence.append(move)
        next_state = State(self.board[::], new_sequence)
        old_hole_index = next_state.hole_index
        if move == Moves.UP:
            new_hole_index = int(next_state.hole_index - next_state.width)
        elif move == Moves.DOWN:
            new_hole_index = int(next_state.hole_index + next_state.width)
        elif move == Moves.LEFT:
            new_hole_index = int(next_state.hole_index - 1)
        elif move == Moves.RIGHT:
            new_hole_index = int(next_state.hole_index + 1)

        next_state.board[new_hole_index], next_state.board[old_hole_index] = \
                next_state.board[old_hole_index], next_state.board[new_hole_index]
        next_state.hole_index = new_hole_index

        return next_state

    def generate_possible_states(self):
        return [self.generate_next_state(move) for move in self.possible_moves()]

    def manhattan_distance(self):
        total_distance = 0
        current_index = 0
        for tile in self.board:
            ideal_index = self.goal_state_board.index(tile)
            c_x, c_y = current_index % self.width, current_index // self.width
            i_x, i_y = ideal_index % self.width, ideal_index // self.width
            total_distance += abs(c_x - i_x) + abs(c_y - i_y)
            current_index += 1
        return total_distance

    def a_star_heuristics(self):
        return self.manhattan_distance() + len(self.sequence)

class Output:

    def __init__(self, sequence=[], nodes_expanded=0, max_search_depth=0):
        self.sequence = sequence
        self.cost_of_path = len(sequence)
        self.nodes_expanded = nodes_expanded
        self.search_depth = len(sequence)
        self.max_search_depth = max_search_depth
        self.running_time = 0.0
        self.max_ram_usage = 0.0

    def __str__(self):
        return "path_to_goal: {}\ncost_of_path: {}\nnodes_expanded: {}\nsearch_depth: {}\nmax_search_depth: {}\nrunning_time: {:.8f}\nmax_ram_usage: {:.8f}\n".format(self.sequence,\
                self.cost_of_path,\
                self.nodes_expanded,\
                self.search_depth,\
                self.max_search_depth,\
                self.running_time,\
                self.max_ram_usage\
                )

def solve_bfs(state):
    states = []
    states.append(state)
    state_index = 0
    check_count = 0
    max_search_depth = 0
    while True:
        if state_index < 0 or state_index >= len(states):
            raise ValueError("No solution found for state:\n {}".format(state))
        check_state = states[state_index]
        state_index += 1
        if check_state.is_solved():
            return Output(check_state.sequence, check_count, max_search_depth)
        check_count += 1
        for state in check_state.generate_possible_states():
            if state not in states:
                states.append(state)
                state_depth = len(state.sequence)
                if state_depth > max_search_depth:
                    max_search_depth = state_depth


def solve_dfs(state):
    checked_states = {}
    states = []
    states_dict = {}
    states.append(state)
    states_dict[state.board_string()] = True
    max_search_depth = 0
    check_count = 0
    while True:
        if len(states) < 1:
            raise ValueError("No solution found for state:\n {}".format(state))
        check_state = states.pop()
        del states_dict[check_state.board_string()]
        checked_states[check_state.board_string()] = True
        if check_state.is_solved():
            return Output(check_state.sequence, check_count, max_search_depth)
        check_count += 1
        for state in reversed(list(check_state.generate_possible_states())):
            state_key = state.board_string()
            if state_key not in states_dict and state_key not in checked_states:
                states.append(state)
                states_dict[state_key] = True
                state_depth = len(state.sequence)
                if state_depth > max_search_depth:
                    max_search_depth = state_depth


def solve_ast(state):
    checked_states = []
    states = []
    states.append(state)
    max_search_depth = 0
    check_count = 0
    while True:
        if len(states) < 1:
            raise ValueError("No solution found for state:\n {}".format(state))
        check_state = states.pop()
        checked_states.append(check_state)
        if check_state.is_solved():
            return Output(check_state.sequence, check_count, max_search_depth)
        check_count += 1
        for state in check_state.generate_possible_states():
            if state not in checked_states:
                states.append(state)
                state_depth = len(state.sequence)
                if state_depth > max_search_depth:
                    max_search_depth = state_depth
        states.sort(key=lambda x:x.a_star_heuristics(),reverse=True)


if __name__=="__main__":
    arguments = sys.argv
    search_type = arguments[1]
    initial_state = State([int(val) for val in arguments[2].split(',')])
    start_time = time.time()
    output = Output()
    if search_type == 'bfs':
        output = solve_bfs(initial_state)
    elif search_type == 'dfs':
        output = solve_dfs(initial_state)
    elif search_type == 'ast':
        output = solve_ast(initial_state)
    else:
        print('Invalid search_type: {}'.format(search_type))

    output.max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    output.running_time = time.time() - start_time
    f = open('output.txt', 'w')
    f.write(str(output))
    f.close()
