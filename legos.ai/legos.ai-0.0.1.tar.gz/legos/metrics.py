import torch

def accuracy(pred, yb):
    '''
    Calculate accuracy for classification problem by:
    - Find the position of max value with argmax
    - Compare with the target values
    - Calculate the mean
    '''
    return (torch.argmax(pred, dim=1)==yb).detach().float().mean()
