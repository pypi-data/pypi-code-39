import numpy as np
from numba import jit, njit, int32, int64
from numba.types import boolean


'''-----------------------------------------------------------------------------
FOR LABELING
-----------------------------------------------------------------------------'''
# @njit(boolean(int64, int64, int64, int64))
@njit(cache=True)
def keep_q(start_a, stop_a, start_b, stop_b):
    '''
    Determines whether or not to keep the second range for labeling the first
    i.e. whether or not the range indicated by [start_b, stop_b] overlaps with
    the range designated by [start_a, stop_a]

    Notes:
        assumes start < stop

    Arguments:
        start_a (int): start of range to test against
        stop_a (int): stop of range to test against
        start_b (int): start of range in question
        stop_b (int): stop of range in question

    Returns:
        (bool): whether or not the second range overlaps the first
    '''
    if stop_b < start_a: return False
    if start_b > stop_a: return False
    return True

# @njit(int64[:,:](int64, int64, int64[:,:]))
@njit(cache=True)
def relevant_labels(start, stop, reference_ranges):
    '''
    Filter a set of reference ranges for those relevant to the range spaned by
    `[start, stop]`

    Arguments:
        start (int): start of range to test against
        stop (int): stop of range to test against
        reference_ranges (np.array): an integer array of shape (-1, 3)
            indicating the type of range as well as its start and stop

    Returns:
        relevant_ranges (np.array): an integer array of shape (-1, 3)
            indicating the type of range as well as its start and stop that all
            overlap with the passed arguments start and stop
    '''
    results = np.array([0][:0]).reshape(-1, 3)
    for i in prange(len(reference_ranges)):
        _type, start_b, stop_b = reference_ranges[i]
        if keep_q(start, stop, start_b, stop_b):
            results = np.concatenate(
                (results, np.array([[_type, start_b, stop_b]]))
            )
    return results


# @njit(int64[:,:](int64, int64, int64[:, :], int64))
@njit(cache=True)
def _label_range(start, stop, reference_ranges, number_of_range_types):
    '''
    Encodes the range into a hot-encoding

    Arguments:
        start (int): start of range to test against
        stop (int): stop of range to test against
        reference_ranges (np.array): an integer array of shape (-1, 3)
            indicating the type of range as well as its start and stop
        number_of_range_types (int): how many channels the encoding should have

    Returns:
        encoding (np.array): an integer array of shape
            `(stop-start, number_of_range_types)` indicating the type of range
            at index `i` is relevant to the range indicated by `[start, stop]`
            based on `reference_ranges`
    '''
    range_length = stop - start
    encoding = np.zeros((range_length, number_of_range_types), dtype=np.int64)
    boundaries = reference_ranges[:,1:].T

    for i in range(range_length):
        _i = i + start
        # ranges_to_apply = np.all([
        #     reference_ranges[:, 1] <= _i,
        #     reference_ranges[:, 2] >= _i
        # ], axis=0)
        # logical_test = np.array([boundaries[0,:] <= _i, boundaries[1,:] >= _i])
        logical_test = np.concatenate((
            (boundaries[0,:] <= _i).reshape(-1, boundaries.shape[-1]),
            (boundaries[1,:] >= _i).reshape(-1, boundaries.shape[-1])
        )).T

        ranges_to_apply = np.array([np.all(logical_test[j]) for j in range(len(logical_test))])
        indices = np.unique(reference_ranges[ranges_to_apply][:, 0])
        for j in indices:
            encoding[i, j] = 1
        # encoding[i, reference_ranges[ranges_to_apply][:, 0]] = 1
    return encoding

@jit(forceobj=True, cache=True)
def label_range(start, stop, reference_ranges, labels_order):
    # ensure np as input
    np_labels = np.array(labels_order)
    np_ranges = np.array(reference_ranges)
    # convert string labels to integers
    np_ranges = _ranges_np_to_nb(np_ranges, np_labels)
    return _label_range(start, stop, np_ranges, len(labels_order))


'''-----------------------------------------------------------------------------
FOR COALESCE
-----------------------------------------------------------------------------'''
@jit(forceobj=True, cache=True)
def label_to_index(label, labels_order):
    return np.where(labels_order == label)[0][0]

def labels_to_indices(labels, labels_order):
    f = lambda label: label_to_index(label, labels_order)
    return np.array(list(map(f, labels)))

@jit(forceobj=True, cache=True)
def index_to_label(index, labels_order):
    return labels_order[index]

def indices_to_labels(indices, labels_order):
    f = lambda index : index_to_label(index, labels_order)
    return np.array(list(map(f, indices)))

@jit(forceobj=True, cache=True)
def _ranges_np_to_py(ranges):
    return [[type, int(start), int(stop)] for type, start, stop in ranges]

@jit(forceobj=True, cache=True)
def _ranges_np_to_nb(np_ranges, np_labels_order):
    if np_labels_order.size > 0:
        np_ranges[:, 0] = labels_to_indices(np_ranges[:, 0], np_labels_order)
    return np.array(np_ranges, dtype=np.int64)

@jit(forceobj=True, cache=True)
def _ranges_nb_to_np(np_ranges, np_labels_order):
    if np_labels_order.size > 0:
        np_labels = indices_to_labels(np_ranges[:, 0], np_labels_order).reshape((-1, 1))
        np_ranges = np.append(np_labels, np_ranges[:, 1:], axis=1)
    return np_ranges

@njit(cache=True)
def merge_q(label_a, start_a, stop_a, label_b, start_b, stop_b):
    if label_a != label_b: # not of same type
        return False
    elif stop_a < start_b: # a does not start and then overlap b
        return False
    elif stop_b < start_a: # b does not start and then overlap a
        return False
    else: # same type and overlap, merge into i, do not append
        return True

@njit(cache=True)
def _coalesce(ranges):
    coalesced = np.array([0][:0]).reshape(-1, 3)
    for i in range(len(ranges)):
        label_a, start_a, stop_a = ranges[i]
        append_flag = True
        for j in range(len(coalesced)):
            label_b, start_b, stop_b = coalesced[j]
            if merge_q(label_a, start_a, stop_a, label_b, start_b, stop_b):
                append_flag = False
                coalesced[j] = [label_a, min(start_a, start_b), max(stop_a, stop_b)]
                break
        if append_flag:
            coalesced = np.concatenate((coalesced, np.array([[label_a, start_a, stop_a]])))
    return coalesced

@jit(forceobj=True, cache=True)
def coalesce(ranges, labels_order=[]):
    '''
    A python wrapper for taking LabeledRanges (as list) and sending it to numba
    to simplify.

    Arguments:
        ranges (list): a list of ranges, where each range is a list of length
            3 consisting of:
                label (int / str)
                start (int)
                stop (int)
        labels_order (list): if the labels of ranges are as strings, then
            labels_order corresponds to a list, containing each label to be used
            as a lookup table for converting them to indicies.

    Returns:
        ranges (list): a simplified version of the input
    '''
    # ensure np as input
    np_labels = np.array(labels_order)
    np_ranges = np.array(ranges)
    # convert string labels to integers
    np_ranges = _ranges_np_to_nb(np_ranges, np_labels)
    np_result = _coalesce(np_ranges)
    # invert labels to strings
    np_result = _ranges_nb_to_np(np_result, np_labels)
    return _ranges_np_to_py(np_result)
