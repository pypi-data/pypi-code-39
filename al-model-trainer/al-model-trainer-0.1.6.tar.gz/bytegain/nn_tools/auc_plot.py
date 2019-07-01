"""
Plots AUC for binary classifier
"""

import numpy
import numpy.ma
import matplotlib
import sys
import csv
from scipy.stats import binom
from sklearn import metrics
from enum import Enum

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def create_total_pos(results):
    """Returns a list of cumulative fraction of positive examples.
    The lengt of the list is max(1, number of negative examples)"""
    length = len(results)
    #total_pos = numpy.zeros([length], dtype=numpy.float)
    total_pos = [0.0]
    for i in range(0, length):
        pos = results[i]['label']
        if pos:
            total_pos[-1] += 1
        else:
            total_pos.append(total_pos[-1])
    pos_count = total_pos[-1]
    if length == 0 or pos_count == 0:
        raise Exception("WARNING: bad data for results,total_pos: %d %d"% (length, pos_count))

    total_pos = numpy.array(total_pos)
    total_pos /= pos_count
    return total_pos

def compute_auc(results):
    y_true = [result['label'] for result in results]
    y_pred = [result['probability'] for result in results]
    # y_pred_label = [1 if result['probability'] > 0.5 else 0 for result in results]
    fpr, tpr, thresholds = metrics.roc_curve(y_true, y_pred)
    return metrics.auc(fpr, tpr)


def compute_metrics(results, threshold=0.5):
    y_true = [result['label'] for result in results]
    y_pred = [result['probability'] for result in results]
    y_pred_label = [1 if result['probability'] > threshold else 0 for result in results]

    metrs = {
        'precision': metrics.precision_score(y_true, y_pred_label),
        'recall': metrics.recall_score(y_true, y_pred_label),
        'accuracy': metrics.accuracy_score(y_true, y_pred_label)
    }

    fpr, tpr, thresholds = metrics.roc_curve(y_true, y_pred)
    metrs['auc'] = metrics.auc(fpr, tpr)
    # Find fpr and tpr for a given threshold
    thresholds = thresholds.tolist()
    index = binary_search_reverse(thresholds, threshold)
    metrs['false_positive_rate'], metrs['true_positive_rate'] = fpr[index], tpr[index]

    # All metrics are numpy floats - convert them to python float
    for key, value in metrs.iteritems():
        metrs[key] = value.item()

    conf_mtr = metrics.confusion_matrix(y_true, y_pred_label)
    metrs['confusion_mtr'] = numpy.ndarray.tolist(conf_mtr)
    return metrs


# Binary search in a reversely sorted array
def binary_search_reverse(a, x):
    lo = 0
    hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        mid_element = a[mid]
        if mid_element > x:
            lo = mid+1
        else:
            hi = mid
    return lo

def sort_results(results):
    results.sort(key=lambda v: v['probability'], reverse=True)


"""
Computes actual & predicted values for each "bucket" in the sorted
result list.
bucket_fractions is an array of floats, where each value represents
the fraction of results to use for that bucket.
bucket_fractions should sum to <1 (the remainder is used for the last bucket)
"""


def get_buckets(results, bucket_fractions):
    count = len(results)
    # Last bucket is "remainer"
    bucket_count = len(bucket_fractions) + 1
    breakpoints = [0] * bucket_count
    fraction_sum = 0.0
    for i in range(len(bucket_fractions)):
        fraction_sum += bucket_fractions[i]
        breakpoints[i] = int(fraction_sum * count)

    breakpoints[len(bucket_fractions)] = count
    actual = []
    predicted = []
    confidence = []
    prev_end = 0
    for i in range(bucket_count):
        bucket_size = breakpoints[i] - prev_end
        pred_sum = 0.0
        actual_sum = 0.0
        for j in range(prev_end, breakpoints[i]):
            pred_sum += results[j]['probability']
            if results[j]['label']:
                actual_sum += 1.0

        actual_val = actual_sum / bucket_size
        actual.append(actual_val)
        predicted.append(pred_sum / bucket_size)
        conf = binom.interval(0.95, bucket_size, actual_val)
        confidence.append(conf[1] / bucket_size - actual_val)
        prev_end = breakpoints[i]

    return actual, predicted, confidence


def plot_predicted_vs_actual(filename, results, smoothing=500):
    print ("Plot datapoints: %d Smoothing: %d" % (len(results), smoothing))
    length = len(results)
    preds = []
    leases = []
    np_lease = numpy.zeros([length])
    np_prob = numpy.zeros([length])
    for i in range(length):
        np_prob[i] = results[i]['probability']
        if results[i]['label']:
            np_lease[i] = 1.0

    for i in range(length - smoothing):
        leases.append(numpy.ma.average(np_lease[i:i + smoothing]))
        preds.append(numpy.ma.average(np_prob[i:i + smoothing]))
    do_plot_predicted_vs_actual(filename, preds, leases)


