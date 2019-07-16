from . import matrix_calculator
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import time as timelib

def classification_diversity(weblog, categories, threshold_requests_per_session, verbose = False):
    """
    Calculate matrices using matrix_calculator.py. Select requested_category and referrer_category of weblog that are in entry "categories"
    """
    if verbose== True:
        start_time = timelib.time()
        print("\n   * Computing matrix ...")
    # Selecting sessions with more than N requests
    requests_per_session=weblog.groupby('session_id').size()
    sessions_requests_over_threshold=list(requests_per_session[requests_per_session>threshold_requests_per_session].index)
    divpat_log = weblog[weblog.session_id.isin(sessions_requests_over_threshold)]
    # Filtering some requests
    divpat_log=divpat_log[divpat_log.requested_category.isin(categories)]
    divpat_log=divpat_log[divpat_log.referrer_category.isin(categories)]
    # Defining matrices
    diversity_columns=('referrer_topic','requested_topic')
    browsing_matrix,_ = matrix_calculator.compute_browsing_matrix(divpat_log,'referrer_category','requested_category',labels=categories)
    markov_matrix,_ = matrix_calculator.compute_markov_matrix(divpat_log,'referrer_category','requested_category',labels=categories)
    diversifying_matrix,_ = matrix_calculator.compute_diversifying_matrix(divpat_log,'referrer_category','requested_category',\
                                                                             diversity_columns,labels = categories,threshold=2)
    # Selecting sessions only with requests that have changed topic
    divpat_log = divpat_log[divpat_log.requested_topic != divpat_log.referrer_topic]
    change_browsing_matrix,_ = matrix_calculator.compute_browsing_matrix(divpat_log,'referrer_category','requested_category',labels=categories)

    if verbose == True:
        print("     Matrix computed in %.1f seconds."%(timelib.time() - start_time))
    return browsing_matrix, markov_matrix, diversifying_matrix,change_browsing_matrix;

def plot_pattern_matrix(matrix,categories,ticks_theme='inclined',title='',xlabel='',ylabel='',\
                        text_place = 'fig', fs=12,xlabelfs=18,filename = None,verbose = False):
    """
    Plot matrix with heatmap method 
    """
    if verbose== True:
        start_time = timelib.time()
        print("\n   * Plotting matrix ...")
        
    fig, ax = plt.subplots(figsize=(6,6))
    #heatmap
    image = ax.imshow(matrix,cmap="YlGn")
    ax.figure.colorbar(image, ax=ax)
    ax.set_xticks(np.arange(matrix.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(matrix.shape[0]+1)-.5, minor=True)
        
    if ticks_theme=='inclined':
        ax.set_xticklabels(categories, rotation=45,ha='left')
        ax.set_yticklabels(categories, rotation=45)
        
    elif ticks_theme=='abreviation':
        ticks = [cat[:2] for cat in categories]
        text_box = []
        for ind,tick in enumerate(ticks):
            counter=2
            while ticks.count(tick)>1:
                counter+=1
                indices = [i for i, x in enumerate(ticks) if x == tick]
                for index in indices: 
                    ticks[index]=categories[index][:counter]
                tick = categories[ind][:counter]
            text_box.append('%s: %s'%(tick,categories[ind]))
        props = dict(boxstyle='round', facecolor='wheat', alpha=1.0)
        if text_place=='fig':
            ax.text(0.25,1.7,'\n'.join(text_box), transform=ax.transAxes, fontsize=10,
                    verticalalignment='top', bbox=props)                   
        ax.set_xticklabels(ticks, rotation=45,ha='left')
        ax.set_yticklabels(ticks, rotation=45)
        
    elif ticks_theme=='greek':
        greek_letters = ['\u03b1','\u03b2','\u03b3','\u03b4','\u03b5',\
                         '\u03b6','\u03b7','\u03b8','\u03b9','\u03ba',\
                         '\u03bb','\u03bc','\u03bd','\u03be','\u03bf']
        text_box = []
        ticks = []
        for i in range(len(categories)):
            text_box.append('%s : %s'%(greek_letters[i],categories[i]))
            ticks.append(greek_letters[i])
        props = dict(boxstyle='round', facecolor='wheat', alpha=1.0) 
        if text_place=='fig':
            ax.text(0.25,1.4,'\n'.join(text_box), transform=ax.transAxes, fontsize=10,
                    verticalalignment='top', bbox=props)           
        ax.set_xticklabels(ticks)
        ax.set_yticklabels(ticks)
        
    elif ticks_theme == 'dict':
        text_box = []
        ticks = []
        for key in sorted(categories.keys()):
            text_box.append('%s : %s'%(key,categories[key]))
            ticks.append(key)
        props = dict(boxstyle='round', facecolor='wheat', alpha=1.0) 
        if text_place=='fig':
            ax.text(0.25,1.4,'\n'.join(text_box), transform=ax.transAxes, fontsize=10,
                    verticalalignment='top', bbox=props)           
        ax.set_xticklabels(ticks)
        ax.set_yticklabels(ticks)        
                
    ax.set_xlabel(xlabel,fontsize=xlabelfs)
    ax.set_ylabel(ylabel)
    ax.xaxis.set_tick_params(labelsize=fs)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(fs)
        ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)
    for edge, spine in ax.spines.items():
        spine.set_visible(False)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=7)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.axvline(len(categories)-1.5, linestyle='-', color='r')
    ax.axhline(len(categories)-1.5, linestyle='-', color='r')
    textcolors=["black", "white"]
    if not isinstance(matrix, (list, np.ndarray)):
        matrix = image.get_array()
        #    threshold = image.norm(np.nanmax(ax.set_yticks(np.arange(matrix.shape[0]+1)-.5, minor=True)))/2.
    threshold=0.5*(np.nanmax(matrix)-np.nanmin(matrix))
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    valfmt = matplotlib.ticker.StrMethodFormatter("{x:.2f}")
    texts = []
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if np.isnan(matrix[i,j]):
                text = image.axes.text(j, i, 'X',fontsize=fs)
                texts.append(text)
            else:
                kw.update(color=textcolors[image.norm(matrix[i, j]) > threshold])
                text = image.axes.text(j, i, valfmt(matrix[i, j], None),fontsize=fs, **kw)
                texts.append(text)
    fig.tight_layout()
    if filename is not None:
        plt.savefig("/home/alexandre/Documents/Melty/Experience/%s.pdf"%filename, bbox_inches = 'tight')
        #plt.savefig("/home/alexandre/Documents/alex/Figures/%s.pdf"%filename, bbox_inches = 'tight')
    plt.show() 
    
    if text_place == 'separate':
        fig, ax = plt.subplots(figsize=(1,1))
        ax.text(0,1,'\n'.join(text_box), transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=props) 
        plt.axis('off')
        plt.savefig("/home/alexandre/Documents/alex/Figures/test.pdf", bbox_inches = 'tight')
        plt.show()
    
    if verbose == True:
        print("     Matrix plotted in %.1f seconds."%(timelib.time() - start_time))
    plt.clf()
    plt.close()
    return;
    
