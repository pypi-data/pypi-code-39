import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def barplot(ax, data_matrix, xticklabels=[], with_yerrs=False, yerrs=None, 
            color_list=[], width=0.3, space=0.1, data_series=[], ci=None, 
            return_data=False, return_rect=False, **kwargs):
    '''Make barplot from given data matrix.
    Parameters
    ----------
    ax: Axes
        object to be plotted
    data_matrix: nD list or list
        series of data lists
    yerrs: nD list or list
        series of yerr values lists. Shapes of data_matrix and yerrs should be
        the same if you would plot with yerrs.
            
    Dependencies
    ------------
    numpy
    matplotlib.pyplot
    get_barindex
    xticks
    make_plot_df

    '''
    # get data shape
    data_shape = np.array(data_matrix).shape
    if len(data_shape) == 1:
        data_shape = (1, data_shape[0])
        data_matrix = [data_matrix]
        yerrs = [yerrs]
    # get index
    x, index = get_barindex(data_shape, width=width, space=space, slide=1)
    # set existing defalt parameters into kwargs
    kwargs['width'] = width
    # plot
    rects = []
    for i in range(data_shape[0]):
        if with_yerrs:
            kwargs['yerr'] = yerrs[i]
        if data_series:
            kwargs['label'] = data_series[i]
        if color_list:
            kwargs['color'] = color_list[i]
        rect = ax.bar(x[i], data_matrix[i], **kwargs)
        rects.append(rect)

    ax.set_xticks(xticks(index, width, data_shape[0]))
    if 'label' in kwargs:
        ax.legend(loc='best')
    if len(xticklabels) > 0:
        ax.set_xticklabels(xticklabels)
    if return_data and return_rect:
        return make_plot_df(data_matrix, xticklabels, yerrs, data_series, ci), \
            rects
    if return_data:
        return make_plot_df(data_matrix, xticklabels, yerrs, data_series, ci)
    if return_rect:
        return rects

def get_barindex(data_shape, width=0.3, space=0.1, slide=1):
    '''
    Parameters
    ----------
        data_shape: list or tuple
            first value indicates number of data series and second value indicates
            number of bars for each series. For example, (2, 6) indicates that
            there are two series of data conataining 6 categories.
    Return
    ------
        x: seiries_num dimentional list
            x contains series number of lists. each list is consist of category number of
            series of values indicating positions of bars.
    '''
    series_num = data_shape[0]
    data_num = data_shape[1]
    d = (space + width) * series_num
    index = np.linspace(1, 1+d * data_num, data_num, endpoint=True)
    x = [index+width*i for i in range(series_num)]
    return x, index

def xticks(index, width, series_num):
    return index+(width/2)*(series_num-1)

def make_plot_df(data_matrix, xticklabels, yerrs=[], data_series=[], ci=None):
    '''Return df containing plotted data'''
    df = pd.DataFrame(index=[], columns=[])
    df['x'] = xticklabels
    if yerrs:
        if not ci:
            raise Exception('Specify CI percentage if you input yerrs.')
    if len(np.array(data_matrix).shape) == 1:
        data_matrix = [data_matrix]
        yerrs = [yerrs]
    else:
        if not data_series:
            raise Exception('Specify series of data if you input multi-D data.')
    for i in range(len(data_matrix)):
        df['{}_y'.format(data_series[i])] = data_matrix[i]
        if yerrs:
            df['{}_CI{}_L'.format(data_series[i], ci)] = yerrs[i][0]
            df['{}_CI{}_H'.format(data_series[i], ci)] = yerrs[i][1]
    return df
