from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import time as timelib
import numpy as np
import pandas as pd

def compute_pca(session_data, session_features, cluster_types, verbose = False):
    if verbose == True:
        start_time = timelib.time()
        print("\n   * Principal component analysis ...")
        
    pca = PCA()
    column_names = ['pc%d'%i for i in range(1,len(session_features)+1)]
    session_data_reduced = pca.fit_transform(session_data[session_features])
    session_data_reduced = pd.DataFrame(data = session_data_reduced,columns = column_names, index = session_data.index)
    for cluster_type in cluster_types:
        session_data_reduced[cluster_type] = session_data_reduced.index.map(session_data[cluster_type])
    if verbose == True:
        print("     Principal component analysis completed in %.1f seconds"%(timelib.time() - start_time))
    return session_data_reduced, pca.explained_variance_ratio_, pca.components_;

def plot_explained_variance(explained_variance_ratio, threshold_explained_variance = 0.8, verbose = False, filename = None):
    """
    Plot explained variance of each princpal components
    """
    if verbose == True:
        start_time = timelib.time()
        print("\n   * Plotting explained variance ratio of all components from PCA ...")
        
    list_pc = []
    for i in np.arange(1,explained_variance_ratio.shape[0]+1):
        list_pc.append("C"+str(i))
    x = np.arange(explained_variance_ratio.shape[0])
    n_components_threshold = len(explained_variance_ratio[explained_variance_ratio.cumsum()<threshold_explained_variance]) +1
    plt.scatter(x,explained_variance_ratio)
    plt.axvline(x = n_components_threshold - 1, label = "%.1f of cumulated\n explained variance"%threshold_explained_variance, color = 'r', linewidth = 0.5)
    plt.xticks(x, list_pc)
    plt.grid(axis='y', linestyle='--')
    plt.xlabel("Components")
    plt.ylabel("Explanied variance ratio")
    plt.title("Explained variance ratio of each component")
    plt.legend()
    if filename is not None:
        plt.savefig("../Figures/%s.pdf"%filename)
    plt.show()

    if verbose == True:
        print("    Plot completed in %.1f seconds."%(timelib.time() - start_time))
    return;

def scatterplot(session_data_pca, components, feature_names, cluster_type, verbose = False, filename = None):
    """
    Plot scatterplot of sessions along PC1 and PC2 axis, and the composition of these two components, 
    with sessions colored in function of their cluster
    """
    if verbose == True:
        start_time = timelib.time()
        print("\n   * Plotting scatterplot of Principal Component 1 and 2 ...")
        
    plt.figure()
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(8,4))
    rows = feature_names
    rows = ['Nb de requêtes','Durée','Star-chain \nIndex','Écart type durée \nentre requêtes','Durée moyenne \nentre requêtes']
    columns = ["PC-1","PC-2"]
    matrix = np.transpose(components)
    ax1.matshow(matrix, cmap="coolwarm", clim=[-1, 1])
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            c = matrix[i,j]
            ax1.text(j,i, '%0.2f'%c, va='center', ha='center', color="k", size=10)
    ax1.set_xticks(range(2))
    ax1.set_yticks(range(len(feature_names)))
    ax1.set_xticklabels(columns)
    ax1.set_yticklabels(rows)
    cluster_ids = session_data_pca[cluster_type].unique()
    cluster_ids.sort()
    for cluster_id in cluster_ids:
        ax2.scatter(session_data_pca[session_data_pca[cluster_type]==cluster_id].pc1,\
                    session_data_pca[session_data_pca[cluster_type]==cluster_id].pc2,label=str(cluster_id))
    ax2.legend(title = 'cluster_id')
    ax2.set_xlabel("PC-1")
    ax2.set_ylabel("PC-2")
    ax2.set_title("Scatterplot of PC-1 and PC-2")
    ax2.invert_yaxis()
    if filename is not None:
        plt.savefig("../Figures/%s.png"%filename)
    plt.show() 
    
    if verbose == True:
        print("    Plot completed in %.1f seconds."%(timelib.time() - start_time))
    return;

