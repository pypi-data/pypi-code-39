import matplotlib.pyplot as plt
import time as timelib

def boxplot(session_data, cluster_type, features, filename = None,verbose = False):
    """
    Plot boxplots of the sessions features given in entry
    """
    if verbose== True:
        start_time = timelib.time()
        print("\n   * Plotting boxplots ...")
        
    n_plots = len(features)
    fig,ax=plt.subplots(1,n_plots,figsize=(16,4))
    axis_counter=0
    cluster_ids = session_data[cluster_type].unique()
    cluster_ids.sort()
    for feature in features:
        feature_boxplot_data = [] 
        for c_id in cluster_ids:
            feature_boxplot_data.append(session_data[session_data[cluster_type]==c_id][feature].values)
        ax[axis_counter].boxplot(feature_boxplot_data,showfliers=False)
        ax[axis_counter].set_xticklabels(cluster_ids)
        for tick in ax[axis_counter].xaxis.get_major_ticks():
                tick.label.set_fontsize(10) 
        for tick in ax[axis_counter].yaxis.get_major_ticks():
                tick.label.set_fontsize(10)
        ax[axis_counter].set_title(features[axis_counter])
        axis_counter+=1
    ax[2].set_xlabel('\nCluster',fontsize=18)
    plt.tight_layout()
    if filename is not None:
        plt.savefig('../Figures/%s.pdf'%filename)
    plt.show()
    plt.clf()
    plt.close()
    
    if verbose == True:
        print("     Boxplots plotted in %.1f seconds."%(timelib.time() - start_time))
    return;