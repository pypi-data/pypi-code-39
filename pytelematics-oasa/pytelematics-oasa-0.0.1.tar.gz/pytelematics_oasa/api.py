from .exception import OasaTelematicsError
import requests

class OasaTelematics(object):

    def get(self, action, *params):
        """
        Make a GET Request to the api and returns the data. \n
        Go to the documentation page 
        (https://oasa-telematics-api.readthedocs.io/en/latest/index.html) for more details
        """

        api = "http://telematics.oasa.gr/api/"
        query = {'act': action}

        for i, param in enumerate(params, 1):
            query.update({f'p{i}': param})

        response = requests.get(api, query)
        return response.json()

    def get_all_lines(self):
        """
        Returns data on all bus lines.
        """

        return self.get('webGetLines')

    def closest_stops(self, x, y):
        """
        Returns the nearest stops \n
        Params:
            x: Latitude
            y: Longitude
        """

        return self.get('getClosestStops', x, y)

    def linecodes(self, lineID):
        """
        Returns the linecodes of its lineID
        """

        linecodes = []
        lines = self.get('webGetLines')

        for line in lines:
            if line['LineID'] == lineID :
                linecodes.append(line['LineCode'])

        if not linecodes:
            raise OasaTelematicsError(f'{lineID} is not a valid line ID or does not exists.')
        
        return linecodes

class Line(OasaTelematics):

    def __init__(self, linecode):
        super(Line, self).__init__()

        res = self.get('webGetLines')
        for item in res:
            if item['LineCode'] == linecode:
                self.linecode = linecode
                self.ID = item['LineID']
                self.name = item['LineDescr']
                self.name_en = item['LineDescrEng']

        try:
            self.ID
        except AttributeError:
            raise OasaTelematicsError("Invalid Linecode or does not exists.")

    def routes(self, cls=False):
        """
        Returns the routes of a line. \n
        Params: \n
            cls: True  => Returns data as Route instance. \n
                 False => Returns data normally.
        """

        res = self.get('webGetRoutes', self.linecode)
        if cls is True:
            routes = [Route(item['RouteCode']) for item in res]
        else:
            routes = [item for item in res]

        return routes

    def schedule_days(self):
        """
        Returns the info for which program / schedule the line follows.
        """

        return self.get('getScheduleDaysMasterline', self.linecode)

class Route(OasaTelematics):

    def __init__(self, routecode):
        super(Route, self).__init__()

        routename = self.get('getRouteName', routecode)
        if routename is not None:
            self.routecode = routecode
            self.name = routename[0]['route_descr']
            self.name_en = routename[0]['route_departure_eng']
        else:
            raise OasaTelematicsError('Invalid Routecode or does not exists.')

    def bus_location(self):
        """
        Returns the location of buses on a particular route.
        """

        return self.get('getBusLocation', self.routecode)

    def details(self):
        """
        Returns the details of the route, 
        ie the location of the stops and the order in which the bus is 'visited'.
        """

        return self.get('webRouteDetails', self.routecode)

    def stops(self):
        """
        Returns the stops of a route.
        """

        res = self.get('webGetStops', self.routecode)
        stops = [item for item in res]

        return stops

class Stop(OasaTelematics):

    def __init__(self, stopcode):
        super(Stop, self).__init__()

        info = self.get('getStopNameAndXY', stopcode)
        if info is not None:
            self.stopcode = stopcode
            self.name = info[0]['stop_descr']
            self.name_en = info[0]['stop_descr_matrix_eng']
            self.lat = info[0]['stop_lat']
            self.lng = info[0]['stop_lng']
        else:
            raise OasaTelematicsError('Invalid Stopcode or does not exists.')

    def arrivals(self):
        return self.get('getStopArrivals', self.stopcode)



