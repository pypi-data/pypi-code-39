#!/usr/bin/env python
"""Utilities for dealing with client fleet data."""
from __future__ import absolute_import
from __future__ import division

from __future__ import unicode_literals

import collections

from future.builtins import int
from future.utils import iteritems
from future.utils import iterkeys
from future.utils import itervalues
from typing import Any, DefaultDict, Dict, List, Optional, Set, Text, Tuple


def _DictFromDefaultDict(input_dict):
  output_dict = {}
  for k, v in iteritems(input_dict):
    if isinstance(v, collections.defaultdict):
      output_dict[k] = _DictFromDefaultDict(v)
    else:
      output_dict[k] = v
  return output_dict


def _ValidateBucket(day_bucket, day_buckets):
  if day_bucket not in day_buckets:
    raise ValueError("Invalid bucket '%d'. Allowed buckets are %s." %
                     (day_bucket, sorted(day_buckets)))


class FleetStats(object):
  """Encapsulates client activity statistics.

  A FleetStats object contains fleet-wide n-day-active data for multiple days,
  client-labels and statistic category values. An example of a
  statistic category is 'GRR version', for which we could have values
  such as 'GRR windows amd64 3214'. Another example of a category is
  'Platform', for which we could have the values 'Linux' or 'Windows'.
  Every FleetStats object contains data for one, and only one category.
  """

  def __init__(self, day_buckets,
               label_counts,
               total_counts):
    """Initializes a FleetStats object.

    Args:
      day_buckets: A set of n-day-active buckets for which the encapsulated
        stats were computed.
      label_counts: A dict structure containing n-day-active data for multiple
        days, client-labels and statistic category values. Notably,
        'label_counts' is expected to only have data for clients with GRR
        labels.
      total_counts: A dict structure containing n-day-active totals for all
        clients - regardless of label - across multiple category values.
    """
    self._day_buckets = day_buckets
    self._label_counts = label_counts
    self._total_counts = total_counts
    all_labels = set()
    for day_bucket in self._label_counts:
      all_labels.update(iterkeys(self._label_counts[day_bucket]))
    self._all_labels = sorted(all_labels)

  def GetAllLabels(self):
    """Returns all client labels represented in the underlying data."""
    return list(self._all_labels)

  def GetDayBuckets(self):
    """"Returns the n-day-active buckets for the underlying data (sorted)."""
    return sorted(self._day_buckets)

  def GetValuesForDayAndLabel(self, day_bucket,
                              client_label):
    """Returns activity counts for a particular bucket and client label.

    Each entry in the returned dict maps a category value to the total number
    of clients for that category value that were active in
    the last 'day_bucket' days, and had the given client label. An empty dict
    is returned if no clients with the given label were active in the given
    time window.

    Args:
      day_bucket: n-day-active bucket for the data to return.
      client_label: Client label for which to return data.
    """
    _ValidateBucket(day_bucket, self._day_buckets)
    try:
      return dict(self._label_counts[day_bucket][client_label])
    except KeyError:
      return {}

  def GetTotalsForDay(self, day_bucket):
    """Returns totals for a particular bucket (across all client-labels).

    Each entry in the returned dict maps a category value to the total number
    of clients for that category value that were active in
    the last 'day_bucket' days. An empty dict is returned if no clients were
    active in the given time window.

    Args:
      day_bucket: n-day-active bucket for the data to return.
    """
    _ValidateBucket(day_bucket, self._day_buckets)
    try:
      return dict(self._total_counts[day_bucket])
    except KeyError:
      return {}

  def GetFlattenedLabelCounts(self):
    """Returns a flat representation of the encapsulated label-specific data.

    This method is mostly intended to make testing easier.
    """
    flattened_counts = {}
    for day_bucket, label_dict in iteritems(self._label_counts):
      for client_label, category_value_dict in iteritems(label_dict):
        for category_value, num_actives in iteritems(category_value_dict):
          flattened_counts[(day_bucket, client_label,
                            category_value)] = num_actives
    return flattened_counts

  def GetFlattenedTotalCounts(self):
    """Returns a flat representation of the encapsulated label-free totals.

    This method is mostly intended to make testing easier.
    """
    flattened_counts = {}
    for day_bucket, category_value_dict in iteritems(self._total_counts):
      for category_value, num_actives in iteritems(category_value_dict):
        flattened_counts[(day_bucket, category_value)] = num_actives
    return flattened_counts

  def GetAggregatedLabelCounts(self):
    """Sums up the total number of n-day-actives by label and day-bucket.

    Returns:
      A dict, where each entry maps a client label in the encapsulated data
      to a dict that maps n-day-active buckets to the total number of clients
      with said client-label that were active within said bucket.
    """
    # Pyformat reformats this defaultdict initialization in a manner that
    # breaks the linter (g-long-lambda).
    # pyformat: disable
    aggregated_counts = collections.defaultdict(
        lambda: collections.defaultdict(int))
    # pyformat: enable
    for day_bucket in self._day_buckets:
      for client_label in self.GetAllLabels():
        day_label_sum = 0
        for num_actives in itervalues(
            self.GetValuesForDayAndLabel(day_bucket, client_label)):
          day_label_sum += num_actives
        aggregated_counts[client_label][day_bucket] = day_label_sum
    return _DictFromDefaultDict(aggregated_counts)

  def GetAggregatedTotalCounts(self):
    """Sums up the total number of n-day-actives by day-bucket.

    Returns:
      A dict, where each entry maps an n-day-active bucket to the total
      number of clients that were active within said bucket.
    """
    aggregated_counts = collections.defaultdict(int)
    for day_bucket in self._day_buckets:
      day_sum = 0
      for num_actives in itervalues(self.GetTotalsForDay(day_bucket)):
        day_sum += num_actives
      aggregated_counts[day_bucket] = day_sum
    return _DictFromDefaultDict(aggregated_counts)

  def Validate(self):
    """Sanity-checks the encapsulated stats.

    For every label, the function mapping day-buckets to number of clients seen
    should be non-decreasing. E.g. it does not make sense for there to be
    fewer 7-day-active clients than 1-day-active clients. The same reasoning
    applies to the label-free totals.

    Raises:
      ValueError: If the underlying data fails sanity checks.
    """
    aggregated_label_counts = self.GetAggregatedLabelCounts()
    for client_label, day_bucket_dict in iteritems(aggregated_label_counts):
      sorted_counts_by_day = sorted(iteritems(day_bucket_dict))
      prev_count = 0
      for _, count in sorted_counts_by_day:
        if count < prev_count:
          raise ValueError("Day-bucket counts for label %s are invalid: %s." %
                           (client_label, sorted_counts_by_day))
        prev_count = count

    sorted_counts_by_day = sorted(iteritems(self.GetAggregatedTotalCounts()))
    prev_count = 0
    for _, count in sorted_counts_by_day:
      if count < prev_count:
        raise ValueError(
            "Day-bucket counts for fleet-wide totals are invalid: %s." %
            (sorted_counts_by_day,))
      prev_count = count


