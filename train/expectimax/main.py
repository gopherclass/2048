from board import Board
from ai import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--depth', type=int, default=3)
parser.add_argument('--weights', action='store_true')
args = parser.parse_args()

def test():
    board = Board()


    print(board)
    print(eval(board, True))


def main():
    max_depth = args.depth
    use_weights = args.weights
    print(args)

    # board initialization
    board = Board()
    board.advance()
    board.advance()
    print('Initial Board (Search Depth: {})'.format(max_depth))
    print(board)

    #while board.valid_pos():
    while True:
        s = time.time()
        n_empty = len(board.valid_pos())
        if n_empty >= 12:
            action = get_move(board, 1, False)
        #if n_empty >= 6:
        else:
            action = get_move(board, max_depth, use_weights)
        # else:
        #     action = get_move(board, max_depth + 1, use_weights)
        duration = time.time() - s
        if action is None:
            break
        board.step(action)
        board.advance()
        print(f'MOVE to {Actions[action]}({action}), Total Score: {int(board.score)}, Search time: {duration:.3f}s')
        print(board)

if __name__ == '__main__':
    main()
    #test()