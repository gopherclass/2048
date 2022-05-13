from typing import Tuple
import numpy as np
import math, io


LOG_10_2 = math.log10(2)
rng = np.random.default_rng()

def merge_line(v) -> int:
    n = 0
    i = 0
    j = 1
    while j < 4:
        if i >= j:
            j += 1
        elif v[i] == 0 and v[j] == 0:
            j += 1
        elif v[i] == 0:
            v[i] = v[j]
            v[j] = 0
            j += 1
        elif v[j] == 0:
            j += 1
        elif v[i] == v[j]:
            n += 2 << v[i]
            v[i] += 1
            v[j] = 0
            i += 1
            j += 1
        else:
            i += 1
    return n

def merge(board) -> int:
    r = sum(merge_line(line) for line in board)
    return r
    #return sum(merge_line(line) for line in board)


class Board:
    def __init__(self):
        self.board = np.zeros((4,4), dtype=np.uint8)
        self.score = 0.0
    
    def __getitem__(self, pos: Tuple[int, int]):
        return self.board[pos]
    
    def __setitem__(self, pos: Tuple[int, int], value: int):
        self.board[pos] = value

    def max(self):
        return np.max(self.board)
    
    def clone(self):
        tmp = Board()
        tmp.board = self.board.copy()
        return tmp
    
    def is_equal(self, other):
        return np.array_equal(self.board, other.board)
    
    def __str__(self):
        maxlen = 1 + int(LOG_10_2 * self.max())
        #x = x.view(4, 4)
        w = io.StringIO()
        for row in self.board:
            for n in row:
                n = 1 << n.item() if n > 0 else 0
                w.write("{:>{len}} ".format(n, len=maxlen))
            w.write("\n")
        return w.getvalue()
  
    def step(self, to):
        if to == 2:  # LEFT
            self.score += merge(self.board)
        elif to == 3:  # RIGHT
            self.score += merge(np.fliplr(self.board))
        elif to == 0:  # UP
            self.score += merge(self.board.transpose())
        elif to == 1:  # DOWN
            self.score += merge(np.fliplr(self.board.transpose()))
        else:
            raise Exception('Invalid direction')
    
    def valid_acts(self):
        actions_list = []
        for action in range(4):
            tmp = self.clone()
            tmp.step(action)
            if not self.is_equal(tmp):
                actions_list.append(action)
        return actions_list

    def valid_pos(self):
        pos = np.argwhere(self.board == 0).tolist()
        if len(pos) == 0:
            return False
        return pos

    def advance(self):
        avails = np.argwhere(self.board == 0)
        if len(avails) == 0:
            return False
        i = rng.choice(avails)
        n = rng.choice([1, 2], p = [0.9, 0.1])
        self.board[tuple(i)] = n
        return True

