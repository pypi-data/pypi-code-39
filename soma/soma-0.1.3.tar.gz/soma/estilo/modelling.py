import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from seaborn import heatmap
from typing import List, Tuple
import pandas as pd


def correlation_matrix(m: np.ndarray, labels: List[str] = None) -> np.ndarray:
    """
        Calculates a correlation matrix given a :math:`[N_{samples} \\times N_{features}]` data matrix.
        
        This correlation is composed of the Pearson Correlation Coefficient
        between each pair of features.

        Args:
            m (:class:`numpy.ndarray`): 
                A :math:`[N_{samples} \\times N_{features}]` data matrix.
            labels (list(str)): 
                A list of n_features labels.

        Returns:
            :class:`numpy.ndarray`: The resulting :math:`[N_{features} \\times N_{features}]` correlation matrix.
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
        Calculates a :math:`[N_{samples} \\times N_{samples}]` distance matrix given a :math:`[N_{samples} \\times N_{features}]` data matrix. 

        Args:
            m (:class:`numpy.ndarray`): A :math:`[N_{samples} \\times N_{features}]` data matrix.

        Returns:
            :class:`numpy.ndarray`: The resulting :math:`[N_{samples} \\times N_{samples}]` distance matrix.
    """
    from scipy.spatial.distance import pdist, squareform

    dist_matrix = squareform(pdist(m))

    fig, ax = plt.subplots()
    ax.set_aspect(1)
    sns.heatmap(dist_matrix, annot=False, linewidths=0.5, ax=ax)
    ax.set_xlabel("Sample")
    ax.set_ylabel("Sample")
    return dist_matrix


def distance_orderner(dist_matrix: np.ndarray) -> Tuple[np.array, np.array]:
    """
        Calculates an ordered total distance (useful for finding outliers) and plots it.
        
        Args:
            dist_matrix (:class:`numpy.ndarray`): A [N x N] distance matrix.
        
        Returns:
            (tuple): Tuple contaning:
                - dists (:class:`numpy.ndarray`): Total distance for each sample.
                - i_dists (:class:`numpy.ndarray`): Indexes used to sort dists.
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


def clean_animale_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
        Cleans the animale sales dataset.

        It excludes infinite, zero quantities and NaN entries from the DataFrame.

        Args:
            df (:class:`pandas.Dataframe`): The animale sales dataset.

        Returns:
            The cleaned dataset.
    """
    df.drop_duplicates(subset="id_produto_cor", keep=False, inplace=True)
    df["qtde"].replace(0, np.nan, inplace=True)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def load_provao_dataset(
    path_animale: str, path_provao: str
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
        Loads the animale sales dataset (with sales indicators) and the votes dataset.

        Args:
            path_animale (str): Path to the animale dataset in Pickle format.
            path_provao (str): Path to the provao dataset in CSV format.
        
        Returns:
            (tuple): Tuple contaning:
                - df_merged (:class:`pandas.Dataframe`): A merged dataset from animale and provao.
                - df_animale (:class:`pandas.Dataframe`): Animale sales dataset.
                - df_provao (:class:`pandas.Dataframe`): Provao dataset      
    """

    df_animale = pd.read_pickle(path_animale)
    df_provao = pd.read_csv(path_provao)

    df_provao = df_provao.rename(columns={"preco": "nota_preco"})
    df_provao.drop(columns=["id_colecao", "id_produto_estilo", "produto"], inplace=True)

    df_animale = clean_animale_dataset(df_animale)
    df_animale.rename(columns={"preco_varejo_original": "preco"}, inplace=True)

    df_merged = df_animale.merge(df_provao, on="id_produto_cor")
    return df_merged, df_animale, df_provao


# test_func = load_provao_dataset('P:/Artur Lemos/Aposta/export/dataset_animale.pkl', 'P:/Artur Lemos/Aposta/export/voto_provao_online.csv')

""

