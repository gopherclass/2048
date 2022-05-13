import os, pickle
from play_game import PlayGame
from argparse import ArgumentParser
from numpy import save
from torch.utils.tensorboard import SummaryWriter

parser = ArgumentParser()
parser.add_argument('--train', action='store_true', help='Train if this flag is set, otherwise test')
parser.add_argument('--save_file', type=str, default=None)
parser.add_argument('--overwrite', action='store_true', help='Overwrite training the existing model')
parser.add_argument('--verbose', action='store_true')
parser.add_argument('--use_summary', action='store_true')
parser.add_argument('--n_epochs', type=int, default=1000)
args = parser.parse_args()

if args.overwrite and not args.train:
    raise Exception('--overwrite flag should only be used with --train flag')

indices_list = [[(i,j) for j in range(4)] for i in range(4)]
indices_list += [[(i,j) for i in range(4)] for j in range(4)]
tmp = [[(0, 0), (0, 1), (1, 1), (1, 0)],
[(0, 1), (0, 2), (1, 2), (1, 1)],
[(0, 2), (0, 3), (1, 3), (1, 2)]]
indices_list += tmp
indices_list += [[(tmp[i][j][0] + 1, tmp[i][j][1]) for j in range(4)] for i in range(3)]
indices_list += [[(tmp[i][j][0] + 2, tmp[i][j][1]) for j in range(4)] for i in range(3)]

N = 4
M = len(indices_list)
C = 17

save_file = args.save_file
writer = SummaryWriter() if args.use_summary else None

# Load or create a new instance
if args.train:  # For Train
    if os.path.isfile(save_file) and args.overwrite:
        print('Loading from', save_file)
        game = pickle.load(open(save_file, 'rb'))
    else:
        print('Initializing from scratch')
        game = PlayGame(N, M, indices_list, C)
else:  # For Test
    if not os.path.isfile(save_file):
        raise FileNotFoundError(save_file, 'doesn\'t exist')
    else:
        print('[Test] Loading from', save_file)
        game = pickle.load(open(save_file, 'rb'))
        save_file = None

game.run(save_file=save_file, writer=writer, n_epochs=args.n_epochs,
         is_learning=args.train, verbose=args.verbose)