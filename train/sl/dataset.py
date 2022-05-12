import torch
from torch.utils.data import Dataset
from torch import Tensor
#from tqdm import tqdm
from typing import Tuple

class BoardDataset(Dataset):
    def __init__(self, filename):
        self.data = []
        with open(filename, 'r') as f:
            for line in f:
                if line.strip() == '':
                    print('Empty line here')
                    continue
                # if line == '\n':
                #     continue
                line = line.split(' ')
                sample = []
                sample.extend(list(map(int, line[1:17]))) # data
                sample.append(int(line[18])) # label
                sample.append(int(line[19].strip())) # prev tile position
                assert len(sample) == 18
                self.data.append(sample)

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx) -> Tuple[Tensor, Tensor, Tensor]:
        # if self.transform:
        #     sample = self.transform(self.data[idx])
        sample = self.data[idx]
        data = torch.Tensor([sample[:16]])
        label = torch.Tensor([sample[16]])
        prev_pos = torch.Tensor([sample[17]])
        return data, label, prev_pos

if __name__ == '__main__':
    from glob import glob
    import torchvision
    transforms = torchvision.transforms.ToTensor()
    file = './data/shuffle_00a.txt'
    dataset = BoardDataset(file)



