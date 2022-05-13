import numpy as np
import time
# from game_board import GameBoard
from board import Board
from n_tuple import Network
from random import randint
from tqdm import tqdm
import pickle

acts = ['UP', 'DOWN', 'LEFT', 'RIGHT']

class PlayGame():
    def __init__(self, n, m, indices_list, c=17, verbose=True):
        # self.board = GameBoard()
        self.board = Board()
        self.V = Network(n, m, indices_list, c)
    
    def save_checkpoint(self, save_file):
        with open(save_file, 'wb') as f:
            pickle.dump(self, f)


    def run(self, save_file, writer, n_epochs, is_learning, verbose=True):
        self.verbose = verbose
        self.is_learning = is_learning
        total_score_sum = 0.0
        max_tiles = []
        highest_tile = -1
        highest_score = -1
        winrate = 0.0
        whatami = 'Train' if is_learning else 'Test'
        for i in tqdm(range(n_epochs)):
            self.init_game()
            self.learn()
            # Max tile
            max_tile = 1 << self.board.max() # 현재 보드의 max tile
            if max_tile > highest_tile:  # 전체 max tile
                highest_tile = max_tile
            max_tiles.append(max_tile)
            if max_tile >= 2048:
                winrate += 1
            # Score
            score = self.board.score
            total_score_sum += score
            if score > highest_score:
                highest_score = score
            # Summary
            if i % 100 == 0:
                if writer is not None:
                    writer.add_scalar("Score/"+whatami, total_score_sum/(i+1), i)
                    writer.add_scalar("Max_tile/"+whatami, max_tile, i)
            # Checkpoint
            if i % 1000 == 0 and i != 0:
                if save_file is not None: self.save_checkpoint(save_file)
                if writer is not None: writer.flush()
            print(f'GAME {i} OVER. total score : {self.board.score}, max tile : {max_tile}')
        print('======= ' + whatami + ' Over =======')
        print(f'Avg. Total score: {total_score_sum/n_epochs}, Highest Tile Reached: {highest_tile}, Highest Score Reached: {highest_score}')


    def init_game(self):
        self.board = Board()
        self.board.advance()
        self.board.advance()
    
    def learn(self):
        t = 0
        while True:
            if len(self.board.valid_acts()) == 0:
                break
            action = self.get_move(self.board)
            reward, after_state, next_state = self.make_move(action)
            if self.verbose:
                print(self.board)
            if self.is_learning and t > 0:
                self.learn_evaluation(after_state, next_state)
            t += 1

    def get_move(self, state): # argmax_a(Evaluate(s,a'))
        #next_actions = range(4)
        next_actions = state.valid_acts()
        action_list = [0]*4
        for a in range(4):
            if a in next_actions:
                action_list[a] += self.evaluate(state,a)
            #action_list.append(self.evaluate(state, a))
        return np.argmax(action_list)

    def evaluate(self, state, action : int):
        after_state, reward = self.compute_afterstate(state, action)
        return reward + self.V.get(after_state)
    
    def compute_afterstate(self, state, action : int):
        temp_grid = state.clone()
        temp_grid.step(action)
        return temp_grid, temp_grid.score

    def make_move(self, action : int):
        after_state, reward = self.compute_afterstate(self.board, action)
        if self.verbose:
            print(f'MOVE to {acts[action]} ({action}), Total Score : {self.board.score}')
        self.board.step(action)
        self.board.advance()
        next_state = self.board.clone()
        return reward, after_state, next_state

    def learn_evaluation(self, after_state, next_state):
        action = self.get_move(next_state)
        after_state_, reward_ = self.compute_afterstate(next_state, action)
        self.V.update(after_state, after_state_, reward_)
