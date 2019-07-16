import pandas as pd
import numpy as np
import tqdm
import time as timelib
import matplotlib.pyplot as plt

# local modules

from . import function



def temporal_analysis(weblog, session_data, analysis_column, temporal_analysis_weblog_start, temporal_analysis_weblog_end,\
                      group_names, weblog_column_dict,micd = False, verbose = False):
    """
    Calculate temporal (each hour) number of requests, entropy consummed,
    entropy offered and Mean Individual Consummed Diversity along the groups
    specified in "group_names"
    """
    if verbose== True:
        start_time_tot = timelib.time()
        print("\n   * Computing temporal analysis ...")
    temporal_analysis_weblog_start = pd.Timestamp(temporal_analysis_weblog_start)
    temporal_analysis_weblog_end = pd.Timestamp(temporal_analysis_weblog_end)
    t_weblog=weblog[weblog[weblog_column_dict['timestamp_column']]<temporal_analysis_weblog_end]
    t_weblog=t_weblog[t_weblog[weblog_column_dict['timestamp_column']]>temporal_analysis_weblog_start]
    start_day=pd.Timestamp(t_weblog[weblog_column_dict['timestamp_column']].min()).day
    end_day=pd.Timestamp(t_weblog[weblog_column_dict['timestamp_column']].max()).day
    if start_day > end_day:
        t_days = list(range(start_day,int(temporal_analysis_weblog_start.days_in_month)+1)) + list(range(1,end_day+1))
    else :
        t_days = list(range(int(start_day),int(end_day)+1))
    t_hours=list(range(0,24))
    t_activity_columns = ['t_activity_'+group_name for group_name in group_names]
    t_consumed_diversity_columns = ['t_consumed_diversity_'+group_name for group_name in group_names]
    t_offered_diversity_columns = ['t_offered_diversity_'+group_name for group_name in group_names]    
    if micd: t_mean_ind_cons_div_columns = ['t_mean_ind_cons_div_'+group_name for group_name in group_names]
    if micd: column_names = ['start_time','end_time','t_activity_total','t_consumed_diversity_total','t_offered_diversity_total','t_mean_ind_cons_div_total']\
                    +t_activity_columns+t_consumed_diversity_columns + t_offered_diversity_columns + t_mean_ind_cons_div_columns
    else: column_names = ['start_time','end_time','t_activity_total','t_consumed_diversity_total','t_offered_diversity_total']\
                    +t_activity_columns+t_consumed_diversity_columns + t_offered_diversity_columns 
    timeseries_data=pd.DataFrame(columns=column_names)
    for columns in timeseries_data:
        timeseries_data[columns] = np.zeros(len(t_days)*len(t_hours))

    counter=0
    year = temporal_analysis_weblog_start.year
    month = temporal_analysis_weblog_start.month
    yesterday = temporal_analysis_weblog_start.day
    for day in tqdm.tqdm(t_days):
        if day < yesterday: month += 1
        if month > 12:
            month = 1
            year += 1
        for hour in t_hours:
            start_time=pd.Timestamp('%d-%d-%d %s:00:00'%(year,month,day,function.zf(hour)))
            end_time=pd.Timestamp('%d-%d-%d %s:59:59'%(year,month,day,function.zf(hour)))
            timeseries_data['start_time'][counter] = start_time
            timeseries_data['end_time'][counter] = end_time
            hour_weblog=t_weblog[t_weblog[weblog_column_dict['timestamp_column']].apply(lambda x: pd.Timestamp(x))>start_time]
            hour_weblog=hour_weblog[hour_weblog[weblog_column_dict['timestamp_column']].apply(lambda x: pd.Timestamp(x))<end_time]
            hour_session = session_data[session_data.session_id.isin(hour_weblog.session_id.unique())]
            # Total
            timeseries_data['t_activity_total'][counter]=hour_weblog.shape[0]
            if hour_weblog.shape[0]>0:
                pa_consumed,aux=function.proportional_abundance(hour_weblog,analysis_column)
                pa_offered,aux=function.proportional_abundance(hour_weblog.drop_duplicates\
                                                               (subset=weblog_column_dict['requested_page_column']),analysis_column)
                timeseries_data['t_consumed_diversity_total'][counter]=function.ShannonEntropy(pa_consumed)
                timeseries_data['t_offered_diversity_total'][counter]=function.ShannonEntropy(pa_offered)
                if micd: timeseries_data['t_mean_ind_cons_div_total'][counter]=hour_session.topic_entropy.mean()
            # Groups 
            for group_name in group_names:
                list_sessions = session_data[session_data[group_name]].session_id.values
                weblog_tmp = hour_weblog[hour_weblog.session_id.isin(list_sessions)]
                session_tmp = hour_session[hour_session.session_id.isin(list_sessions)]
                timeseries_data['t_activity_'+group_name][counter] = weblog_tmp.shape[0]
                if weblog_tmp.shape[0]>0:
                    pa_consumed, aux = function.proportional_abundance(weblog_tmp,analysis_column)
                    pa_offered,aux=function.proportional_abundance(weblog_tmp.drop_duplicates\
                                                                   (subset=weblog_column_dict['requested_page_column']),analysis_column)
                    timeseries_data['t_consumed_diversity_'+group_name][counter] = function.ShannonEntropy(pa_consumed)
                    timeseries_data['t_offered_diversity_'+group_name][counter]=function.ShannonEntropy(pa_offered)
                    if micd: timeseries_data['t_mean_ind_cons_div_'+group_name][counter]=session_tmp.topic_entropy.mean()
            # Aux
            counter+=1
        del hour_weblog
        yesterday = day 
        
    if verbose == True:
        print("     Temporal analysis computed in %.1f seconds."%(timelib.time() - start_time_tot))
    return timeseries_data;