def classification_tex(f, weblog, threshold_requests_per_session,categories,weblog_columns_dict):
    """
    Write on latex file information variables on classification
    """
    categories = list(set(categories)-{'social','search','other'})

    
    requests_per_session=weblog.groupby('session_id').size()
    sessions_requests_over_threshold=list(requests_per_session[requests_per_session>threshold_requests_per_session].index)
    divpat_log = weblog[weblog.session_id.isin(sessions_requests_over_threshold)]
    #divpat_log=divpat_log[(divpat_log.referrer_external == False)&(divpat_log.requested_external == False)]
    num_reqs_inside=divpat_log.shape[0]
    divpat_log=divpat_log[~divpat_log.requested_category.isin(['social','search','other'])]
    divpat_log=divpat_log[~divpat_log.referrer_category.isin(['social','search','other'])]
    num_reqs_selected_cats=divpat_log.shape[0]
    
    #divpat_log=divpat_log[divpat_log.requested_category.isin(categories)]
    
    f.write("\n% 5. Diversifying patterns according to classification")
    f.write("\n\\newcommand{\\%s}{%.1f}"%('PCDivPatTotalSelectedCat',100.0*num_reqs_selected_cats/num_reqs_inside))
    f.write("\n\\newcommand{\\%s}{%d}"%('DivPatTotalNumberRequests',divpat_log.shape[0]))
    f.write("\n\\newcommand{\\%s}{%d}"%('DivPatTotalNumberUsers',len(divpat_log.userID.unique())))
    f.write("\n\\newcommand{\\%s}{%d}"%('DivPatTotalNumberSessions',len(divpat_log.session_id.unique())))
    f.write("\n\\newcommand{\\%s}{%d}"%('DivPatTotalNumberPages',len(list(set(divpat_log[weblog_columns_dict['requested_page_column']].unique())|
            set(divpat_log[weblog_columns_dict['referrer_page_column']].unique())))))  
    return f;

def matrix_tex(f, browsing_matrix, diversifying_matrix, categories):
    """
    Write on latex file the most 
    """
    digit_dic={'0':'Zero','1':'One','2':'Two','3':'Three','4':'Four','5':'Five','6':'Six','7':'Seven','8':'Eight','9':'Nine'}
    divpat_categories = list(set(categories)-{'social','search','other'})
    divpat_N_categories=len(divpat_categories)
    # Browsing patterns
    r,c=np.unravel_index(browsing_matrix[:-1,:-1].argsort(axis=None)[::-1][:3],dims=(divpat_N_categories,divpat_N_categories))
    
    for i in range(3):
        f.write("\n\\newcommand{\\%s}{%s}"%('GlobalBP%sName'%(digit_dic[str(i+1)]),'%s$\\rightarrow$%s'%(divpat_categories[r[i]],divpat_categories[c[i]])  ))
        f.write("\n\\newcommand{\\%s}{%0.1f}"%('GlobalBP%sValue'%(digit_dic[str(i+1)]),100.0*browsing_matrix[r[i],c[i]]))
    #  Diversifying patterns
    r,c=np.unravel_index(np.nan_to_num(diversifying_matrix)[:-1,:-1].argsort(axis=None)[::-1][:3],dims=(divpat_N_categories,divpat_N_categories))
    for i in range(3):
        f.write("\n\\newcommand{\\%s}{%s}"%('GlobalDP%sName'%(digit_dic[str(i+1)]),'%s$\\rightarrow$%s'%(divpat_categories[r[i]],divpat_categories[c[i]])  ))
        f.write("\n\\newcommand{\\%s}{%0.1f}"%('GlobalDP%sValue'%(digit_dic[str(i+1)]),100.0*diversifying_matrix[r[i],c[i]]))
    return f;
