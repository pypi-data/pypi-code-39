import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from graph_tool.all import Graph
from graph_tool.all import graph_draw
import time as timelib

def ShannonEntropy(P,normalize=False):
    P=np.array(P)
    if normalize:
        P=P/P.sum()
    P=P[P>1e-20]
    return -np.sum(P*np.weblog2(P));

def proportional_abundance(weblog,field):
    if weblog.shape[0]==0:
        raise AssertionError('Empty weblog.')
    histogram=weblog[field].value_counts()
    pa_df=histogram/histogram.values.sum()
    if abs(1.0-pa_df.values.sum())>1e-8:
        raise AssertionError("ERROR: Proportional abundance distribution does not sum up to one.")
    return pa_df.values,list(pa_df.index);

def session_draw_bis_melty(sessions_id, weblog,weblog_columns_dict):
    """
    Draw the graph of sessions with sessions_id given in entry
    """
    session = weblog[weblog.session_id==sessions_id]
    session = session.rename(index=str,columns = {weblog_columns_dict['requested_page_column']:'requested_page',\
                                                  weblog_columns_dict['referrer_page_column']:'referrer_page'})
    s_pages = session[['requested_page','requested_external']]
    s_pages_ref = session[['referrer_page','referrer_external']]
    s_pages_ref = s_pages_ref.rename(index = str, columns = {'referrer_page':'requested_page','referrer_external':'requested_external'})
    s_pages = s_pages.append(s_pages_ref)
    s_pages.drop_duplicates(subset = 'requested_page',inplace=True)
    g = Graph()
    v = {}
    halo = g.new_vertex_property("bool")
    for row in s_pages.itertuples():
        v[row.requested_page] = g.add_vertex()
        if row.requested_external:
            halo[v[row.requested_page]] = True
        else:
            halo[v[row.requested_page]] = False
    session.apply(lambda x: g.add_edge(v[x.referrer_page], v[x.requested_page]), axis=1)
    graph_draw(g, vertex_halo=halo, output="../graph_dump/_session"+str(sessions_id)+".png")
    return;
    
def session_draw_bis(sessions_id, weblog,weblog_columns_dict):
    """
    Draw the graph of sessions with sessions_id given in entry
    """
    session = weblog[weblog.session_id==sessions_id]
    session = session.rename(index=str,columns = {weblog_columns_dict['requested_page_column']:'requested_page',\
                                                  weblog_columns_dict['referrer_page_column']:'referrer_page'})
    s_pages = session['requested_page']
    s_pages_ref = session['referrer_page']
    #s_pages_ref = s_pages_ref.rename(index = str, columns = {'referrer_page':'requested_page'})
    s_pages = s_pages.append(s_pages_ref)
    s_pages.drop_duplicates(inplace=True)
    g = Graph()
    v = {}
    for page in s_pages.values:
        v[page] = g.add_vertex()
        
    session.apply(lambda x: g.add_edge(v[x.referrer_page], v[x.requested_page]), axis=1)
    graph_draw(g,output="../graph_dump/_session"+str(sessions_id)+".png")
    return;

