from re import M
import numpy as np
#from board import Board
class Network():
    def __init__(self, n, m, indices_list, c=17):
        self.n = n  # size of single tuple
        self.m = m  # number of tuples
        self.c = c  # base
        self.tuples = [Tuple(indices, n, m, c) for indices in indices_list]

    def index(self, v):
        ret = 0
        for j in range(len(v)): # len(v) = self.n
            ret += v[j] * self.c**j
        return int(ret)
    
    def get(self, state):
        sum_values = 0
        for tup in self.tuples:
            v_sequence = tup.look_up(state)
            index_v = self.index(v_sequence)
            sum_values += tup.lut[index_v]
        return sum_values
    
    def update(self, state, update_state, reward, alpha=0.0025):
        for tup in self.tuples:
            v_sequence = tup.look_up(state)
            index_v = self.index(v_sequence)
            tup.lut[index_v] += alpha * (reward + self.get(update_state) - self.get(state))



class Tuple():
    def __init__(self, indices, n, m, c=17):
        self.indices = indices
        self.n_weights = m*(c**n)
        self.lut = np.zeros(self.n_weights)#[0]*self.n_weights
    
    def look_up(self, board):
        tile_values = []
        for index in self.indices:
            val = board.board[index] if board.board[index] != 0 else 0
            tile_values.append(val)
        return tile_values


    

