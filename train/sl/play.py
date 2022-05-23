import torch
from model import CNN2048
from numpy import ndarray
from board import Board
from glob import glob
from torch.distributions import Categorical
ACTIONS = ['UP', 'RIGHT', 'DOWN', 'LEFT']

def encode_board(board: ndarray):
    #bsz = board.shape[0]
    board = torch.from_numpy(board)
    output = torch.zeros(1,16,4,4)
    for i in range(16):
        output[:,i,:,:].masked_fill_(board == i, 1)
    return output

models = glob('./model/*.pth')
for i, model in enumerate(models):
    print(f'{i}: {model}')
print(f'{i+1}: None')
models.append(None)
model_number = int(input('Please choose the model: '))
model_path = models[model_number]

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = CNN2048().to(device)
n_games = 1000
if model_path is not None:
    model.load_state_dict(torch.load(model_path, map_location=device))
    print('Model loaded from', model_path)
else:
    exit()

def get_move(board: Board):
    with torch.no_grad():
        probs = model(encode_board(board.board).to(device))
    valid_a = board.valid_acts()
    for a in range(4):
        if a not in valid_a:
            probs[:,a] -= float('inf')
    action = probs.argmax(dim=1).item()
    # action = Categorical(probs).sample().item()
    return action

def play_game(verbose):
    board = Board()
    board.advance()
    board.advance()

    while True:
        action = get_move(board)
        board.step(action)
        board.advance()
        if verbose:
            print(f'MOVE to {ACTIONS[action]}({action}), Total Score: {board.score}')
            print(board)
        if len(board.valid_acts()) == 0:
            break
    return board

score_total = 0
max_score = -1
max_max_tile = 0
for i in range(n_games):
    board = play_game(verbose=False)
    score = board.score
    max_tile = 1 << board.max()
    score_total += score
    if score > max_score:
        max_score = score
    if max_tile > max_max_tile:
        max_max_tile = max_tile
    print(f'==== Game {i} Score: {score}, Max Tile: {max_tile} ======\n')
print(f'===== Average Score: {score_total/n_games}, Highest Score Reached: {max_score}, Highest Tile Reached: {max_max_tile} ======')
