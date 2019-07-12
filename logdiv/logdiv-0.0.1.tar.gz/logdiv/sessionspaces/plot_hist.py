import matplotlib.pyplot as plt
import numpy as np

def hist1D(feature, log_scale = False, filename = None):
    feature.hist(bins = 15)
    if log_scale:
        plt.yscale('log')
        plt.xscale('log')
    plt.grid(axis="x")
    plt.xlabel('%s'%feature.name)
    plt.ylabel('numbers of sessions')
    plt.title('%s histogram 1D'%feature.name)
    if filename is not None:
        plt.savefig("../Figures/%s.pdf"%filename)
    plt.show()
    plt.close()
    return;    
    
def hist2D(features_1, features_2, log_scale = False, filename = None):
    fig, ax= plt.subplots()
    _,_,_,im = ax.hist2d(features_1.values,features_2.values, bins = 10)
    plt.colorbar(im)
    if log_scale:
        plt.yscale('log')
        plt.xscale('log')
    plt.xlabel('%s'%features_1.name)
    plt.ylabel('%s'%features_2.name)
    plt.title('%s %s histogram 2D'%(features_1.name,features_2.name))
    if filename is not None:
        plt.savefig("../Figures/%s.pdf"%filename)
    plt.show()
    plt.close()
    return;
    
    
def plot_hist_requests(session_data, threshold, filename = None):
    text_box=[]
    for reqs in range(1,threshold+1):
        num_of_reqs=session_data[session_data.requests==reqs].shape[0]
        pc_of_reqs=100.0*num_of_reqs/session_data.shape[0]
        text_box.append('Sessions with    {} req.: {:>7} ({:5.1f}%)'.format(reqs,num_of_reqs,pc_of_reqs))
    num_of_reqs=session_data[session_data.requests>threshold].shape[0]
    pc_of_reqs=100.0*num_of_reqs/session_data.shape[0]
    text_box.append('Sessions with >{} req.: {:>8} ({:5.1f}%)'.format(reqs,num_of_reqs,pc_of_reqs))        
    min_value=session_data.requests.values.min()
    max_value=session_data.requests.values.max()
    fig, ax = plt.subplots()
    bincuts=np.linspace(start=min_value-0.5,stop=max_value+0.5,num=(max_value-min_value+2),endpoint=True)
    ax.grid()
    ax.hist(session_data.requests.values,bins=bincuts, edgecolor='black', linewidth=0.8,zorder=3)
    ax.set_xscale("log", nonposx='clip')
    ax.set_yscale("log", nonposy='clip')
    props = dict(boxstyle='round', facecolor='wheat', alpha=1.0)
    ax.text(0.35,0.9,'\n'.join(text_box), transform=ax.transAxes, fontsize=10,
    verticalalignment='top', bbox=props)
    plt.xlabel('Number of Requests')
    plt.ylabel('Number of Sessions')
    if filename is not None:
        fig.savefig('../Figures/%s.pdf'%filename, format='pdf')
    plt.show()
    plt.clf()
    plt.close()