
import copy
from typing import List, Tuple

import arrow
import pandas as pd

from cortex_common.utils.dataframe_utils import filter_recent_records_on_column, filter_time_column_before
from cortex_common.utils.dataframe_utils import head_as_dict
from cortex_common.utils.object_utils import unique_id, search_for_values_in_list
from cortex_common.utils.time_utils import derive_hour_from_date
from cortex_common.utils.time_utils import fold_start_and_stop_time_tuples_into_dict, time_is_within, oldest, newest
from cortex_profiles.datamodel.constants import CONTEXTS
from cortex_profiles.datamodel.dataframes import INSIGHT_ACTIVITY_COLS
from cortex_profiles.datamodel.dataframes import SESSIONS_COLS


# May never be used ... TODO ... make a decorator for this ...
def associate_insight_activity_with_user_sessions(insight_activity_df:pd.DataFrame, sessions_df:pd.DataFrame, time_column:str) -> pd.DataFrame:
    """
    :param insights_df: A dataframe with insights that were presented that captures the following information:
                1. The User that was presented the insight (profileId)
                2. The App the Insight was presented on (appId)
                3. The Time the insight was presented as an 1SO UTC Date (isoUTCPresentedTime)
    :param sessions_df:
    :return:
    """
    return pd.concat(
        [
            ua_df.reset_index(drop=True).assign(
                sessionId=associate_activity_with_sessions(
                    ua_df.reset_index(drop=True).rename(columns={time_column:INSIGHT_ACTIVITY_COLS.ACTIVITY_TIME}),
                    sessions_df[(sessions_df[SESSIONS_COLS.PROFILEID] == user_app_pair[0]) & (sessions_df[SESSIONS_COLS.APPID] == user_app_pair[1])]
                )
            )
            for user_app_pair, ua_df in insight_activity_df.groupby([INSIGHT_ACTIVITY_COLS.PROFILEID, INSIGHT_ACTIVITY_COLS.APPID])
        ]
    )


def associate_activity_with_sessions(activity_df:pd.DataFrame, sessions_df:pd.DataFrame) -> pd.DataFrame:
    sessions_df = sessions_df.assign(**{
        SESSIONS_COLS.ISOUTCSTARTTIME:sessions_df[SESSIONS_COLS.ISOUTCSTARTTIME].map(arrow.get),
        SESSIONS_COLS.ISOUTCENDTIME:sessions_df[SESSIONS_COLS.ISOUTCENDTIME].map(arrow.get)
    })
    return activity_df[INSIGHT_ACTIVITY_COLS.ACTIVITY_TIME].map(arrow.get).map(
        lambda x: head_as_dict(
            sessions_df[
                (sessions_df[SESSIONS_COLS.ISOUTCSTARTTIME].map(lambda y: x >= y)) &
                (sessions_df[SESSIONS_COLS.ISOUTCENDTIME].map(lambda y: x <= y))
                ]
        ).get(SESSIONS_COLS.ID)
    )


def derive_sessions_from_user_activity_df(user_activity_df: pd.DataFrame) -> pd.DataFrame:
    sessions_df = pd.concat(
        [
            derive_sessions_from_user_app_specific_activity(user, udf)
            for user, udf in user_activity_df.groupby(by=[INSIGHT_ACTIVITY_COLS.PROFILEID, INSIGHT_ACTIVITY_COLS.APPID])
        ],
        ignore_index=True
    )
    return sessions_df


def derive_sessions_from_user_activity(user_activity_df:pd.DataFrame, column_mapping:dict={}) -> pd.DataFrame:
    """
    :param user_activity_df: Needs a Data Frame that contains information regarding the following:
                1. The User With the Activity (profileId)
                2. The App the Activity was on (appId)
                3. The Start Time of the Activity as an 1SO UTC Date (isoUTCStartTime)
                4. The End Time of the Activity as an 1SO UTC Date (isoUTCEndTime)
    :param column_mapping: A dictionary mapping the names of the columns of the data frame that was passed in to the
                           columns expected as mentioned above ...
    :return: A dataframe of all the sessions derived ...
    """
    default_val = pd.DataFrame(columns = list(SESSIONS_COLS.keys()))
    return default_val if user_activity_df.empty else derive_sessions_from_user_activity_df(user_activity_df)


