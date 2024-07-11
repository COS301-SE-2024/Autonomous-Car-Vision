import sys
import torch

def check_cuda_availability():
    return torch.cuda.is_available()

if __name__ == "__main__":
    result = check_cuda_availability()
    print(result)
    sys.exit(0)