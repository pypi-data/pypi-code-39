#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Скрипт сводит файлы со статистикой следующего формата: Bob_01_20180118110000.csv
	DateTime	y1	y2	x1	x2	state	rate
0	2018-01-18 11:00:00.000	0.05515958368778229	0.3669011890888214	0.45685988664627075	0.7031605839729309	sleep	0.999748170375824
1	2018-01-18 11:00:00.100	0.05515958368778229	0.3669011890888214	0.45685988664627075	0.7031605839729309	sleep	0.999748170375824
2	2018-01-18 11:00:00.200	0.05515958368778229	0.3669011890888214	0.45685988664627075	0.7031605839729309	sleep	0.999748170375824
3	2018-01-18 11:00:00.300	0.05515958368778229	0.3669011890888214	0.45685988664627075	0.7031605839729309	sleep	0.999748170375824
4	2018-01-18 11:00:00.400	0.05515958368778229	0.3669011890888214	0.4568598866462708	0.7031605839729309	awake	0.999748170375824
5	2018-01-18 11:00:00.500	0.05515958368778229	0.3669011890888214	0.45685988664627086	0.7031605839729309	awake	0.999748170375824
...

в файл со статистикой следующего формата: st_Bob.csv
   state               start time                 end time                interval
0  sleep  2018-01-18 11:00:00.000  2018-01-18 11:00:00.400  0 days 00:00:00.400000
1  awake  2018-01-18 11:00:00.400  2018-01-18 11:00:00.600  0 days 00:00:00.200000
2  sleep  2018-01-18 11:00:00.600  2018-01-18 11:00:01.000  0 days 00:00:00.400000
3  awake  2018-01-18 11:00:01.000  2018-01-18 11:00:11.100  0 days 00:00:10.100000
...

для корректной работы необходимо поместить скрипт в папку с файлами dog_name*.csv, 
при запуске передать в командной строке имя собаки (пример: python3 ./get_st.py Bob) 
'''

import pandas as pd
import datetime
import glob
import sys


def main():
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        print("for correct work enter: python3 ./get_st.py dog_name")
        sys.exit(1)

    all_files = glob.glob(name + "*.csv")
    if len(all_files) == 0:
        print("csv file not found")
        sys.exit(1)

    input_statistic_list = []
    output_statistic_list = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col='DateTime')
        input_statistic_list.append(df)

    for df in input_statistic_list:

        df2 = pd.DataFrame(columns=['state', 'start time', 'end time', 'interval', 'low activity time', 'mid activity time', 'high activity time'])
        prev_state = df.iloc[0]['state']
        prev_time = df.index[0]
        df2_index = 0
        df2.loc[0] = [prev_state, prev_time, None, None, None, None, None]

        #TODO: придумать другой способ узнать время между кадров
        time_between_frames = pd.to_datetime(df.index[1]) - pd.to_datetime(df.index[0])

        low_act_tm = pd.Timedelta(0)
        mid_act_tm = pd.Timedelta(0)
        high_act_tm = pd.Timedelta(0)

        len_df = len(df)

        for i in range(1, len_df):

            if df.iloc[i]['moving_rate'] < 0.1:
                low_act_tm += time_between_frames
            elif df.iloc[i]['moving_rate'] < 0.3:
                mid_act_tm += time_between_frames
            else:
                high_act_tm += time_between_frames

            if df.iloc[i]['state'] != prev_state:
                interval = pd.to_datetime(df.index[i]) - pd.to_datetime(prev_time)
                df2.loc[df2_index] = [prev_state, prev_time, df.index[i], interval, low_act_tm, mid_act_tm, high_act_tm]

                prev_state = df.iloc[i]['state']
                prev_time = df.index[i]
                df2_index += 1


            elif i + 1 == len_df:
                interval = pd.to_datetime(df.index[i]) - pd.to_datetime(prev_time)
                df2.loc[df2_index] = [prev_state, prev_time, df.index[i], interval, low_act_tm, mid_act_tm, high_act_tm]

        output_statistic_list.append(df2)

    out = pd.concat(output_statistic_list)
    out.to_csv('st_'+ name +'.csv')
    print('statistic save into st_' + name + '.csv')

if __name__ == "__main__":
    main()