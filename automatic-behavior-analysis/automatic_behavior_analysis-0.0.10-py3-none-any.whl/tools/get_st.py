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
import os
import argparse
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser(description="Statistic analysis")
    parser.add_argument('--dir', help="Path to annotations", default='./')
    parser.add_argument('dog_name', nargs='?', help="Name of processes dog")
    args = vars(parser.parse_args())
    
    if len(args['dog_name']) > 0:
        name = args['dog_name']
    else:
        print("for correct work enter: python3 ./get_st.py dog_name")
        sys.exit(-1)

    dir_path = ""
    if args['dir'] is not None:
        dir_path = args['dir']     
    all_files = glob.glob(os.path.join(dir_path, name) + "*.csv")
    if len(all_files) == 0:
        print("csv file not found")
        sys.exit(1)

    output_statistic = pd.DataFrame(columns=['state', 'start time', 'end time', 'interval'])
    output_statistic_list = []
    input_statistic = None
    for filename in all_files:        
        df = pd.read_csv(filename, index_col='DateTime')
        if input_statistic is not None:
            input_statistic = pd.concat([input_statistic, df])
        else:
            input_statistic = df
    input_statistic = input_statistic.sort_index()

    interval_state = input_statistic.iloc[0]['moving_rate'] > 0.1
    interval_start_time = input_statistic.index[0]
    prev_state = interval_state
    last_time = input_statistic.index[0]
    #output_statistic.loc[0] = [prev_state, prev_time, None, None, None, None, None]
    for i in tqdm(range(1, len(input_statistic))):
        cur_time = input_statistic.index[i]        
        time_between_frames = pd.to_datetime(cur_time) - pd.to_datetime(last_time)
        state = input_statistic.iloc[i]['moving_rate'] > 0.2

        if ((time_between_frames.total_seconds() > 1) or
            (state == prev_state and state != interval_state)):
            # Собака пропадала из кадра надолго, ее состояние было не известно и это разные интервалы
            # или cостояние собаки изменилось
            # Заканчиваем интервал
            interval_length = pd.to_datetime(last_time) - pd.to_datetime(interval_start_time)
            if interval_length.total_seconds() > 0.05:
                # Если интервал имеет значимую длительность (больше одного кадра)

                new_period = {'state': interval_state, 
                                            'start time': interval_start_time,
                                            'end time':cur_time, 
                                            'interval':interval_length}
                output_statistic_list.append(new_period)

            # Выставляем новое начало и тип интервала
            interval_start_time = cur_time
            interval_state = state
        last_time = cur_time        
        prev_state = state
    output_statistic = pd.DataFrame(output_statistic_list, columns=['state', 'start time', 'end time', 'interval'])
    #output_statistic = pd.concat(output_statistic_list, ignore_index=True)
    output_statistic.to_csv(os.path.join(dir_path, 'st_'+ name +'.csv'))
    print('statistic save into st_' + name + '.csv')

if __name__ == "__main__":
    main()