#! /usr/bin/env python3

import json
import logging
from operator import itemgetter
from sys import argv

script, distances_json = argv

LOG = 'toolbox.log'

def read_distances_dict(distances_json):
    with open(distances_json, 'r') as fp:
        logging.info('Reading distances from file {} ...\n'.format(distances_json))

        mean_taxon_distances = json.load(fp)
        return mean_taxon_distances

level = logging.INFO
log_format = '%(asctime)s - %(message)s'
handlers = [logging.FileHandler(LOG, 'w'), logging.StreamHandler()]
logging.basicConfig(level=level, format=log_format, handlers=handlers)

'''
The distances dict has structure:

{"species": [
            [window_no1, distance],
            [window_no2, distance],
            ...
            ]}
'''

def get_outliers_list(window_dist_list, cutoff):
    #sorted_dist_list = sorted(window_dist_list, key=itemgetter(1), reverse=True)
    return [window for window in window_dist_list if window[1] >= cutoff]


def sort_dist_list(window_dist_list, no_top_windows):
    return sorted(window_dist_list, key=itemgetter(1), reverse=True)[0:no_top_windows]


def get_taxon_top_dists(distances_dict, taxon, no_top_windows):
    return sort_dist_list(distances_dict[taxon], no_top_windows)

distances_dict = read_distances_dict(distances_json)

for taxon in sorted(distances_dict.keys()):
    print(taxon)
    print(get_taxon_top_dists(distances_dict, taxon, 5))
    #get_outliers_list(distances_dict[taxon], 0.0005)

# alternative to manual cutoffs: find break points in window distances
# plot histogram(?) of window distances sorted from highest to see if slope changes

# can you find outliers more efficiently without re-starting every time from scratch?

# can you find optimal mean that removes, say exactly 1% of the sequence data?
# perhaps sort the windows first by distances, then find a mean that would result in discarding 1%? 

# to avoid iterating over the entire list while searching for outliers, perhaps loop over first using the largest cutoff, then smaller etc.

#####################

# print n top distance windows for taxon x
# print n top distance windows across all taxa # also cutoff on min number of taxa
# print    