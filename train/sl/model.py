import torch
import torch.nn.functional as F
from torch import nn

class CNN2048(nn.Module):
    def __init__(self, d_h=222):
        super().__init__()
        self.conv1 = nn.Conv2d(16, d_h, 2, stride=1)
        self.conv2 = nn.Conv2d(d_h, d_h, 2, stride=1)
        self.conv3 = nn.Conv2d(d_h, d_h, 2, stride=1)
        self.conv4 = nn.Conv2d(d_h, d_h, 2, stride=1)
        self.conv5 = nn.Conv2d(d_h, d_h, 2, stride=1)
        self.fc = nn.Linear(4 * 4 * d_h, 4)
    
    def forward(self, x):
        x = F.pad(x, (0,1,0,1))
        x = torch.relu(self.conv1(x))
        x = F.pad(x, (0,1,0,1))
        x = torch.relu(self.conv2(x))
        x = F.pad(x, (0,1,0,1))
        x = torch.relu(self.conv3(x))
        x = F.pad(x, (0,1,0,1))
        x = torch.relu(self.conv4(x))
        x = F.pad(x, (0,1,0,1))
        x = torch.relu(self.conv5(x)) # size(x)=(N, C, 4, 4)
        x = x.flatten(start_dim=1)
        x = self.fc(x) # size(x) = (N, 4)
        return torch.softmax(x, dim=1)


# class CNN2048(nn.Module):
#     def __init__(self, device=None):
#         super().__init__()
#         #self.device = device
#         self.conv1 = nn.Conv2d(16, 256, kernel_size=2)
#         self.conv2 = nn.Conv2d(256, 256, kernel_size=2)
#         self.conv3 = nn.Conv2d(256, 256, kernel_size=2)
#         self.conv4 = nn.Conv2d(256, 256, kernel_size=2)

#         self.norm1 = nn.BatchNorm2d(256)
#         self.norm2 = nn.BatchNorm2d(256)
#         self.norm3 = nn.BatchNorm2d(256)
#         self.norm4 = nn.BatchNorm2d(256)

#         self.fc = nn.Linear(256 * 4 * 4, 4)
    
#     def forward(self, x):
#         x = F.pad(x, (0,1,0,1)) 
#         x = torch.relu(self.norm1(self.conv1(x)))
#         x = F.pad(x, (0,1,0,1)) 
#         x = torch.relu(self.norm2(self.conv2(x)))
#         x = F.pad(x, (0,1,0,1)) 
#         x = torch.relu(self.norm3(self.conv3(x)))
#         x = F.pad(x, (0,1,0,1)) 
#         x = torch.relu(self.norm4(self.conv4(x)))
#         x = x.view(x.size(0), -1)
#         x = self.fc(x)
#         #print(x.detach().numpy())
#         return torch.softmax(x, dim=1)
#         # return x
    
    # def encode_board(self, board: Tensor, bsz: int):
    #     output = torch.zeros(bsz,16,4,4, device=self.device)
    #     #print(output.shape, board.shape)
    #     for i in range(16):
    #         output[:,i,:,:].masked_fill_(torch.from_numpy(board == i).to(self.device), 1)
    #     return output # (bsz, 16, 4, 4)