def mosaic(session_data, weblog, features, type_cluster, weblog_columns_dict,filename = None, verbose = False):
    """
    Plot cluster mosaic: take the 5 most representatives sessions of each cluster, draw the graph of each of them, show the timespan
    and when requests are made along timespan axe
    """
    if verbose== True:
        start_time = timelib.time()
        print("\n   * Computing and plotting cluster mosaic ...")
    num_cluster = session_data[type_cluster].unique()
    num_cluster.sort()    
    # compute centroids in order to select pertinent sessions
    centroids = pd.DataFrame(columns=["cluster_id"] + features)
    centroids["cluster_id"] = num_cluster
    for dim in features:
        mean = []
        for cluster_id in num_cluster:
            mean.append(session_data[session_data[type_cluster]==cluster_id][dim].mean())
        centroids[dim] = mean
    # select sessions representative of each cluster
    start_time = timelib.time()
    selected_sessions = {}
    centroids["sum"] = centroids[features].sum(axis=1)
    session_data["dist"] = session_data[type_cluster].map(pd.Series(data=centroids["sum"], index=centroids.cluster_id.values))
    session_data["dist"] = session_data[features].sum(axis=1) - session_data["dist"]
    session_data["dist"] = np.sqrt((session_data["dist"] * session_data["dist"]))
    N_max_sessions=5 # Sessions to plot per cluster        
    for cluster_id in num_cluster:
        selected_sessions[cluster_id] = list(session_data[session_data[type_cluster]==cluster_id].sort_values(["dist"]).session_id.values)[:N_max_sessions]
        cluster_sessions = session_data[session_data[type_cluster] == cluster_id].session_id.unique()
        cluster_weblog = weblog[weblog.session_id.isin(cluster_sessions)]
        
        # Retrieving data for the N sessions sample
        session_data_df = pd.DataFrame(columns=['id','start','end','timespan','span_sec'])
        sessions=selected_sessions[cluster_id]
        session_data_df['id']=sessions # The number of the sessions to plot for this cluster
        session_start=cluster_weblog[[weblog_columns_dict['timestamp_column'],'session_id']].groupby('session_id').min()
        session_end=cluster_weblog[[weblog_columns_dict['timestamp_column'],'session_id']].groupby('session_id').max()
        session_data_df['start']=session_data_df.id.map(pd.Series(data=session_start\
                       [weblog_columns_dict['timestamp_column']].values,index=session_start.index))
        session_data_df['end']=session_data_df.id.map(pd.Series(data=session_end\
                       [weblog_columns_dict['timestamp_column']].values,index=session_end.index))
        session_data_df['timespan']=session_data_df.apply(lambda row: pd.Timedelta(pd.Timestamp(row.end)-pd.Timestamp(row.start)) , axis=1)
        session_data_df['span_sec']=session_data_df.timespan.apply(lambda x: x.seconds)
    # Computing the timeframe
        max_time=session_data[session_data.session_id.isin(sessions)].timespan.max()#span[cluster_id]
        padding_seconds=np.ceil(max_time/9.0)
        time_window_seconds=max_time+padding_seconds+1
        seconds = np.ceil(max_time/60/5)*5*60
        # Filling matrix
        width = int(0.015*max_time)
        image=np.zeros((len(sessions),int(time_window_seconds),4))
        session_counter=0
        for session in sessions:
            session_draw_bis(session, cluster_weblog,weblog_columns_dict)
            # selecting requests for the session
            session_weblog=cluster_weblog[cluster_weblog.session_id==session].sort_values(by='timestamp')
            session_weblog['relative_seconds']=0
            session_start=pd.Timestamp(session_weblog.timestamp.min())#pd.Timestamp(session_data[session_data.id==session].start.iloc[0])
            session_weblog['relative_seconds']=session_weblog['timestamp'].apply(lambda x: (pd.Timestamp(x)-session_start).seconds )
            for r in range(0,session_weblog.shape[0]):
                if r==session_weblog.shape[0]-1:
                    # if it is the last (or only request) we fill with blank pixels
                    image[session_counter,session_weblog.iloc[r].relative_seconds:,:]=np.zeros((int(time_window_seconds)-session_weblog.iloc[r].relative_seconds,4))
                else:
                    # color patch
                    pix_start=session_weblog.iloc[r].relative_seconds
                    pix_end=session_weblog.iloc[r+1].relative_seconds
                    paint_color=np.array([100,100,100,1])
                    paint_color_patch=np.reshape(np.tile(paint_color,pix_end-pix_start),newshape=(pix_end-pix_start,4))
                    image[session_counter,pix_start:pix_end,:]=paint_color_patch
                    # black patch
                    pix_start=session_weblog.iloc[r].relative_seconds
                    pix_end=pix_start+width
                    paint_color=np.array([0,0,0,1])
                    paint_black_patch=np.reshape(np.tile(paint_color,pix_end-pix_start),newshape=(pix_end-pix_start,4))
                    image[session_counter,pix_start:pix_end,:]=paint_black_patch
            session_counter+=1 
        grid = plt.GridSpec(10000, 12000, wspace=0.4, hspace=0.3)
        plt.subplot(grid[:, :9999])
        # Plotting the matrix
        plt.imshow((image*255).astype(np.uint8))
        plt.gcf().set_size_inches([ 4, 4])
        plt.gca().axis('auto')
        plt.xlabel('Minutes',fontsize=14)
        plt.ylabel('')
        #sessions_per_cluster=session_data[session_data[type_cluster]==cluster_id].shape[0]
        percent_sessions_per_cluster=100.0*session_data[session_data[type_cluster]==cluster_id].shape[0]/session_data.shape[0]
        plt.title("Cluster %s (%.1f%%)"%(str(cluster_id),percent_sessions_per_cluster),fontsize=14)
        plt.grid(alpha=0.0)
        plt.tick_params(axis="both", which="major", labelsize=6)
        # Lines and axes
        ax = plt.gca();
        #   Major ticks
        minutes = [int(n * round(seconds/60/5)) for n in range(0, 6)]
        seconds = list(map(lambda x: int(x*60), minutes))
        ax.set_xticks(seconds)
        ax.set_xticklabels(minutes,fontsize=14)
        ax.set_yticks(np.arange(0, len(sessions), 1))
        ax.set_yticklabels(['' for n in sessions])
        #   Minor ticks
        ax.set_yticks(np.arange(-.5, len(sessions), 1), minor=True);
        # Gridlines based on minor ticks
        ax.grid(which='minor', color='w', linestyle='-', linewidth=2)
        # Saving and closing
        plt.subplot(grid[:1999, 10000:11999])
        plt.axis('off')
        img = mpimg.imread("../graph_dump/_session"+str(sessions[0])+".png")
        plt.imshow(img)
        plt.subplot(grid[2000:3999, 10000:11999])
        plt.axis('off')
        img = mpimg.imread("../graph_dump/_session"+str(sessions[1])+".png")
        plt.imshow(img)
        plt.subplot(grid[4000:5999, 10000:11999])
        plt.axis('off')
        img = mpimg.imread("../graph_dump/_session"+str(sessions[2])+".png")
        plt.imshow(img)
        plt.subplot(grid[6000:7999, 10000:11999])
        plt.axis('off')
        img = mpimg.imread("../graph_dump/_session"+str(sessions[3])+".png")
        plt.imshow(img)
        plt.subplot(grid[8000:9999, 10000:11999])
        plt.axis('off')
        img = mpimg.imread("../graph_dump/_session"+str(sessions[4])+".png")
        plt.imshow(img)
        if filename is not None:    
            plt.savefig('../Figures/%s_%s.pdf'%(filename,str(cluster_id)), format='pdf')
        plt.show()
        plt.clf()
        plt.close()
            
    if verbose == True:
        print("     Cluster mosaic computed and plotted in %.1f seconds."%(timelib.time() - start_time))
    return;