class FleetStatsBuilder(object):
  """An object used to incrementally build FleetStats objects."""

  def __init__(self, day_buckets):
    """Initializes a FleetStatsBuilder object.

    Args:
      day_buckets: A set of n-day-active buckets for the fleet statistics.
    """
    self._day_buckets = day_buckets
    # Pyformat reformats these defaultdict initializations in a manner that
    # breaks the linter (g-long-lambda).
    # pyformat: disable
    self._label_counts = collections.defaultdict(
        lambda: collections.defaultdict(lambda: collections.defaultdict(int)))
    self._total_counts = collections.defaultdict(
        lambda: collections.defaultdict(int))
    # pyformat: enable

  def IncrementLabel(self,
                     client_label,
                     category_value,
                     day_bucket,
                     delta = 1):
    category_value = "" if category_value is None else category_value
    _ValidateBucket(day_bucket, self._day_buckets)
    self._label_counts[day_bucket][client_label][category_value] += delta

  def IncrementTotal(self,
                     category_value,
                     day_bucket,
                     delta = 1):
    category_value = "" if category_value is None else category_value
    _ValidateBucket(day_bucket, self._day_buckets)
    self._total_counts[day_bucket][category_value] += delta

  def Build(self):
    fleet_stats = FleetStats(self._day_buckets,
                             _DictFromDefaultDict(self._label_counts),
                             _DictFromDefaultDict(self._total_counts))
    fleet_stats.Validate()
    return fleet_stats