def temporal_analysis_article(weblog, temporal_analysis_weblog_start, temporal_analysis_weblog_end, weblog_column_dict,verbose = False):
    """
    Calculate temporal (each 6 hours) number of requests article -> article and 
    number of requests article -> article that have changed topic
    """
    if verbose== True:
        start_time_tot = timelib.time()
        print("\n   * Computing temporal analysis on number of article ...")
    temporal_analysis_weblog_start = pd.Timestamp(temporal_analysis_weblog_start)
    temporal_analysis_weblog_end = pd.Timestamp(temporal_analysis_weblog_end)
    t_weblog=weblog[weblog[weblog_column_dict['timestamp_column']]<temporal_analysis_weblog_end]
    t_weblog=t_weblog[t_weblog[weblog_column_dict['timestamp_column']]>temporal_analysis_weblog_start]
    start_day=pd.Timestamp(t_weblog[weblog_column_dict['timestamp_column']].min()).day
    end_day=pd.Timestamp(t_weblog[weblog_column_dict['timestamp_column']].max()).day
    if start_day > end_day:
        t_days = list(range(start_day,int(temporal_analysis_weblog_start.days_in_month)+1)) + list(range(1,end_day+1))
    else :
        t_days = list(range(int(start_day),int(end_day)+1))
    t_hours=list(range(0,24))

    column_names = ['start_time','end_time','t_activity_article','t_activity_article_change_topic']
    timeseries_data=pd.DataFrame(columns=column_names)
    for columns in timeseries_data:
        timeseries_data[columns] = np.zeros(len(t_days)*len(t_hours))

    counter=0
    year = temporal_analysis_weblog_start.year
    month = temporal_analysis_weblog_start.month
    yesterday = temporal_analysis_weblog_start.day
    for day in tqdm.tqdm(t_days):
        if day < yesterday: month += 1
        if month > 12:
            month = 1
            year += 1
        hour = 0
        for i in range(4):
            start_time=pd.Timestamp('%d-%d-%d %s:00:00'%(year,month,day,function.zf(hour)))
            end_time=pd.Timestamp('%d-%d-%d %s:59:59'%(year,month,day,str(int(function.zf(hour))+5)))
            timeseries_data['start_time'][counter:counter+6] = start_time
            timeseries_data['end_time'][counter:counter+6] = end_time
            hour_weblog=t_weblog[t_weblog[weblog_column_dict['timestamp_column']].apply(lambda x: pd.Timestamp(x))>start_time]
            hour_weblog=hour_weblog[hour_weblog[weblog_column_dict['timestamp_column']].apply(lambda x: pd.Timestamp(x))<end_time]
            
            hour_weblog=hour_weblog[(hour_weblog.requested_category == 'article') &  (hour_weblog.referrer_category == 'article')]
            
            # number of requests article article per hour
            timeseries_data['t_activity_article'][counter:counter+6]=hour_weblog.shape[0]
            
            hour_weblog=hour_weblog[hour_weblog.requested_topic != hour_weblog.referrer_topic]

            #number of requests article article that have changed topic
            timeseries_data['t_activity_article_change_topic'][counter:counter+6] = hour_weblog.shape[0]
            # Aux
            counter+=6
            hour+=6
        del hour_weblog
        yesterday = day 
        
    if verbose == True:
        print("     Temporal analysis on number of article computed in %.1f seconds."%(timelib.time() - start_time_tot))
    return timeseries_data;