def do_plot_predicted_vs_actual(filename, predictions, actual, x_values, use_percent=True, x_axis_label=None, y_axis_label=None):
    length = len(predictions)
    assert length > 1
    # print "input length: %d" % length
    plt.clf()
    if use_percent:
        predictions = [x * 100 for x in predictions]
        actual = [x * 100 for x in actual]

    max_val = max([predictions[0], actual[0], predictions[-1], actual[-1]]) * 1.1
    plt.subplots_adjust(left=0.1, right=0.97, top=0.98, bottom=0.09, wspace=0.0, hspace=0.0)
    # print ("length: %s" % str(length + (length / 10 - 1)))
    xrange = numpy.arange(0, 11)
    xrange = xrange * (length) / 10.0
    # print "predictions: %s" % str(predictions)
    plt.xticks(xrange)
    ax = plt.gca()
    if use_percent:
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: "%3d%%" % (float(x) * 100 / (length))))
    else:
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: "%3.1f" % (float(x) / (length))))
    ax.set_ylim([0, max_val])
    ax.set_autoscale_on(False)
    plt.grid(b=True, which='major', axis='y', color='0.3', linestyle='-', alpha=0.3, linewidth=0.3)
    lines = []
    if x_axis_label != None:
        plt.xlabel(x_axis_label)

    if y_axis_label != None:
        plt.ylabel(y_axis_label)
    # Reverse x values so plot goes Up & to the Right.
    x_values = [length - x for x in x_values]
    line, = plt.plot(x_values, predictions, "b-", linewidth=1, antialiased=True, label="predictions")
    lines.append(line)
    if actual != None:
        # plot_x = numpy.arange(0, length, length / float(len(actual)))
        line, = plt.plot(x_values, actual, "g-", linewidth=1, antialiased=True, label="actual")
        lines.append(line)
    plt.legend(handles=lines)
    plt.savefig(filename, dpi=300)


def get_predicted_vs_actual(results, points=None, min_positive_per_point = 100):
    length = len(results)

    # Compute the minimum # of samples per point.
    # We want 1000 positive (or negative if they are rarer) examples per point.
    actual = 0
    for j in range(0, length):
        if results[j]['label']:
            actual += 1.0

    if actual < min_positive_per_point * 3:
        min_positive_per_point = actual / 3

    if points is not None:
        delta = float(length)/points
        stop_points = [int(i * delta) - 1 for i in range(1, points+1)]
    else:
        stop_points = []

    min_distance = length / 100
    actual_points = []
    pred_points = []
    ece = 0.0  # Expected calibration error
    x_values = []
    last_point = 0
    pred = 0.0
    actual = 0.0
    # Compute positive rate in top 10% bucket
    actual_ten_percent = 0.0
    count_ten_percent = int(len(results)*0.1)
    for i, point in enumerate(results):
        pred += results[i]['probability']
        if results[i]['label']:
            if i < count_ten_percent:
                actual_ten_percent += 1.0
            actual += 1.0

        if (((actual > min_positive_per_point and i - last_point > min_distance) or i == len(results) - 1) and points is None) or i in stop_points:
            count = i - last_point + 1
            accuracy = actual / count  # accuracy
            confidence = pred / count  # confidence
            ece += count * abs(accuracy - confidence)

            # Hack so end points are 0%/100%
            x_values.append( float(i) if i == len(results) -1 else float(last_point))
            actual_points.append(accuracy)
            pred_points.append(confidence)
            last_point = i
            actual = 0.0
            pred = 0.0

    ece = ece / length

    print "Positive rate in top 10 percent: %s " % (actual_ten_percent/count_ten_percent)

    x_values = [(x * len(x_values)) / length for x in x_values]
    # print "Expected Calibration Error: %.4f." % ece
    return ece, pred_points, actual_points, x_values


def plot_predicted_vs_actual2(filename, results, points=None, use_percent=True, x_axis_label=None, y_axis_label=None):
    ece, pred_points, actual_points, x_values = get_predicted_vs_actual(results, points)
    do_plot_predicted_vs_actual(filename, pred_points, actual_points, x_values, use_percent, x_axis_label, y_axis_label)
    return ece


class PlotType(Enum):
    percent = 'percent'
    odds_ratio = 'odds_ratio'
    percent_of_total = 'percent_of_total'

    def __str__(self):
        return self.value

