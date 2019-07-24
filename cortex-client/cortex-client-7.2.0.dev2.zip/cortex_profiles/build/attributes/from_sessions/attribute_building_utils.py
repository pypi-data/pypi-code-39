from collections import Counter
from typing import List, Tuple

import pandas as pd

from cortex_common.utils.dataframe_utils import determine_count_of_occurrences_of_grouping, \
    determine_time_spent_on_occurrences_of_grouping
from cortex_common.utils.time_utils import derive_day_from_date
from cortex_profiles.build.attributes.from_sessions.etl_utils import filter_recent_sessions, append_hours_to_user_logins
from cortex_profiles.datamodel.dataframes import SESSIONS_COLS, DAILY_LOGIN_COUNTS_COL, \
    LOGIN_COUNTS_COL, LOGIN_DURATIONS_COL, DAILY_LOGIN_DURATIONS_COL


def group_daily_login_counts(sessions_df:pd.DataFrame) -> pd.DataFrame:
    daily_login_count_df = derive_daily_login_counts(sessions_df)
    columns_to_keep = [
        DAILY_LOGIN_COUNTS_COL.PROFILEID, DAILY_LOGIN_COUNTS_COL.APPID, DAILY_LOGIN_COUNTS_COL.DAY,
                       DAILY_LOGIN_COUNTS_COL.TOTAL]
    return daily_login_count_df[columns_to_keep].groupby([
        DAILY_LOGIN_COUNTS_COL.APPID, DAILY_LOGIN_COUNTS_COL.PROFILEID
    ], as_index=False) if (not daily_login_count_df.empty) else pd.DataFrame(columns=columns_to_keep)


def group_daily_login_durations(sessions_df:pd.DataFrame) -> pd.DataFrame:
    columns_to_keep = [SESSIONS_COLS.PROFILEID, SESSIONS_COLS.APPID, SESSIONS_COLS.DURATIONINSECONDS]
    return derive_daily_login_duration(sessions_df)[columns_to_keep].groupby(
        [SESSIONS_COLS.PROFILEID, SESSIONS_COLS.APPID], as_index=False
    ) if (not sessions_df.empty) else pd.DataFrame(columns=columns_to_keep)



# ----------------------------------------------------------------------


def derive_count_of_user_logins(sessions_df:pd.DataFrame) -> pd.DataFrame:
    return determine_count_of_occurrences_of_grouping(
        sessions_df[[
            LOGIN_COUNTS_COL.PROFILEID,
            LOGIN_COUNTS_COL.APPID,
        ]],
        [
            LOGIN_COUNTS_COL.PROFILEID,
            LOGIN_COUNTS_COL.APPID
        ],
        LOGIN_COUNTS_COL.TOTAL
    )


def derive_time_users_spent_logged_in(sessions_df:pd.DataFrame) -> pd.DataFrame:
    return determine_time_spent_on_occurrences_of_grouping(
        sessions_df,
        [LOGIN_DURATIONS_COL.PROFILEID, LOGIN_DURATIONS_COL.APPID],
        LOGIN_DURATIONS_COL.DURATION
    )


def derive_daily_login_counts(sessions_df:pd.DataFrame) -> pd.DataFrame:
    """
    #Refactor: Can I use the profile instead of the logins df?
    #Refactor: Can I adjust day based on timezone if available ...
        # - If you learned someone's timezone ... do you have to shift all of the historic data? or only the new stuff you are computing???
    :param logins_df:
    :return:
    """
    daily_logins = [
        derive_total_logins_on_specific_dates(user_app_tuple, sessions_df)
        for user_app_tuple, sessions_df in sessions_df.groupby([DAILY_LOGIN_COUNTS_COL.PROFILEID, DAILY_LOGIN_COUNTS_COL.APPID])
    ]
    return pd.concat(daily_logins, ignore_index=True) if daily_logins else pd.DataFrame(columns=list(sessions_df.columns) + [DAILY_LOGIN_COUNTS_COL.DAY])


def derive_average_of_daily_login_counts(sessions_df:pd.DataFrame) -> pd.DataFrame:
    # Groups all of the different counts
    groups = group_daily_login_counts(sessions_df)
    return groups.mean().reset_index() if (not (isinstance(groups, pd.DataFrame) and groups.empty)) else groups


def derive_daily_login_duration(logins_df:pd.DataFrame) -> pd.DataFrame:
    login_dfs = [
        derive_user_date_login_duration_df(user_app_tuple, user_logins_df)
        for user_app_tuple, user_logins_df in logins_df.groupby([DAILY_LOGIN_DURATIONS_COL.PROFILEID, DAILY_LOGIN_DURATIONS_COL.APPID])
    ]
    return pd.concat(login_dfs, ignore_index=True) if login_dfs else pd.DataFrame(columns=list(logins_df.columns) + [DAILY_LOGIN_DURATIONS_COL.DAY])


def derive_recent_daily_login_duration(sessions_df:pd.DataFrame) -> pd.DataFrame:
    return derive_daily_login_duration(filter_recent_sessions(sessions_df))


def derive_average_of_daily_login_durations(sessions_df:pd.DataFrame) -> pd.DataFrame:
    groups = group_daily_login_durations(sessions_df)
    return groups.mean().reset_index() if (not (isinstance(groups, pd.DataFrame) and groups.empty)) else groups


def derive_average_of_recent_daily_login_durations(sessions_df:pd.DataFrame) -> pd.DataFrame:
    return derive_average_of_daily_login_durations(filter_recent_sessions(sessions_df))

# --------------------------------------------------------------------------------------------


def derive_user_date_login_duration_df(user_app_tuple:str, sessions_df:pd.DataFrame) -> pd.DataFrame:
    user_login_duration_df = sessions_df.reset_index()
    user_login_duration_df[DAILY_LOGIN_DURATIONS_COL.DAY] = user_login_duration_df[SESSIONS_COLS.ISOUTCSTARTTIME].map(derive_day_from_date)
    user_login_duration_df = determine_time_spent_on_occurrences_of_grouping(
        user_login_duration_df,
        [DAILY_LOGIN_DURATIONS_COL.APPID, DAILY_LOGIN_DURATIONS_COL.PROFILEID, DAILY_LOGIN_DURATIONS_COL.DAY],
        DAILY_LOGIN_DURATIONS_COL.DURATION
    )
    return user_login_duration_df


def derive_count_of_hourly_logins(logins_df:pd.DataFrame) -> pd.DataFrame:
    return pd.concat([
        derive_user_hour_login_count_df(user_app_tuple, user_logins_df)
        for user_app_tuple, user_logins_df in append_hours_to_user_logins(logins_df).groupby(["user", "app"])
    ])


def derive_user_hour_login_count_df(user_app_tuple:Tuple, user_logins_df:pd.DataFrame) -> pd.DataFrame:
    return user_logins_df.groupby("hour").size().reset_index().rename(columns={0:"logins"}).assign(
        user = user_app_tuple[0],
        app = user_app_tuple[1]
    )


def derive_total_logins_on_specific_dates(user_app_tuple:List, user_sessions_df:pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame([
        {
            DAILY_LOGIN_COUNTS_COL.PROFILEID: user_app_tuple[0],
            DAILY_LOGIN_COUNTS_COL.APPID: user_app_tuple[1],
            DAILY_LOGIN_COUNTS_COL.DAY: date,
            DAILY_LOGIN_COUNTS_COL.TOTAL: count
        } for date, count in Counter(user_sessions_df[SESSIONS_COLS.ISOUTCSTARTTIME].map(derive_day_from_date)).items()
    ])


if __name__ == "__main__":
    pass