def temporal_analysis_article_day(weblog, temporal_analysis_weblog_start, temporal_analysis_weblog_end, weblog_column_dict,verbose = False):
    """
    Calculate temporal (each day) number of requests article -> article and 
    number of requests article -> article that have changed topic
    """
    if verbose== True:
        start_time_tot = timelib.time()
        print("\n   * Computing temporal analysis on number of article ...")
    temporal_analysis_weblog_start = pd.Timestamp(temporal_analysis_weblog_start)
    temporal_analysis_weblog_end = pd.Timestamp(temporal_analysis_weblog_end)
    t_weblog=weblog[weblog[weblog_column_dict['timestamp_column']]<temporal_analysis_weblog_end]
    t_weblog=t_weblog[t_weblog[weblog_column_dict['timestamp_column']]>temporal_analysis_weblog_start]
    start_day=pd.Timestamp(t_weblog[weblog_column_dict['timestamp_column']].min()).day
    end_day=pd.Timestamp(t_weblog[weblog_column_dict['timestamp_column']].max()).day
    if start_day > end_day:
        t_days = list(range(start_day,int(temporal_analysis_weblog_start.days_in_month)+1)) + list(range(1,end_day+1))
    else :
        t_days = list(range(int(start_day),int(end_day)+1))
    t_hours=list(range(0,24))
    column_names = ['start_time','end_time','t_activity_article','t_activity_article_change_topic']
    timeseries_data=pd.DataFrame(columns=column_names)
    for columns in timeseries_data:
        timeseries_data[columns] = np.zeros(len(t_days)*len(t_hours))

    counter=0
    year = temporal_analysis_weblog_start.year
    month = temporal_analysis_weblog_start.month
    yesterday = temporal_analysis_weblog_start.day
    for day in tqdm.tqdm(t_days):
        if day < yesterday: month += 1
        if month > 12:
            month = 1
            year += 1
        
        start_time=pd.Timestamp('%d-%d-%d 00:00:00'%(year,month,day))
        end_time=pd.Timestamp('%d-%d-%d 23:59:59'%(year,month,day))
        timeseries_data['start_time'][counter:counter+24] = start_time
        timeseries_data['end_time'][counter:counter+24] = end_time
        day_weblog=t_weblog[t_weblog[weblog_column_dict['timestamp_column']].apply(lambda x: pd.Timestamp(x))>start_time]
        day_weblog=day_weblog[day_weblog[weblog_column_dict['timestamp_column']].apply(lambda x: pd.Timestamp(x))<end_time]
        
        day_weblog=day_weblog[(day_weblog.requested_category == 'article') &  (day_weblog.referrer_category == 'article')]
        
        # number of requests article article per hour
        timeseries_data['t_activity_article'][counter:counter+24]=day_weblog.shape[0]
        
        day_weblog=day_weblog[day_weblog.requested_topic != day_weblog.referrer_topic]

        #number of requests article article that have changed topic
        timeseries_data['t_activity_article_change_topic'][counter:counter+24] = day_weblog.shape[0]
        # Aux
        counter+=24
        del day_weblog
        yesterday = day 
        
    if verbose == True:
        print("     Temporal analysis on number of article computed in %.1f seconds."%(timelib.time() - start_time_tot))
    return timeseries_data;

