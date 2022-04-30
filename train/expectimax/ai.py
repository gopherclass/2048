from board import Board
import time, math

Action = int
Value = float
State = Board
Actions = ['Left', 'Right', 'Up', 'Down']

def eval(state: State, weighted: bool) -> Value:
    def smoothness():
        smoothness = 0.0
        for row in state:
            pass #TODO:

    def monotonicity():
        pass
    if weighted:
        n_empty = len(state.valid_pos())
        weights = {
            'w_smoothness': 0.1,
            'w_monotonicity': 1.0,
            'w_empty': 2.7,
            'w_max': 1.0
        }
        value = smoothness() * weights['w_smoothness'] \
            + monotonicity() * weights['w_monotonicity'] \
            + state.max() * weights['w_max'] \
            + math.log(n_empty) * weights['w_empty']
        return value
    else:
        return state.score
# state -> expectimax search -> action
def get_move(state: State, max_depth: int) -> Action:
    max_action = None
    max_value = float('-inf')
    for action in range(4):
        new_state = state.clone()
        new_state.step(action)

        if state.is_equal(new_state):
            continue

        if max_action is None:
            max_action = action
        
        state_value = chance(new_state, 1.0, max_depth)

        if state_value > max_value:
            max_value = state_value
            max_action = action

    return max_action

def maximize(state, prob, depth) -> Value:
    #print('max', depth)
    max_value = float('-inf')

    #for action in range(4):
    for action in state.valid_acts():
        new_state = state.clone()
        new_state.step(action)

        if state.is_equal(new_state):
            continue

        value = chance(new_state, prob, depth - 1)
        max_value = max(max_value, value)

    return max_value

def chance(state, prob, depth) -> Value:
    #print('chance', depth)
    if depth <= 1 or prob <= 1e-4:
        return state.score
    
    empty_cells = state.valid_pos()
    n_empty = len(empty_cells)

    prob /= n_empty
    prob_tile2 = 0.9 * prob
    prob_tile4 = 0.1 * prob

    alpha = 0.0

    for cell in empty_cells:
        cell = tuple(cell)
        if state[cell] == 0:
            state[cell] = 1
            alpha += maximize(state, prob_tile2, depth)
            state[cell] = 2
            alpha += maximize(state, prob_tile4, depth)
            state[cell] = 0

    res = alpha / n_empty

    return res


