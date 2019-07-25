import pandas as pd
import numpy as np
import time as timelib
import matplotlib.pyplot as plt   

# local modules

from . import function



def temporal_analysis(weblog, session_data, classification_column, temporal_analysis_weblog_start, temporal_analysis_weblog_end,\
                      group_names, weblog_column_dict,micd = False, verbose = False):
    """
    Calculate temporal (each hour) number of requests, entropy consummed,
    entropy offered and Mean Individual Consummed Diversity along the groups
    specified in "group_names"
    
    Parameters
    ----------
        weblog: pandas dataframe of requests
         
        session_data: pandas dataframe of requests

        classification_column: pandas dataframe column wanted to be analysed
    
        temporal_analysis_weblog_start: start timestamp
   
        temporal_analysis_weblog_end: end timestamp

        group_names: list of string
    
        weblog_columns_dict: dict
       
    Returns
    -------
        Pandas dataframe
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
    try:    
        import tqdm
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
                    pa_consumed,aux=function.proportional_abundance(hour_weblog,'requested_'+classification_column)
                    pa_offered,aux=function.proportional_abundance(hour_weblog.drop_duplicates\
                                                                   (subset=weblog_column_dict['requested_page_column']),'requested_'+classification_column)
                    timeseries_data['t_consumed_diversity_total'][counter]=function.ShannonEntropy(pa_consumed)
                    timeseries_data['t_offered_diversity_total'][counter]=function.ShannonEntropy(pa_offered)
                    if micd: timeseries_data['t_mean_ind_cons_div_total'][counter]=hour_session[classification_column+'_entropy'].mean()
                # Groups 
                for group_name in group_names:
                    list_sessions = session_data[session_data[group_name]].session_id.values
                    weblog_tmp = hour_weblog[hour_weblog.session_id.isin(list_sessions)]
                    session_tmp = hour_session[hour_session.session_id.isin(list_sessions)]
                    timeseries_data['t_activity_'+group_name][counter] = weblog_tmp.shape[0]
                    if weblog_tmp.shape[0]>0:
                        pa_consumed, aux = function.proportional_abundance(weblog_tmp,'requested_'+classification_column)
                        pa_offered,aux=function.proportional_abundance(weblog_tmp.drop_duplicates\
                                                                       (subset=weblog_column_dict['requested_page_column']),'requested_'+classification_column)
                        timeseries_data['t_consumed_diversity_'+group_name][counter] = function.ShannonEntropy(pa_consumed)
                        timeseries_data['t_offered_diversity_'+group_name][counter]=function.ShannonEntropy(pa_offered)
                        if micd: timeseries_data['t_mean_ind_cons_div_'+group_name][counter]=session_tmp[classification_column+'_entropy'].mean()
                # Aux
                counter+=1
            del hour_weblog
            yesterday = day 
            
    except ImportError:
        for day in t_days:
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
                    pa_consumed,aux=function.proportional_abundance(hour_weblog,'requested_'+classification_column)
                    pa_offered,aux=function.proportional_abundance(hour_weblog.drop_duplicates\
                                                                   (subset=weblog_column_dict['requested_page_column']),'requested_'+classification_column)
                    timeseries_data['t_consumed_diversity_total'][counter]=function.ShannonEntropy(pa_consumed)
                    timeseries_data['t_offered_diversity_total'][counter]=function.ShannonEntropy(pa_offered)
                    if micd: timeseries_data['t_mean_ind_cons_div_total'][counter]=hour_session[classification_column+'_entropy'].mean()
                # Groups 
                for group_name in group_names:
                    list_sessions = session_data[session_data[group_name]].session_id.values
                    weblog_tmp = hour_weblog[hour_weblog.session_id.isin(list_sessions)]
                    session_tmp = hour_session[hour_session.session_id.isin(list_sessions)]
                    timeseries_data['t_activity_'+group_name][counter] = weblog_tmp.shape[0]
                    if weblog_tmp.shape[0]>0:
                        pa_consumed, aux = function.proportional_abundance(weblog_tmp,'requested_'+classification_column)
                        pa_offered,aux=function.proportional_abundance(weblog_tmp.drop_duplicates\
                                                                       (subset=weblog_column_dict['requested_page_column']),'requested_'+classification_column)
                        timeseries_data['t_consumed_diversity_'+group_name][counter] = function.ShannonEntropy(pa_consumed)
                        timeseries_data['t_offered_diversity_'+group_name][counter]=function.ShannonEntropy(pa_offered)
                        if micd: timeseries_data['t_mean_ind_cons_div_'+group_name][counter]=session_tmp[classification_column+'_entropy'].mean()
                # Aux
                counter+=1
            del hour_weblog
            yesterday = day 
    

        
    if verbose == True:
        print("     Temporal analysis computed in %.1f seconds."%(timelib.time() - start_time_tot))
    return timeseries_data;


def temporal_analysis_article(weblog, classification_column_diversity, classification_column_transaction, transaction,temporal_analysis_weblog_start, temporal_analysis_weblog_end, weblog_column_dict,verbose = False):
    """
    Calculate temporal (each 6 hours) number of requests article -> article and 
    number of requests article -> article that have changed classification
    
    Parameters
    ----------
    weblog: pandas dataframe of requests
    
    classification_column_diversity: pandas dataframe column wanted to be analysed
 
    classification_column_transaction: pandas dataframe column wanted to be selected for transaction
    
    transaction: string, belonging to the items of classification_column_transaction
            
    temporal_analysis_weblog_start: start timestamp
   
    temporal_analysis_weblog_end: end timestamp
    
    weblog_column_dict: dict
       
    Returns
    -------
        Pandas dataframe
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

    column_names = ['start_time','end_time','t_activity_article','t_activity_article_change_class']
    timeseries_data=pd.DataFrame(columns=column_names)
    for columns in timeseries_data:
        timeseries_data[columns] = np.zeros(len(t_days)*len(t_hours))

    counter=0
    year = temporal_analysis_weblog_start.year
    month = temporal_analysis_weblog_start.month
    yesterday = temporal_analysis_weblog_start.day
    for day in t_days:
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
            
            hour_weblog=hour_weblog[(hour_weblog['requested_'+classification_column_transaction] == transaction) &  (hour_weblog['referrer_'+classification_column_transaction] == transaction)]
            
            # number of requests article article per hour
            timeseries_data['t_activity_article'][counter:counter+6]=hour_weblog.shape[0]
            
            hour_weblog=hour_weblog[hour_weblog['requested_'+classification_column_diversity] != hour_weblog['referrer_'+classification_column_diversity]]

            #number of requests article article that have changed class
            timeseries_data['t_activity_article_change_class'][counter:counter+6] = hour_weblog.shape[0]
            # Aux
            counter+=6
            hour+=6
        del hour_weblog
        yesterday = day 
        
    if verbose == True:
        print("     Temporal analysis on number of article computed in %.1f seconds."%(timelib.time() - start_time_tot))
    return timeseries_data;

