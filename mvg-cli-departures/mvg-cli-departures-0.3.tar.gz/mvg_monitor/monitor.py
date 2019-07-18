#!/usr/bin/env python3

import argparse
import json
import mvg_api


class Request:
    """Describing a request and providing methods to answer one.

    :param station: either name or id of the departure station
    :param product: either UBAHN, BUS, SBAHN or TRAM; default UBAHN
    :param n_connections: number of possible connections/departures to query; default 1
    """

    def __init__(self, station: str, product: str = 'UBAHN', n_connections: int = 1):
        self.station = station
        self.transport = product
        self.num_connections = n_connections

    @property
    def station(self):
        return self.__station_id

    # TODO: catch possible err when cant identify station
    # TODO: print feedback which station was taken
    @station.setter
    def station(self, station):
        """Set the station id and looks it up if it's not a number. """
        if isinstance(station, int):
            self.__station_id = station
        else:
            self.__station_id = mvg_api.get_id_for_station(station)

    @property
    def transport(self):
        return self.__transport

    @transport.setter
    def transport(self, transport):
        """Sets the means of transport; checks if correct one way selected. """
        supported_means_of_transport = ['UBAHN', 'TRAM', 'BUS', 'SBAHN']
        if transport in supported_means_of_transport:
            self.__transport = transport
        else:
            raise ValueError('{} is not supported; '
                             'check: {}'.format(transport, supported_means_of_transport))

    @property
    def num_connections(self):
        return self.__num_connections

    @num_connections.setter
    def num_connections(self, connections):
        """Sets num_connections to query if connections is greater than 0. """
        if connections > 0:
            self.__num_connections = connections
        else:
            raise ValueError('Number connections queried must be greater than 0;'
                             ' is {}'.format(connections))

    @staticmethod
    def extract_quick_departure(single_departure):
        """Extracting relevant information to display for a quick departure request.

        :param single_departure: dict of a single departure returned by mvg_api.get_departures()
        :return: condensed information; including product, line, destination and minutes left
        """
        ret = {'product': single_departure['product'],
               'line': single_departure['label'],
               'dest': single_departure['destination'],
               'min_left': single_departure['departureTimeMinutes']}
        return ret

    def departures(self, condense_fun):
        """Querying the next num_connections departures for given station.

        :param condense_fun: callable condensing retrieved function
        :return: list of upcoming departures
        """
        # returns a list of dicts holding the departure information
        departures = mvg_api.get_departures(self.station)

        results = []
        for dep in departures:
            if self.transport in dep['product']:
                # get next departure in minutes
                results.append(condense_fun(dep))

            if len(results) == self.num_connections:
                break

        if len(results) == 0:
            results.append('!! NO CONNECTIONS FOUND FOR REQUEST !!')

        return results

    def next_departures(self):
        """Querying and displaying next departures. """

        # list of upcoming departures
        departures = self.departures(self.extract_quick_departure)

        # beginning of print out
        print('\n' * 4)
        print('#' * 80)

        if isinstance(departures[0], str):
            print('#' * 80)
            print(departures[0])
        else:
            # formatting
            header = 'departures for {} from {} '.format(departures[0]['product'],
                                                         mvg_api.get_stations(self.station)[0]['name'])
            print('{} {}'.format(header, '#' * (79-len(header))))  # keep header line at 80 col
            print()

            # printing departures
            for i, dep in enumerate(departures):
                print('LINE:\t {}'.format(dep['line']))
                print('TO:\t {}'.format(dep['dest']))
                print('IN:\t {} min.'.format(dep['min_left']))
                print()  # empty line for better reading

        # ending of print out
        print('#' * 80)
        print('#' * 80)
        print()