def plot_temporal_avant(timeseries_data,verbose=True):
    """
    Same as plot_temporal but old version
    """
    if verbose== True:
        start_time = timelib.time()
        print("\n   * Plotting temporal analysis ...")
        
    filter_size=1
    filter_array=(1/filter_size)*np.ones(filter_size)
    first_day=18
    last_day=24    
    number_of_days=int(last_day-first_day+1)
    we_days=[9,10,16,17,23,24]
    # Figure setting
    fig,(ax1,ax2)=plt.subplots(2,1,figsize=(15,5))
    # Activity
    ax1.plot(range(len(timeseries_data['t_activity_total'])),np.convolve(timeseries_data['t_activity_total'],filter_array,mode='same'))
    ax1.plot(range(len(timeseries_data['t_activity_F'])),np.convolve(timeseries_data['t_activity_F'],filter_array,mode='same'))
    ax1.plot(range(len(timeseries_data['t_activity_search'])),np.convolve(timeseries_data['t_activity_search'],filter_array,mode='same'))
    ax1.plot(range(len(timeseries_data['t_activity_social'])),np.convolve(timeseries_data['t_activity_social'],filter_array,mode='same'))
    ax1.set_xticks([12+n*24 for n in range(0,number_of_days)])
    ax1.set_xticklabels(['9/%d/2017 '%(n) for n in range(first_day,first_day+number_of_days+1)],fontsize=11)
    ax1.grid(False)
    ax1.set_xlim((0,len(timeseries_data['t_activity_social'])*1.25))
    for n in range(0,number_of_days+1):#painting the lines dividing the days
        ax1.axvline(x=n*24,color='k',linestyle=':')
    for we_day in we_days: # painting the weekend days
        ax1.axvspan(24*(we_day-first_day), 24*(we_day-first_day+1), facecolor='green', edgecolor='none', alpha=.2)
    ax1.set_title('Hourly Activity',fontsize=14)
#    ax1.set_xlabel('Time')
    ax1.set_ylabel('Requests',fontsize=14)
    ax1.set_yscale('log')
#    ax1.legend(['Total','Sessions w. 1 Req.','Sessions w. 2 Req.','Sessions w. 3 Req.','Sessions w. 4 Req.','Sessions wmt 4 req.','Sessions w. Search Or.','Sessions w. Social Or.'])
    ax1.legend(['Total','Sessions \nwith more than \n4 requests','Sessions\noriginated\nin search\npages','Sessions\noriginated\nin social\nplatforms'])
   
    # Diversity
    ax2.plot(range(len(timeseries_data['t_diversity_total'])),np.convolve(np.power(2,timeseries_data['t_diversity_total']),filter_array,mode='same'))
