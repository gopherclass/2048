from board import Board
from ai import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--depth', type=int, default=3)
args = parser.parse_args()


def main():
    max_depth = args.depth

    # board initialization
    board = Board()
    board.advance()
    board.advance()
    print('Initial Board (Search Depth: {})'.format(max_depth))
    print(board)

    #while board.valid_pos():
    while True:
        s = time.time()
        action = get_move(board, max_depth)
        duration = time.time() - s
        if action is None:
            break
        board.step(action)
        board.advance()
        print(f'MOVE to {Actions[action]}({action}), Total Score: {int(board.score)}, Search time: {duration:.3f}s')
        print(board)

if __name__ == '__main__':
    main()