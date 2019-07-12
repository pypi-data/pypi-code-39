import pandas as pd
import matplotlib.pyplot as plt

def plot_pages(weblog,days,hour_start,hour_end,filename=None):
    """
    Calculate and plot the number of requests each day at defined hour (entries) in function of 25 most popular pages
    """
    df = pd.DataFrame()
    for day in days:
        start='2019-6-%s %s:00:00'%(str(day),str(hour_start))
        end='2019-6-%s %s:59:59'%(str(day),str(hour_end))
        weblog_tmp = weblog[weblog.timestamp>start]
        weblog_tmp = weblog_tmp[weblog_tmp.timestamp<end]
        df['June_%s'%day]= (weblog_tmp.requested_pageID.value_counts()[:25].reset_index(drop=True))/weblog_tmp.shape[0]
    
    plt.figure()
    df.plot()
    plt.xlabel('25 most popular pages')
    plt.ylabel('Number of requests / Number of requests tot.')
    plt.title('June_%s__%s: %s:00:00-%s:59:59'%(str(min(days)),str(max(days)),str(hour_start),str(hour_end)))
    if filename is not None:
        plt.savefig('/home/alexandre/Documents/Melty/Experience/Pages_%s__%s/%s.pdf'%(str(min(days)),str(max(days)),filename))
    plt.show()
    return;
        
    
    