#    ax2.plot(range(len(t_diversity_B)),np.convolve(np.power(t_diversity_B,2.0),filter_array,mode='same'))
#    ax2.plot(range(len(t_diversity_C)),np.convolve(np.power(t_diversity_C,2.0),filter_array,mode='same'))
#    ax2.plot(range(len(t_diversity_D)),np.convolve(np.power(t_diversity_D,2.0),filter_array,mode='same'))
#    ax2.plot(range(len(t_diversity_E)),np.convolve(np.power(t_diversity_E,2.0),filter_array,mode='same'))
    ax2.plot(range(len(timeseries_data['t_diversity_F'])),np.convolve(np.power(2,timeseries_data['t_diversity_F']),filter_array,mode='same'))
    ax2.plot(range(len(timeseries_data['t_diversity_search'])),np.convolve(np.power(2,timeseries_data['t_diversity_search']),filter_array,mode='same'))
    ax2.plot(range(len(timeseries_data['t_diversity_social'])),np.convolve(np.power(2,timeseries_data['t_diversity_social']),filter_array,mode='same'))
    ax2.set_xticks([12+n*24 for n in range(0,number_of_days)])
    ax2.set_xticklabels(['9/%d/2017 '%(n) for n in range(first_day,first_day+number_of_days+1)],fontsize=11)
    ax2.grid(False)
    ax2.set_xlim((0,len(timeseries_data['t_activity_social'])*1.25))
    for n in range(0,number_of_days+1):#painting the lines dividing the days
        ax2.axvline(x=n*24,color='k',linestyle=':')
    for we_day in we_days: # painting the weekend days
        ax2.axvspan(24*(we_day-first_day), 24*(we_day-first_day+1), facecolor='green', edgecolor='none', alpha=.2)
#    ax2.set_title('Diversity')
    ax2.set_xlabel('Time',fontsize=14)
    ax2.set_ylabel('IEUC',fontsize=14)
    # Saving
    week_graph_length=10
    weeks_in_graph=number_of_days/7
    fig.set_size_inches(week_graph_length*weeks_in_graph, 5)
    plt.tight_layout()
    plt.savefig('../Figures/temporal_apres.pdf', format='pdf')
    plt.show()
    plt.clf()
    plt.close()
    
    if verbose == True:
        print("     Temporal analysis plotted in %.1f seconds."%(timelib.time() - start_time))
    return;

