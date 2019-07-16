import pandas as pd

def weblog_sessionizer(weblog,weblog_columns_dict,cutoff_minutes=30):
    """
    Sessionize weblog in sessions: as long as a group of requests have the same user_id and no inactivity in 30 minutes this is a session"
    """
    weblog = weblog.copy(deep=True)
    # sort by timestamp
    weblog.sort_values(by=[weblog_columns_dict['user_id_column'],weblog_columns_dict['timestamp_column']],ascending=[True,True],inplace=True)
    # Detect time jumps greater than threshold
    gt_xmin = weblog[weblog_columns_dict['timestamp_column']].diff() > pd.Timedelta(minutes=cutoff_minutes)
    # Detect changes of user
    diff_user = weblog[weblog_columns_dict['user_id_column']] != weblog[weblog_columns_dict['user_id_column']].shift()
    weblog['session_id'] = (diff_user | gt_xmin).cumsum()
    return weblog['session_id'];
