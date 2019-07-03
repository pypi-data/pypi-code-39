import torch
from torch.utils.data import Dataset


class NDArrayDataset(Dataset):
    def __init__(self, *arrays):
        if not all(len(arrays[0]) == len(array) for array in arrays):
            raise ValueError("All arrays must have the same length")
        self.arrays = arrays

    def __getitem__(self, idx):
        return tuple(torch.as_tensor(array[idx]) for array in self.arrays)

    def __len__(self):
        return len(self.arrays[0])


__all__ = ["NDArrayDataset"]
