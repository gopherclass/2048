import torch
import torch.onnx
from model import CNN2048

def main():
    model = CNN2048()
    model.load_state_dict(torch.load('./model/model3.pth', map_location=torch.device('cpu')))
    model.eval()
    dummy_input = torch.zeros((1, 16, 4, 4))
    torch.onnx.export(model, dummy_input, 'model/onnx_model3.pth', verbose=True)

if __name__ == '__main__':
    main()

