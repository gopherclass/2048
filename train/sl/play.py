from numpy import ndarray
import torch
from model import CNN2048
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
n_games = 100
if model_path is not None:
    model.load_state_dict(torch.load(model_path))
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
    return board.score

score_total = 0
for i in range(n_games):
    score = play_game(verbose=False)
    score_total += score
    print(f'==== Game {i} Score: {score} ======\n')
print('===== Average Score:', score_total/n_games)
