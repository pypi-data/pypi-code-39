import pandas as pd
import time as timelib
import numpy as np
import matplotlib.pyplot as plt
from . import function
pd.options.mode.chained_assignment = None

def proportion_group(weblog, session_data,classification_column, classifications, group_names, verbose = False):
    """
    Calculate and return proportion_data: number of requests and entropy for each group
    
    Parameters
    ----------
        weblog: pandas dataframe of requests
        
        session_data: pandas dataframe of sessions
        
        classification_column: pandas dataframe column for proportion analysis
        
        classifications: list of items in classification_column wanted to be analysed
        
        group_names: list of sessions group wanted to analyse
        
    Returns
    -------
        Pandas Dataframe
        Numpy array
    """
    if verbose == True:
        start_time = timelib.time()
        print("\n   * Computing aggregated diversity ...")
        
    proportions_matrix=[]
    entropy_matrix = []
    
    # Groups
    for group_name in group_names:    
        list_sessions = session_data[session_data[group_name]].session_id.values
        weblog_tmp=weblog[weblog.session_id.isin(list_sessions)]
        weblog_tmp.loc[weblog_tmp[classification_column]=='None',classification_column]='Other'
        pa,pa_names = function.proportional_abundance(weblog_tmp,classification_column)
        pa = function.rearrange_pa_relative_labels(pa,classifications,pa_names)
        proportions_matrix.append(pa)
        entropy_matrix.append(function.ShannonEntropy(pa, normalize = True))
        
    del weblog_tmp

    # Total
    weblog=weblog.copy(deep=True)
    weblog.loc[weblog[classification_column]=='None',classification_column]='Other'
    pa,pa_names = function.proportional_abundance(weblog,classification_column)
    pa = function.rearrange_pa_relative_labels(pa,classifications,pa_names)
    proportions_matrix.append(pa)
    entropy_matrix.append(function.ShannonEntropy(pa, normalize = True))

    index_names = [group_name for group_name in group_names]
    index_names.append("Total")
    
    proportion_data = pd.DataFrame(data=proportions_matrix,columns=classifications,index=index_names)
    if verbose == True:
        print("     Aggregated diversity computed in %.1f seconds."%(timelib.time()-start_time))
    
    return proportion_data, entropy_matrix;

def plot_aggregated(proportion_data, entropy_matrix, threshold=2, filename = None):
    """
    Plot proportion data calculated with proportion_group or proportion
    
    Parameters
    ----------
        proportion_data: pandas dataframe from proportion_group analysis
        
        entropy_matrix: numpy array from proportion_group analysis
        
        threshold: int for lim of figure

    Returns
    -------
        None
    """
    ax=proportion_data.plot.barh(stacked=True,edgecolor='none')
    ax.legend(loc=7)
    ax.set_xlim((0,2.75))
    ax.set_ylim((-1,threshold+2.5))
    ax.text(1.1,threshold+2,'Entropy')
    ax.text(1.5,threshold+2,'IEUC')
    for y_tick in ax.get_yticks():
        ax.text(1.1,y_tick-0.1,'%.2f'%entropy_matrix[y_tick])
        ax.text(1.5,y_tick-0.1,'%.2f'%np.power(2.0,entropy_matrix[y_tick]))
    ax.set_xticklabels(['','','','','',''])
    plt.tight_layout()
    if filename is not None:
        plt.savefig('../Figures/%s.pdf'%filename)
    plt.show()
    plt.close()    
    return;
    
def aggregated_tex(f, entropy_matrix):
    """
    Write in latex file entropy of 6 groups (need to be change to adapt number of groups)
        
    Parameters
    ----------
        f: file
        
        entropy_matrix: numpy array from proportion_group analysis

    Returns
    -------
        File (Optionnal)
    """
    f.write("\n% 4. Aggregated Diversity")
    f.write("\n\\newcommand{\\%s}{%.2f}"%('EntropyGroupA',entropy_matrix[0]))
    f.write("\n\\newcommand{\\%s}{%.2f}"%('EntropyGroupB',entropy_matrix[1]))
    f.write("\n\\newcommand{\\%s}{%.2f}"%('EntropyGroupC',entropy_matrix[2]))
    f.write("\n\\newcommand{\\%s}{%.2f}"%('EntropyGroupD',entropy_matrix[3]))
    f.write("\n\\newcommand{\\%s}{%.2f}"%('EntropyGroupE',entropy_matrix[4]))
    f.write("\n\\newcommand{\\%s}{%.2f}"%('EntropyGroupF',entropy_matrix[5]))
    return f;
    