def plot_temporal(timeseries_data, group_names, micd = False, filename = None, verbose = False):
    """
    Plot temporal analysis with timeseries_data calculated with "temporal_analysis"
    """
    if verbose== True:
        start_time = timelib.time()
        print("\n   * Plotting temporal analysis ...")
        
    filter_size=1
    filter_array=(1/filter_size)*np.ones(filter_size)
    first_date=pd.Timestamp(timeseries_data['start_time'].min())
    last_date=pd.Timestamp(timeseries_data['end_time'].max())
    if first_date.day > last_date.day:
        list_date = ['%d/%d/%d'%(first_date.year,first_date.month,n) for n in range(first_date.day,first_date.days_in_month+1)]+\
                    ['%d/%d/%d'%(last_date.year,last_date.month,n) for n in range(1,last_date.day+1)]
        number_of_days=len(list_date)
    else :
        list_date = ['%d/%d/%d'%(first_date.year,first_date.month,n) for n in range(first_date.day,last_date.day+1)]
        number_of_days=len(list_date)
    
    we_days = [pd.Timestamp(n).day for n in timeseries_data['start_time'] if (pd.Timestamp(n).dayofweek == 5 or \
                                                                              pd.Timestamp(n).dayofweek == 6)]
    we_days = list(set(we_days))
    # Figure setting
    if micd: fig,(ax1,ax2,ax3,ax4)=plt.subplots(4,1,figsize=(20,15))
    else: fig,(ax1,ax2,ax3)=plt.subplots(3,1,figsize=(20,15))
    # Activity
    ax1.plot(range(len(timeseries_data['t_activity_total'])),np.convolve(timeseries_data['t_activity_total'],filter_array,mode='same'))
    for group_name in group_names:
        ax1.plot(range(len(timeseries_data['t_activity_'+group_name])),np.convolve(timeseries_data['t_activity_'+group_name],filter_array,mode='same'))
    ax1.set_xticks([12+n*24 for n in range(0,number_of_days)])
    #ax1.set_xticklabels(list_date,fontsize=11)
    ax1.set_xticklabels(['','',''],fontsize=11)
    ax1.grid(False)
    ax1.set_yscale('log')
    ax1.set_xlim((0,len(timeseries_data['t_activity_total'])))
    for n in range(0,number_of_days+1):#painting the lines dividing the days
        ax1.axvline(x=n*24,color='k',linestyle=':')
    for we_day in we_days: # painting the weekend days
        ax1.axvspan(24*(we_day-first_date.day), 24*(we_day-first_date.day+1), facecolor='green', edgecolor='none', alpha=.2)
    ax1.set_title('Hourly Activity',fontsize=14)
    ax1.set_ylabel('Requests',fontsize=14)
    #ax_names= ['Total','Sessions \nwith more than \n4 requests','Sessions\noriginated\nin search\npages','Sessions\noriginated\nin social\nplatforms']
    ax_names = ['Total'] + group_names 
    ax1.legend(ax_names,loc=4,bbox_to_anchor=(1.53,-2.5)) # option to deplace the legend
    # Consumed diversity
    #ax2.plot(range(len(timeseries_data['t_consumed_diversity_total'])),\
     #        np.convolve(np.power(2,timeseries_data['t_consumed_diversity_total']),filter_array,mode='same'))
    ax2.plot(range(len(timeseries_data['t_consumed_diversity_total'])),\
             np.convolve(timeseries_data['t_consumed_diversity_total'],filter_array,mode='same'))
    for group_name in group_names:
        #ax2.plot(range(len(timeseries_data['t_consumed_diversity_'+group_name])),\
         #        np.convolve(np.power(2,timeseries_data['t_consumed_diversity_'+group_name]),filter_array,mode='same'))
        ax2.plot(range(len(timeseries_data['t_consumed_diversity_'+group_name])),\
                 np.convolve(timeseries_data['t_consumed_diversity_'+group_name],filter_array,mode='same'))
    ax2.set_xticks([12+n*24 for n in range(0,number_of_days)])
    #ax2.set_xticklabels(list_date,fontsize=11)
    ax2.set_xticklabels(['','',''],fontsize=11)
    ax2.grid(False)
    ax2.set_xlim((0,len(timeseries_data['t_activity_total'])))
    for n in range(0,number_of_days+1):#painting the lines dividing the days
        ax2.axvline(x=n*24,color='k',linestyle=':')
    for we_day in we_days: # painting the weekend days
            ax2.axvspan(24*(we_day-first_date.day), 24*(we_day-first_date.day+1), facecolor='green', edgecolor='none', alpha=.2)
    ax2.set_ylabel('Cons. IEUC',fontsize=14)
    # Offered diversity
    ax3.plot(range(len(timeseries_data['t_offered_diversity_total'])),\
             np.convolve(np.power(2,timeseries_data['t_offered_diversity_total']),filter_array,mode='same'))
    for group_name in group_names:
        ax3.plot(range(len(timeseries_data['t_offered_diversity_'+group_name])),\
                 np.convolve(np.power(2,timeseries_data['t_offered_diversity_'+group_name]),filter_array,mode='same'))
    ax3.set_xticks([12+n*24 for n in range(0,number_of_days)])
    ax3.set_xticklabels(['','',''],fontsize=11)
    #ax3.set_xticklabels(list_date,fontsize=11)
    ax3.grid(False)
    ax3.set_xlim((0,len(timeseries_data['t_activity_total'])))
    for n in range(0,number_of_days+1):#painting the lines dividing the days
        ax3.axvline(x=n*24,color='k',linestyle=':')
    for we_day in we_days: # painting the weekend days
            ax3.axvspan(24*(we_day-first_date.day), 24*(we_day-first_date.day+1), facecolor='green', edgecolor='none', alpha=.2)
    ax3.set_ylabel('Off. IEUC',fontsize=14)
    # Mean Ind. Cons. Diversity
    if micd:
        ax4.plot(range(len(timeseries_data['t_mean_ind_cons_div_total'])),\
                 np.convolve(np.power(2,timeseries_data['t_mean_ind_cons_div_total']),filter_array,mode='same'))
        for group_name in group_names:
            ax4.plot(range(len(timeseries_data['t_mean_ind_cons_div_'+group_name])),\
                     np.convolve(np.power(2,timeseries_data['t_mean_ind_cons_div_'+group_name]),filter_array,mode='same'))
        ax4.set_xticks([12+n*24 for n in range(0,number_of_days)])
        ax4.set_xticklabels(list_date,fontsize=11)
        ax4.grid(False)
        ax4.set_xlim((0,len(timeseries_data['t_activity_total'])))
        for n in range(0,number_of_days+1):#painting the lines dividing the days
            ax4.axvline(x=n*24,color='k',linestyle=':')
        for we_day in we_days: # painting the weekend days
                ax4.axvspan(24*(we_day-first_date.day), 24*(we_day-first_date.day+1), facecolor='green', edgecolor='none', alpha=.2)
        ax4.set_xlabel('Time',fontsize=14)
        ax4.set_ylabel('M.I.C.IEUC',fontsize=14)
    # Saving
    week_graph_length=10
    weeks_in_graph=number_of_days/7
    fig.set_size_inches(week_graph_length*weeks_in_graph, 5)
    if filename is not None:
        plt.savefig('../Figures/%s.pdf'%filename, bbox_inches = 'tight') # bbox in order to save the legend
    plt.show()
    if verbose == True:
        print("     Temporal analysis plotted in %.1f seconds."%(timelib.time() - start_time))
    plt.clf()
    plt.close()
    return;
    
