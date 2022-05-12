import torch
import os, random
import numpy as np
import torch.nn.functional as F
from model import CNN2048
from glob import glob
from dataset import BoardDataset
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from argparse import ArgumentParser

writer = SummaryWriter()

# def data_iter(file):
#     with open(file, 'r') as f:
#         for line in f:
#             line = line.split(' ')
#             sample = []
#             data = list(map(int, line[1:17]))
#             label = int(line[18])
#             prev_pos = int(line[19].strip())
#             yield data, label, prev_pos

# def make_batch(iterator, batch_size):
#     batch = []

def encode_board(board):
    bsz = board.shape[0]
    board = board.view(bsz, 4, 4)
    output = torch.zeros(bsz,16,4,4)
    for i in range(16):
        output[:,i,:,:].masked_fill_(board == i, 1)
    return output


parser = ArgumentParser()
parser.add_argument('--bsz', type=int, default=1000)
parser.add_argument('--lr', type=float, default=0.001)
parser.add_argument('--milestone', type=int, default=100)
parser.add_argument('--gpu', dest='device', action='store_const', const=torch.device('cuda'), default=torch.device('cpu'))
parser.add_argument('--epochs', type=int, default=1)
parser.add_argument('--path', dest='model_path', default=None)
args = parser.parse_args()
if args.model_path is None:
    exit()
print(args)
# class DotDict(dict):
#     def __getattr__(self, name):
#         return self[name]

# args = DotDict()
# args.bsz = 512
# args.lr = 0.01
# args.milestone = 100
# args.device = 'cuda' if torch.cuda.is_available() else 'cpu'
# args.model_path = './model/model.pth'

model = CNN2048().to(args.device)
# criterion = torch.nn.NLLLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

if os.path.isfile(args.model_path):
    ans = input('Would you like to load the model and continue training? (y/n)')
    if ans == 'y':
        model.load_state_dict(torch.load(args.model_path))

files_list = glob('./data/*.txt')
files_list.sort()
# for epoch in range(args.epochs):

    # random.shuffle(files_list)

for file in files_list:
    #record = []
    print('Loading Dataset from', file)
    dataset = BoardDataset(filename=file)
    dataloader = DataLoader(dataset, batch_size=args.bsz, shuffle=True) 
    
    i = 0
    acc_record, loss_record = [], []
    # size(data, label) = (bsz, 1, 16), (bsz, 1)
    for data, label, _ in dataloader:

        inputs = encode_board(data).to(args.device) # size(inputs)=(bsz, 16, 4, 4)
        probs = model(inputs) # size(probs)=(bsz, 4)
        action = probs.argmax(dim=1).float()  # size(action)=(bsz, )
        label = label.squeeze(1).to(args.device).long() # size(label)=(bsz, )
        label_one_hot = F.one_hot(label, 4) # size(label_one_hot)=(bsz, 4)

        #print(probs.shape, label.shape, action.shape, inputs.shape, data.shape, label.shape)
        optimizer.zero_grad()
        loss = - torch.sum(label_one_hot * torch.log(probs.clamp(1e-10, 1.0)))
        # loss = criterion(probs.clamp(1e-10, 1.0), label)
        loss.backward()
        optimizer.step()

        acc = (action == label).float().mean()
        acc_record.append(acc.item())
        loss_record.append(loss.item())
        #record = np.concatenate(record, [acc.item(), loss.item()])
        #record.append((acc.item(), loss.item()))
        # acc_record.append(float(action == label))
        # loss_record.append(loss.item())
        #total_record.append(float(action == label))

        if i % args.milestone == 0 and i != 0:
            # _acc = acc_record/(args.milestone+1)
            # _loss = loss_record/(args.milestone+1)
            # acc_record, loss_record = [], []
            tmp_acc = np.mean(acc_record)
            tmp_loss = np.mean(loss_record)
            print(f'\t{i}: Accuracy: {tmp_acc}, Loss: {tmp_loss}')
            torch.save(model.state_dict(), args.model_path)
            writer.add_scalar('Accuracy/train', tmp_acc, i)
            writer.add_scalar('Loss/train', tmp_loss, i)
            writer.flush()
        i += 1
 
    tmp_acc = np.mean(acc_record)
    tmp_loss = np.mean(loss_record)
    print(f'File: {file}, Accuracy: {tmp_acc}, Loss: {tmp_loss}')
    torch.save(model.state_dict(), args.model_path)
    writer.add_scalar('Accuracy/train', tmp_acc, i)
    writer.add_scalar('Loss/train', tmp_loss, i)
    writer.flush()

writer.close()
print(args)