def temporal_analysis_article_day(weblog,classification_column_diversity, classification_column_transaction, transaction, temporal_analysis_weblog_start, temporal_analysis_weblog_end, weblog_column_dict,verbose = False):
    """
    Calculate temporal (each day) number of requests article -> article and 
    number of requests article -> article that have changed class
    
    Parameters
    ----------
    weblog: pandas dataframe of requests
    
    classification_column: pandas dataframe column wanted to be analysed
    
    classification_column_transaction: pandas dataframe column wanted to be selected for transaction
    
    transaction: string, belonging to the items of classification_column_transaction

    temporal_analysis_weblog_start: start timestamp
   
    temporal_analysis_weblog_end: end timestamp
    
    weblog_column_dict: dict
       
    Returns
    -------
        Pandas dataframe
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
    column_names = ['start_time','end_time','t_activity_article','t_activity_article_change_class']
    timeseries_data=pd.DataFrame(columns=column_names)
    for columns in timeseries_data:
        timeseries_data[columns] = np.zeros(len(t_days)*len(t_hours))

    counter=0
    year = temporal_analysis_weblog_start.year
    month = temporal_analysis_weblog_start.month
    yesterday = temporal_analysis_weblog_start.day
    for day in t_days:
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
        
        day_weblog=day_weblog[(day_weblog['requested_'+classification_column_diversity] == transaction) &  (day_weblog['referrer_'+classification_column_diversity] == transaction)]
        
        # number of requests article article per hour
        timeseries_data['t_activity_article'][counter:counter+24]=day_weblog.shape[0]
        
        day_weblog=day_weblog[day_weblog['requested_'+classification_column_diversity] != day_weblog['referrer_'+classification_column_diversity]]

        #number of requests article article that have changed class
        timeseries_data['t_activity_article_change_class'][counter:counter+24] = day_weblog.shape[0]
        # Aux
        counter+=24
        del day_weblog
        yesterday = day 
        
    if verbose == True:
        print("     Temporal analysis on number of article computed in %.1f seconds."%(timelib.time() - start_time_tot))
    return timeseries_data;

def plot_temporal(timeseries_data, group_names, micd = False, filename = None, verbose = False):
    """
    Plot temporal analysis with timeseries_data calculated with "temporal_analysis"
    
    Parameters
    ----------
        timeseries_data: pandas dataframe given by temporal functions

        group_names: list of string
        
        micd: bool, if Mean Individual Consummed Diversity is wanted
       
    Returns
    -------
        None
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
    ax1.legend(ax_names,bbox_to_anchor=(2.5,0)) # option to deplace the legend
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
    if not micd: ax3.set_xticklabels(list_date,fontsize=11)
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
    """
    Plot temporal analysis with timeseries_data calculated temporal_analysis_article, 
    plot #(requests art-art that have changed class)/#(requests art-art) 
    
    Parameters
    ----------
        timeseries_data: pandas dataframe given by temporal functions
       
    Returns
    -------
        None
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
    ax1.plot(range(len(timeseries_data['t_activity_article'])),np.convolve(timeseries_data['t_activity_article_change_class']/timeseries_data['t_activity_article'],filter_array,mode='same'))

    ax1.set_xticks([12+n*24 for n in range(0,number_of_days)])
    ax1.set_xticklabels(list_date,fontsize=11)
    ax1.grid(False)
    ax1.set_yscale('log')
    ax1.set_xlim((0,len(timeseries_data['t_activity_article'])))
    for n in range(0,number_of_days+1):#painting the lines dividing the days
        ax1.axvline(x=n*24,color='k',linestyle=':')
    for we_day in we_days: # painting the weekend days
        ax1.axvspan(24*(we_day-first_date.day), 24*(we_day-first_date.day+1), facecolor='green', edgecolor='none', alpha=.2)
    ax1.set_title('#(requêtes art-art qui changent de class)/#(requêtes art-art)',fontsize=14)
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
