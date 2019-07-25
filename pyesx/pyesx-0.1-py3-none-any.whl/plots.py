"""
Library for standard plots used to vizualize ESX data

A. Enguehard - 07/2019
"""

import matplotlib.pyplot as plt


def p24H(values=None, h='UNDEF', fill=True, dbg=False, label='UNDEF', color='b', linestyle='-'):
    """Compute the mean 24H serie from a given time serie and plot it

    Parameters:
    -----------
    * values : (pd.Serie)
        dataseries used to compoyte the 24H cycle
        ex: run.data['O3']['Concs'][10] : series of ozone content at 10m
    """
    groups = values.groupby(values.index.hour)
    mean = groups.mean()
    std = groups.std()
    time = mean.index

    if dbg is True:
        print('Mean : ')
        print(mean)

    if fill is True:
        plt.plot(time, mean, 'o-', label=label + ' Height: ' + str(h) + 'm',
                 color=color, linestyle=linestyle)
        plt.fill_between(time, mean-std, mean+std, alpha=0.5, color=color)
    else:
        plt.plot(time, mean, 'o-', label=label + ' Height: ' + str(h) + 'm',
                 color=color, linestyle=linestyle)
    return


def profiles_at_t(list_runs, spcs, var, t, zscale='mid', divz=False, meas=False, meas_file=None, meas_var_name=None, ax=None, metadata=True):
    """ Helps for comparing profiles from different runs.

    If you want to compare profiles at different times within one run you
    shoudl use "self._plot_profiles_mean_at_t" instead.

    Parameters:
    -----------
    """
    fig, axe = plt.subplots(1)
    # Plot all the runs without metadata
    if len(list_runs) > 0:
        for exp in list_runs[1:]:
            exp._plot_profiles_mean_at_t(spcs, var, [t], zscale=zscale,
                                         meas=False, meas_file=meas_file,
                                         meas_var_name=meas_var_name,
                                         metadata=False, ax=axe, divz=divz)
    # Plot the first one with all the data:
    list_runs[0]._plot_profiles_mean_at_t(spcs, var, [t],
                                          zscale=zscale, meas=meas,
                                          meas_file=meas_file,
                                          meas_var_name=meas_var_name,
                                          metadata=True, ax=axe, divz=divz)
    return