def scatterplot_centroids(session_data_pca,cluster_type,components,feature_names,filename = None,verbose = False):
    """
    Plot scatterplot of the centroids of each clustera long PC1 and PC2 axis, and the composition of these two components
    """
    if verbose == True:
        start_time = timelib.time()
        print("\n   * Plotting scatterplot with clusters of Principal Component 1 and 2 ...")
        
    plt.figure()
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(8,4))
    # Explanation of components
    rows = feature_names
    columns = ["PC-1","PC-2"]
    matrix = np.transpose(components)
    ax1.matshow(matrix, cmap="coolwarm", clim=[-1, 1])
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            c = matrix[i,j]
            ax1.text(j,i, '%0.2f'%c, va='center', ha='center', color="k", size=10)
    ax1.set_xticks(range(2))
    ax1.set_yticks(range(len(feature_names)))
    ax1.set_xticklabels(columns)
    ax1.set_yticklabels(rows)
    # Scatterplot of clusters
    num_cluster = session_data_pca[cluster_type].unique()
    num_cluster.sort()
    ax2.axis('equal')
    ax2.set_xlabel('PC-1',fontsize=16)
    ax2.set_ylabel('PC-2',fontsize=16)
    xlim_min = np.array([session_data_pca[session_data_pca[cluster_type]==cluster_id].pc1.mean()-\
                         50*(session_data_pca[session_data_pca[cluster_type]==cluster_id].\
                                shape[0]/session_data_pca.shape[0])for cluster_id in num_cluster]).min()
    xlim_max = np.array([session_data_pca[session_data_pca[cluster_type]==cluster_id].pc1.mean()+\
                         50*(session_data_pca[session_data_pca[cluster_type]==cluster_id].\
                                shape[0]/session_data_pca.shape[0])for cluster_id in num_cluster]).max()
    ylim_min = np.array([session_data_pca[session_data_pca[cluster_type]==cluster_id].pc2.mean()-\
                         50*(session_data_pca[session_data_pca[cluster_type]==cluster_id].\
                                shape[0]/session_data_pca.shape[0])for cluster_id in num_cluster]).min()
    ylim_max = np.array([session_data_pca[session_data_pca[cluster_type]==cluster_id].pc2.mean()+\
                         50*(session_data_pca[session_data_pca[cluster_type]==cluster_id].\
                                shape[0]/session_data_pca.shape[0])for cluster_id in num_cluster]).max()
    ax2.set_xbound(xlim_min,xlim_max)
    ax2.set_ybound((ylim_min,ylim_max))
    #ax2.set_xlim((-1.5,1.75))
    #ax2.set_ylim((-1.5,1.5))
    ax2.invert_yaxis()
    # Labeling the clusters
    for cluster_id in num_cluster:
        # Cluster_size
        cluster_size=10000*(session_data_pca[session_data_pca[cluster_type]==cluster_id].shape[0]/session_data_pca.shape[0])
        # Cluster label
        cluster_label = str(cluster_id)
        # Plotting the circles
        ax2.scatter(session_data_pca[session_data_pca[cluster_type]==cluster_id].pc1.mean(),\
                    session_data_pca[session_data_pca[cluster_type]==cluster_id].pc2.mean(),\
                    marker='o', c="white", alpha = 0.8, s=cluster_size, edgecolor='k')
        # Plotting the cluster label
        ax2.scatter(session_data_pca[session_data_pca[cluster_type]==cluster_id].pc1.mean(),\
                    session_data_pca[session_data_pca[cluster_type]==cluster_id].pc2.mean(),\
                    marker='$%s$' % (cluster_label), alpha=0.9, s=50, edgecolor='k')
    plt.tight_layout()
    if verbose == True:
        print("    Plot completed in %.1f seconds."%(timelib.time() - start_time))
    if filename is not None:
        plt.savefig("../Figures/%s.pdf"%filename)
    plt.show()
    plt.clf()
    plt.close()
    return;
    