def plot_by_segment(filename, results, y_axis_label = None, title = None, plot_type = PlotType.percent_of_total,
                    buckets = None):
    """

    :param filename: Image file to create
    :param results: Sorted result set
    :param y_axis_label: Graph label for y Axis
    :param title: Plot title
    :return: sums: Ratio/percentage of positive events in each bucket
    """
    if buckets == None:
        buckets = (0.2, 0.2, 0.2, 0.2, 0.2)
    plt.clf()
    fig, ax = plt.subplots()
    labels = ('Very High', 'High', 'Med', 'Low', 'Lowest')
    labels = labels[0:len(buckets)]
    labels_perc = []
    for i in xrange(len(buckets)):
        labels_perc.append(labels[i]+'\n'+str(int(buckets[i]*100))+'%')
    buckets = numpy.array(buckets)
    cumsum = numpy.cumsum(buckets)
    length = len(results)
    y_pos = numpy.arange(len(labels))
    sums = []
    current_count = 0.0
    current_sum = 0.0
    target =  cumsum[0] * length
    total_positive = 0.0
    for example in results:
        if example['label']:
            total_positive +=1

    if total_positive == 0.0:
        raise Exception("No positive results")

    print "Plot type: %s           " % plot_type
    if plot_type == PlotType.odds_ratio:
        total = 0
        for result in results:
            if result['label']:
                total += 1
        average = total / float(length)
        multiplier = 1.0 / average
    elif plot_type == PlotType.percent:
        multiplier = 100
    elif plot_type == PlotType.percent_of_total:
        multiplier = 100
    else:
        raise Exception("Unknown plot_type: %s %s" % (plot_type, type(plot_type)))

    for i in range(length):
        current_count += 1
        if results[i]['label']:
            current_sum += 1
        if i <= target and (i+1) > target or i == length - 1:
            if plot_type == PlotType.percent_of_total:
                sums.append(current_sum / total_positive * multiplier)
            else:
                sums.append(current_sum / current_count * multiplier)

            current_sum = 0.0
            current_count = 0.0
            if len(sums) < len(buckets):
                target = cumsum[len(sums)] * length

    plt.subplots_adjust(left=0.12, right=0.98, top=0.95, bottom=0.13, wspace=0.0, hspace=0.0)
    bars = plt.bar(y_pos, sums, align='center', alpha=0.5)
    for bar in bars:
        height = bar.get_height()
        bottom, top = ax.get_ylim()
        yrange = (top - bottom)
        if height > bottom + yrange * 0.8:
            print_height = height - yrange * 0.06
        else:
            print_height = height + yrange * 0.03
        ax.text(bar.get_x() + bar.get_width()/2., print_height,
                ('%.1f%%' % height) if plot_type in (PlotType.percent_of_total, PlotType.percent) else ("%4.2fx" % height),
                ha='center', va='bottom')

    plt.xticks(y_pos, labels_perc)
    plt.xlabel("User Segment (Best to Worst)")
    # plt.ylabel(y_axis_label)
    if plot_type == PlotType.odds_ratio:
        plt.ylabel("Purchase odds vs average user")
    elif plot_type == PlotType.percent_of_total:
        plt.ylabel("Percent of total positive samples")
    else:
        plt.ylabel("Percent positive in segment")

    if title:
        plt.title(title)
    plt.savefig(filename, dpi=300)
    return sums


def plot_auc(filename, results, results2=None, results3=None, x_label=None, y_label=None,
             labels=None):
    plt.clf()
    total_pos = create_total_pos(results)
    length = len(total_pos)
    if results2 != None:
        total_pos2 = create_total_pos(results2)
    if results3 != None:
        total_pos3 = create_total_pos(results3)

    if x_label == None and y_label == None:
        plt.subplots_adjust(left=0.05, right=0.98, top=0.97, bottom=0.08, wspace=0.0, hspace=0.0)
    else:
        plt.subplots_adjust(left=0.08, right=0.98, top=0.97, bottom=0.09, wspace=0.0, hspace=0.0)

    xticks = numpy.arange(length + 0.001, step=length / 10.0)
    plt.xticks(xticks)
    plt.yticks(numpy.arange(0, 1, step=0.1))
    ax = plt.gca()
    ax.set_autoscale_on(False)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: "%3.1f" % (float(x) / length)))
    plt.grid(b=True, which='major', axis='y', color='0.3', linestyle='-', alpha=0.3, linewidth=0.3)
    plt.grid(b=True, which='major', axis='x', color='0.3', linestyle='-', alpha=0.3, linewidth=0.3)
    plt.plot([0, length - 1], [0, 1], "r-", linewidth=0.2, antialiased=True)

    if y_label:
        ax.set_ylabel(y_label)

    if x_label:
        ax.set_xlabel(x_label)

    plt.plot(total_pos, "b-", linewidth=0.5, antialiased=True, label=labels[0] if labels else None)
    if results2 != None:
        plot_x = numpy.arange(0, length, length / float(len(total_pos2)))
        plt.plot(plot_x, total_pos2, "g-", linewidth=0.5, antialiased=True, label=labels[1] if labels else None)
    if results3 != None:
        plot_x = numpy.arange(0, length, length / float(len(total_pos3)))
        plt.plot(plot_x, total_pos3, "k-", linewidth=0.5, antialiased=True, label=labels[2] if labels else None)

    if labels:
        plt.legend(loc='upper left')
    plt.savefig(filename, dpi=300)