def derive_sessions_from_user_app_specific_activity(profile_app_tuple:str, user_app_specific_activity_df:pd.DataFrame) -> pd.DataFrame:
    profileId, appId = profile_app_tuple
    df = compute_sessions_times_from_activity_df(
        user_app_specific_activity_df[[INSIGHT_ACTIVITY_COLS.ISOUTCSTARTTIME, INSIGHT_ACTIVITY_COLS.ISOUTCENDTIME]].itertuples(index=False, name=None)
    )
    return df.assign(**{
        SESSIONS_COLS.CONTEXT: CONTEXTS.SESSION,
        SESSIONS_COLS.ID:[unique_id() for x in range(0, df.shape[0])],
        SESSIONS_COLS.PROFILEID:profileId,
        SESSIONS_COLS.APPID:appId,
        SESSIONS_COLS.ISOUTCSTARTTIME:df[SESSIONS_COLS.ISOUTCSTARTTIME].map(str),
        SESSIONS_COLS.ISOUTCENDTIME:df[SESSIONS_COLS.ISOUTCENDTIME].map(str),
        SESSIONS_COLS.DURATIONINSECONDS:df[[SESSIONS_COLS.ISOUTCSTARTTIME, SESSIONS_COLS.ISOUTCENDTIME]].apply(add_duration_to_login_time, axis=1)
    })


def compute_sessions_times_from_activity_df(startTime_stopTime_tuples:List[Tuple], session_threshold_mins:int=30) -> pd.DataFrame:
    """
    Key of the dict is when an activity started, value is when it ended ...
    For every start time ...
        is there another start time that is less than 30mins newer then it?
            if so, make the latest end time end time for the earlier start time and get rid of this row?
    """
    sessions = fold_start_and_stop_time_tuples_into_dict(
        map(lambda x: (arrow.get(x[0]), arrow.get(x[1])), startTime_stopTime_tuples)
    )
    for start_time, end_time in copy.deepcopy(sessions).items():
        if start_time not in sessions:
            # Skip whatever has been taken care of ...
            continue

        start_times_within_session_threshold = list(map(
            lambda x: x[0],
            search_for_values_in_list(
                sessions.items(),
                lambda start_time_end_time_tuple: (
                    time_is_within(start_time_end_time_tuple[0], start_time, dict(minutes=session_threshold_mins)) or
                    time_is_within(start_time_end_time_tuple[1], start_time, dict(minutes=session_threshold_mins))
                )
            )
        ))

        all_start_times = start_times_within_session_threshold + [start_time]
        all_end_times = [sessions[x] for x in start_times_within_session_threshold] + [end_time]
        # Find the oldest start time
        oldest_start_time = oldest(all_start_times)
        # Find the newest end time
        newest_end_time = newest(all_end_times)
        # Remove all of the start times involved in these queries ...
        for x in all_start_times:
            if x in sessions:
                del sessions[x]
        # Set the oldest start time with the newest end time ...
        sessions[oldest_start_time] = newest_end_time
    return pd.DataFrame([
        {SESSIONS_COLS.ISOUTCSTARTTIME: start_time, SESSIONS_COLS.ISOUTCENDTIME: end_time} for start_time, end_time in sessions.items()
    ])


def add_duration_to_login_time(startTime_endTime_tuple):
    return abs(startTime_endTime_tuple[0].float_timestamp - startTime_endTime_tuple[1].float_timestamp)


def append_hours_to_user_logins(logins_df:pd.DataFrame) -> pd.DataFrame:
    login_hours = list(map(derive_hour_from_date, logins_df["loggedIn"]))
    return logins_df.assign(
        hour=list(map(lambda x: x["hour"], login_hours)),
        hour_number=list(map(lambda x: x["hour_number"], login_hours)),
        timezone=list(map(lambda x: x["timezone"], login_hours))
    )


def filter_recent_sessions(sessions_df:pd.DataFrame, days_considered_recent=14) -> pd.DataFrame:
    return filter_recent_records_on_column(sessions_df, SESSIONS_COLS.ISOUTCENDTIME, days_considered_recent)


def filter_sessions_before(sessions_df:pd.DataFrame, days:int) -> pd.DataFrame:
    return filter_time_column_before(sessions_df, SESSIONS_COLS.ISOUTCENDTIME, {"days":-1*days})
