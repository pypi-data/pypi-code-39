import os
import json

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

import datetime
import tscleaner.dataframe as datfram
import tscleaner.reservoir_series as resser

import warnings
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
warnings.simplefilter('ignore', UserWarning)

plt.rcParams.update({'figure.max_open_warning': 0})
plt.style.use('seaborn-whitegrid')
font = {'size': 20}
plt.rc('font', **font)


def process(file, path_data, path_figure, redo_figures=False):

    fn = os.path.join(path_data, file)

    if os.path.exists(path_figure + file + '.png') and redo_figures is False:
        # figure already exists
        return

    d = datfram.dataframe(fn)

    if not len(d.index.values):
        # no values in dataset
        return

    d_new, d_out = datfram.remove_double_dates(data_original=d)
    d_new_temp_1 = datfram.remove_outliers_frac(d_new, thres_fraction=0.5)[0]

    if len(d_new.index) >= 2:
        if max(d_new.water_area_filled) > 1e7:
            d_daily = resser.daily_values(d_new_temp_1, inter_method='slinear',
                                          mirroring=4)
            d_new_temp_2 = datfram.remove_outliers_quantile(
                                                            d_daily,
                                                            d_new_temp_1,
                                                            window=100,
                                                            f_std=2,
                                                            thres_quant=0.90
                                                           )[0]
        else:
            d_new_temp_2 = d_new

        d_daily_2 = resser.daily_values(d_new_temp_2, inter_method='slinear',
                                        mirroring=4)
        d_new_2, d_out_2 = datfram.remove_outliers_std(d_new,
                                                       d_daily_2,
                                                       window=180,
                                                       f_std=2)
        d_daily_3 = resser.daily_values(d_new_2, inter_method='slinear',
                                        mirroring=4)
        band_high, band_low = resser.confidence_band(d_daily_3)
        d_daily_4 = resser.daily_values(d_new_2, inter_method='akima',
                                        mirroring=4)
        wavelet = resser.wavelets(d_daily_4, wave_name='db25',
                                  level=8, level_output=4)
        steps = resser.steps(wavelet, window=365, threshold=0.5)

        d_out = pd.concat([d_out, d_out_2], sort=False)
        d_new = d_new_2

    # Create figure
    fig = plt.figure(figsize=(35, 20))
    grid = plt.GridSpec(3, 4, wspace=0.2, hspace=0.2)

    ax1 = plt.subplot(grid[:2, 0:])
    ax2 = plt.subplot(grid[2, 0])
    ax3 = plt.subplot(grid[2, 1])
    ax4 = plt.subplot(grid[2, 2:])

    years = mdates.YearLocator()
    ax1.xaxis.set_major_locator(years)
    ax1.set_xlim([datetime.date(1985, 1, 1), datetime.date(2019, 1, 1)])
    ax1.set_ylim(0, 1.05*max(d.water_area_filled.values))

    ax1.title.set_text(file)

    ax1.plot(d_new.index, d_new.water_area_filled, 'k.',
             label='Preserved datapoints', alpha=0.7)
    ax1.plot(d_out.index, d_out.water_area_filled, 'r.',
             label='Removed datapoints', alpha=0.2)
    ax1.fill_between(band_high.index,
                     band_high.area,
                     band_low.area,
                     facecolor='r',
                     alpha=0.1,
                     label='Confidence band')
    ax1.plot(wavelet, ls='-', linewidth=3,
             color='red', alpha=0.4,
             label='Wavelets datapoints, type: db25, level=4')
    if len(steps) != 0:
        for i in range(len(steps)):
            if steps.up_down.values[i] > 0:
                ax1.axvline(x=steps.index[i], c='k',
                            linestyle='dashed', alpha=0.5)
            else:
                ax1.axvline(x=steps.index[i], c='r',
                            linestyle='dashed', alpha=0.5)
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Surface Area Reservoir [m²]')
    ax1.legend(frameon=True)

    ax2.title.set_text('fraction')
    ax2.plot(d_new.index, d_new.water_area_filled_fraction, 'k.')
    ax2.plot(d_out.index, d_out.water_area_filled_fraction, 'r.')
    ax2.set_ylim(0, 0.65)
    ax2.axhline(y=0.5, c='r', alpha=0.4)
    ax2.tick_params(labelrotation=90)

    ax3.title.set_text('-p')
    ax3.plot(d_new.index, -d_new.water_area_p, 'k.')
    ax3.plot(d_out.index, -d_out.water_area_p, 'r.')
    ax3.set_ylim(-1, 0)
    ax3.tick_params(labelrotation=90)

    wl_max = wavelet.rolling(window=365*2, min_periods=1, center=True).max()
    wl_min = wavelet.rolling(window=365*2, min_periods=1, center=True).min()
    wl_dif = wl_max.copy(deep=True)
    wl_dif.area = wl_max.area-wl_min.area
    wl_dif_std = np.std(wl_dif.area)
    wl_dif_med = np.median(wl_dif.area)
    window = max(wavelet.area.values)-min(wavelet.area.values)

    ax4.title.set_text('envelope distances')
    ax4.plot(wavelet, 'm-', label='wavelet estimation', alpha=0.4)
    ax4.plot(wl_max, label='max', alpha=0.2)
    ax4.plot(wl_min, label='min', alpha=0.2)

    ax5 = ax4.twinx()
    # ax5.axhline(y=2*wl_dif_std+wl_dif_med, c='k')
    # ax5.axhline(y=wl_dif_med, c='k')
    ax5.plot(wl_dif/window, label='dif')
    ax5.set_ylim(0, 1)

    ax4.set_xlabel('Date')
    ax4.set_ylabel('Surface Area Filled [m²]')
    ax4.legend(frameon=True, prop={'size': 7})

    plt.savefig(path_figure + file + '.png')
    plt.clf()

    # print(file + '.png is made')
    return
