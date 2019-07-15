import os
import json

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from tqdm import tqdm

import datetime
import reservoir_series as rs

plt.style.use('seaborn-whitegrid')
font = {'size': 20}
plt.rc('font', **font)

path_data = 'C:/src/paper-global-reservoirs/data/time_series/'

n = 0
n_max = 250

errors = pd.DataFrame({'error': np.full(n_max, np.NaN),
                       'area': np.full(n_max, np.NaN)})

with tqdm(total=n_max) as pbar:
    for file in os.listdir(path_data):

        d = json.loads(open(path_data+file).read())
        date = d['features'][0]['properties']['water_area_time']
        if not len(date):
            n += 1
            pbar.update(1)

            if n >= n_max:
                break

        else:
            date = [datetime.datetime.fromtimestamp(tt / 1000).date()
                    for tt in date]
            area = d['features'][0]['properties']['water_area_filled']

            data = pd.DataFrame({'date': date,
                                 'area': area})

            daily_data = rs.daily_values(data, inter_method='akima')
            savgol = rs.savitzky_golay(daily_data,
                                       window_length=201, polyorder=4)

            error = 0
            j = 0
            for i in range(len(savgol.index)):
                if savgol.index[i].date() == date[j]:
                    error += abs((savgol.area[i]-area[j])/area[j])
                    j += 1

            a = d['features'][0]['properties']['area']
            if a < 0:
                errors.error[n] = np.nan
                errors.area[n] = np.nan
            else:
                errors.error[n] = error/len(date)
                errors.area[n] = d['features'][0]['properties']['area']

            n += 1
            pbar.update(1)

            if n >= n_max:
                break

fig = plt.figure(figsize=(35, 12))

plt.xlim(0, 5e7)
plt.ylim(0, 1)
plt.title('errors vs. areas')

plt.plot(errors.area, errors.error, 'k.', ms=5, alpha=0.3)

plt.xlabel('Surface Area Reservoir [m²]')
plt.ylabel('Mean Absolute Error')

plt.savefig('errors_vs_area_small.png')

fig = plt.figure(figsize=(35, 12))
plt.title('errors vs. areas')

plt.plot(errors.area, errors.error, 'k.', ms=5, alpha=0.3)

plt.xlabel('Surface Area Reservoir [m²]')
plt.ylabel('Mean Absolute Error')

plt.savefig('errors_vs_area_full.png')
