import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List

def correlation_matrix(m: np.ndarray, labels: List[str] = None) -> np.ndarray:
    """
        Calculates a correlation matrix given a [n_samples x n_features] data matrix.
        
        This correlation is composed of the Pearson Correlation Coefficient between each 
        two pairs of features 

        Args:
            m (np.ndarray): A [n_samples x n_features] data matrix.
            labels (list(str)): A list of n_features labels.
        Returns:
            corr_matrix (np.ndarray): The resulting [n_features x n_features] correlation matrix.
    """
    corr_matrix = np.corrcoef(m)

    fig, ax = plt.subplots()
    ax.set_aspect(1)

    sns.heatmap(corr_matrix, annot=True, linewidths=0.5, ax=ax, fmt="1.3f")
    ax.set_title("Linear Correlation Matrix", fontweight="bold", fontsize=14)

    if labels:
        tick_marks = np.arange(len(labels))
        ax.xaxis.set_ticks(tick_marks)
        ax.xaxis.set_ticklabels(labels, rotation=90)
        ax.yaxis.set_ticks(tick_marks)
        ax.yaxis.set_ticklabels(labels)
    plt.show()
    return corr_matrix


def distance_matrix(m: np.ndarray) -> np.ndarray:
    """
        Calculates a [n_samples x n_samples] distance matrix given a [n_samples x n_features] data matrix. 

        Args:
            m (np.ndarray): A [n_samples x n_features] data matrix.
        Returns
            dist_matrix (np.ndarray): The resulting [n_samples x n_samples] distance matrix.
    """
    from scipy.spatial.distance import pdist, squareform

    dist_matrix = squareform(pdist(m))

    fig, ax = plt.subplots()
    ax.set_aspect(1)
    sns.heatmap(corr_matrix, annot=False, linewidths=0.5, ax=ax)
    ax.set_xlabel("Sample")
    ax.set_ylabel("Sample")
    return dist_matrix


def distance_orderner(dist_matrix: np.ndarray) -> np.array:
    """
        Calculates an ordered total distance (useful for finding outliers) and plots it.

        Args:
            dist_matrix (np.ndarray): A [N x N] distance matrix.
        
        Returns:
            dists (np.array): Total distance for each sample.
            i_dists (np.array): Indexes used to sort dists.
    """
    dists = np.sum(dist_matrix, axis=1)

    i_dists = np.argsort(dists)
    dists_ordered = dists[i_dists]

    fig, ax = plt.subplots()
    ax.set_aspect(1)
    sns.scatterplot(x=np.arange(0, dists.shape[0]), y=dists_ordered)
    ax.set_xlabel("Samples")
    ax.set_ylabel("Total Distance")

    return i_dists, dists

