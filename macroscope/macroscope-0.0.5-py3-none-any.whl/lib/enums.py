from enum import Enum


class ClosestSearchMethod(Enum):
    SVD = 'svd'
    SGNS = 'sgns'


class NetworkMethod(Enum):
    PMI = 'PMI'
    COR = 'COR'


class Reduce(Enum):
    PCA = 'pca'
    TSNE = 't-sne'