def plot_temporal_article(timeseries_data, filename = None, verbose = False):
    if verbose== True:
        start_time = timelib.time()
        print("\n   * Plotting temporal analysis on number of article ...")
        
    filter_size=1
    filter_array=(1/filter_size)*np.ones(filter_size)
    first_date=pd.Timestamp(timeseries_data['start_time'].min())
    last_date=pd.Timestamp(timeseries_data['end_time'].max())
    if first_date.day > last_date.day:
        list_date = ['%d/%d/%d'%(first_date.year,first_date.month,n) for n in range(first_date.day,first_date.days_in_month+1)]+\
                    ['%d/%d/%d'%(last_date.year,last_date.month,n) for n in range(1,last_date.day+1)]
        number_of_days=len(list_date)
    else :
        list_date = ['%d/%d/%d'%(first_date.year,first_date.month,n) for n in range(first_date.day,last_date.day+1)]
        number_of_days=len(list_date)
    
    we_days = [pd.Timestamp(n).day for n in timeseries_data['start_time'] if (pd.Timestamp(n).dayofweek == 5 or \
                                                                              pd.Timestamp(n).dayofweek == 6)]
    we_days = list(set(we_days))
    # Figure setting
    fig,ax1=plt.subplots(1,1)
    # Activity
    ax1.plot(range(len(timeseries_data['t_activity_article'])),np.convolve(timeseries_data['t_activity_article'],filter_array,mode='same'))
    ax1.plot(range(len(timeseries_data['t_activity_article_change_topic'])),\
             np.convolve(timeseries_data['t_activity_article_change_topic'],filter_array,mode='same'))

    ax1.set_xticks([12+n*24 for n in range(0,number_of_days)])
    ax1.set_xticklabels(list_date,fontsize=11)
    ax1.grid(False)
    ax1.set_yscale('log')
    ax1.set_xlim((0,len(timeseries_data['t_activity_article'])))
    for n in range(0,number_of_days+1):#painting the lines dividing the days
        ax1.axvline(x=n*24,color='k',linestyle=':')
    for we_day in we_days: # painting the weekend days
        ax1.axvspan(24*(we_day-first_date.day), 24*(we_day-first_date.day+1), facecolor='green', edgecolor='none', alpha=.2)
    ax1.set_title('Hourly Activity',fontsize=14)
    ax1.set_ylabel('Requests',fontsize=14)
    ax_names = ['Requests article -> article', 'Requests article -> article \n that have changed topic'] 
    #ax_names= ['Total','Sessions \nwith more than \n4 requests','Sessions\noriginated\nin search\npages','Sessions\noriginated\nin social\nplatforms']
    ax1.legend(ax_names,loc=4,bbox_to_anchor=(1.8,0.5)) # option to deplace the legend

    # Saving
    week_graph_length=10
    weeks_in_graph=number_of_days/7
    fig.set_size_inches(week_graph_length*weeks_in_graph, 5)
    if filename is not None:
        plt.savefig('/home/alexandre/Documents/Melty/Experience/%s.pdf'%filename, bbox_inches = 'tight') # bbox in order to save the legend
    plt.show()
    if verbose == True:
        print("     Temporal analysis plotted in %.1f seconds."%(timelib.time() - start_time))
    plt.clf()
    plt.close()
    return;
    
