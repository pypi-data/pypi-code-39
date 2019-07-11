import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

def get_torchvision_dataset(dataset, root:str, download:bool=True, transform:transforms.Compose=None, *args, **kwargs):
    """
    Create training set and validation set from a PyTorch Dataset
    Args:
        dataset (torch.utils.data.Dataset): a PyTorch Dataset
        root (str): Root directory of dataset. Pass into `dataset`
        download (bool, optional): Pass into `dataset`
        transform (calllable, optional): Pass into `dataset`
    Returns:
        train_ds (torch.utils.data.Dataset): training set
        valid_ds (torch.utils.data.Dataset): validation set
    """
    train_ds = dataset(root=root, train=True, transform=transform, **kwargs)
    valid_ds = dataset(root=root, train=False, transform=transform, **kwargs)
    return train_ds, valid_ds

def get_mnist(batch_size=256, download=True, root="../data"):
    transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307, ), (0.3081, ))])

    train_ds, valid_ds = get_torchvision_dataset(datasets.MNIST,
                                                 root=root,
                                                 download=download,
                                                 transform=transform)

    train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    valid_dl = DataLoader(valid_ds, batch_size=batch_size, shuffle=False)
    return train_dl, valid_dl