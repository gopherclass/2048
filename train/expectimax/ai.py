from board import Board
import time, math

Action = int
Value = float
State = Board
Actions = ['Left', 'Right', 'Up', 'Down']

def eval(state: State, weighted: bool) -> Value:
    def smoothness():
        smoothness = 0.0
        for x in range(4):
            for y in range(4):
                if state[x,y] != 0:
                    value = math.log(state[x,y]) / math.log(2)
                    for i in range(x+1, 4):
                        if state[i,y] != 0:
                            target_value = math.log(state[i,y]) / math.log(2)
                            smoothness -= abs(value - target_value)
                    for i in range(y+1, 4):
                        if state[x,i] != 0:
                            target_value = math.log(state[x,i]) / math.log(2)
                            smoothness -= abs(value - target_value)
        return smoothness

    def monotonicity():
        directions = [0, 0, 0, 0] # up, down, left, right
        for x in range(4):
            for i in range(x+1, 4):
                difference = state[x,:] - state[i,:]
                for j in range(4):
                    if difference[j] >= 0: directions[0] += abs(difference[j]) # monotonic upward
                    elif difference[j] < 0: directions[1] += abs(difference[j]) # monotonic downward
        for y in range(4):
            for i in range(y+1, 4):
                difference = state[:,y] - state[:,i]
                for j in range(4):
                    if difference[j] >= 0: directions[2] += abs(difference[j]) # monotonic leftward (e.g. [32, 16, 8, 4])
                    if difference[j] < 0: directions[3] += abs(difference[j]) # monotonic rightward (e.g. [4, 8, 16, 32])
        return max(directions[0:2]) + max(directions[2:4])

    if weighted:
        """
        Heuristics: smoothness와 monotonicity를 고려하여 현재 상태의 가치를 계산함
        smoothness: 한 행/열 내의 값들이 얼마나 다른지를 계산함 e.g. [1024, 1024, 1024, 1024]는 perfectly smooth함
        monotonicity: 한 행/열 내의 값들이 단조적으로 증가/감소하는지를 계산함 e.g. [32, 16, 8, 4]는 left방향으로 monotonic함
        """
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
def get_move(state: State, max_depth: int, weighted: bool) -> Action:
    max_action = None
    max_value = float('-inf')
    #for action in range(4):
    for action in state.valid_acts():
        new_state = state.clone()
        new_state.step(action)

        if state.is_equal(new_state):
            continue

        if max_action is None:
            max_action = action
        
        state_value = chance(new_state, 1.0, max_depth, weighted)

        if state_value > max_value:
            max_value = state_value
            max_action = action

    return max_action

def maximize(state, prob, depth, weighted: bool) -> Value:
    #print('max', depth)
    max_value = float('-inf')

    #for action in range(4):
    for action in state.valid_acts():
        new_state = state.clone()
        new_state.step(action)

        if state.is_equal(new_state):
            continue

        value = chance(new_state, prob, depth - 1, weighted)
        max_value = max(max_value, value)

    return max_value

def chance(state, prob, depth, weighted: bool) -> Value:
    #print('chance', depth)
    
    empty_cells = state.valid_pos()
    n_empty = len(empty_cells)
    
    if depth <= 1 and n_empty > 12:
        return eval(state, False)

    if depth <= 1 or prob <= 1e-4:
        return eval(state, weighted)

    prob /= n_empty
    prob_tile2 = 0.9 * prob
    prob_tile4 = 0.1 * prob

    alpha = 0.0

    for cell in empty_cells:
        cell = tuple(cell)
        if state[cell] == 0:
            state[cell] = 1
            alpha += maximize(state, prob_tile2, depth, weighted)
            state[cell] = 2
            alpha += maximize(state, prob_tile4, depth, weighted)
            state[cell] = 0

    res = alpha / n_empty

    return res