def plot_temporal_article_2(timeseries_data, filename = None, verbose = False):
    """
    Plot temporal analysis with timeseries_data calculated temporal_analysis_article, 
    plot #(requests art-art that have changed topic)/#(requests art-art) 
    """
    if verbose== True:
        start_time = timelib.time()
        print("\n   * Plotting temporal analysis on number of article ...")
        
    filter_size=1
    filter_array=(1/filter_size)*np.ones(filter_size)
    first_date=pd.Timestamp(timeseries_data['start_time'].min())
    last_date=pd.Timestamp(timeseries_data['end_time'].max())
    if first_date.day > last_date.day:
        list_date = ['%d/%d/%d'%(first_date.year,first_date.month,n) for n in range(first_date.day,first_date.days_in_month+1)]+\
                    ['%d/%d/%d'%(last_date.year,last_date.month,n) for n in range(1,last_date.day+1)]
        number_of_days=len(list_date)
    else :
        list_date = ['%d/%d/%d'%(first_date.year,first_date.month,n) for n in range(first_date.day,last_date.day+1)]
        number_of_days=len(list_date)
    
    we_days = [pd.Timestamp(n).day for n in timeseries_data['start_time'] if (pd.Timestamp(n).dayofweek == 5 or \
                                                                              pd.Timestamp(n).dayofweek == 6)]
    we_days = list(set(we_days))
    # Figure setting
    fig,ax1=plt.subplots(1,1)
    # Activity
    ax1.plot(range(len(timeseries_data['t_activity_article'])),np.convolve(timeseries_data['t_activity_article_change_topic']/timeseries_data['t_activity_article'],filter_array,mode='same'))

    ax1.set_xticks([12+n*24 for n in range(0,number_of_days)])
    ax1.set_xticklabels(list_date,fontsize=11)
    ax1.grid(False)
    ax1.set_yscale('log')
    ax1.set_xlim((0,len(timeseries_data['t_activity_article'])))
    for n in range(0,number_of_days+1):#painting the lines dividing the days
        ax1.axvline(x=n*24,color='k',linestyle=':')
    for we_day in we_days: # painting the weekend days
        ax1.axvspan(24*(we_day-first_date.day), 24*(we_day-first_date.day+1), facecolor='green', edgecolor='none', alpha=.2)
    ax1.set_title('#(requêtes art-art qui changent de topic)/#(requêtes art-art)',fontsize=14)
    ax1.set_ylabel('Requests',fontsize=14)
    #ax_names= ['Total','Sessions \nwith more than \n4 requests','Sessions\noriginated\nin search\npages','Sessions\noriginated\nin social\nplatforms']

    # Saving
    week_graph_length=10
    weeks_in_graph=number_of_days/7
    fig.set_size_inches(week_graph_length*weeks_in_graph, 5)
    if filename is not None:
        plt.savefig('/home/alexandre/Documents/alex/Figures/%s.pdf'%filename, bbox_inches = 'tight') # bbox in order to save the legend
    plt.show()
    if verbose == True:
        print("     Temporal analysis plotted in %.1f seconds."%(timelib.time() - start_time))
    plt.clf()
    plt.close()
    return;
