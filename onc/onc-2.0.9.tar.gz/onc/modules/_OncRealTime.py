from ._OncService import _OncService

class _OncRealTime(_OncService):
    """
    Near real-time services methods
    """

    def __init__(self, config: dict):
        super().__init__(config)
    

    def getDirectScalar(self, filters: dict, allPages: bool):
        '''
        Method to return scalar data from the scalardata service in JSON Object format
        which match filter criteria defined by a dictionary of filters.
        see https://wiki.oceannetworks.ca/display/help/scalardata+service for usage and available filters
        '''
        return self._getDirectAllPages(filters, 'scalardata', 'getByLocation', allPages)


    def getDirectRawByLocation(self, filters: dict, allPages: bool):
        '''
        Method to return raw data from an instrument, in the payload, in JSON format from the rawdata service 
        which match filter criteria defined by a dictionary of filters
        see https://wiki.oceannetworks.ca/display/help/rawdata+service for usage and available filters
        '''
        return self._getDirectAllPages(filters, 'rawdata', 'getByLocation', allPages)


    def getDirectRawByDevice(self, filters: dict, allPages: bool):
        '''
        Method to return raw data from an instrument, in the payload, in JSON format from the rawdata service 
        which match filter criteria defined by a dictionary of filters
        see https://wiki.oceannetworks.ca/display/help/rawdata+service for usage and available filters
        '''
        return self._getDirectAllPages(filters, 'rawdata', 'getByDevice', allPages)


    def _getDirectAllPages(self, filters: dict, service: str, method: str, allPages: bool):
        '''
        Keeps downloading all scalar or raw data pages until finished
        Automatically translates sensorCategoryCodes to a string if a list is provided
        Return the full stitched data
        '''
        # prepare filters for first page request
        filters = filters or {}
        url = self._serviceUrl(service)
        filters['method'] = method
        filters['token'] = self.token
        dataKey = 'sensorData' if service == 'scalardata' else 'data'

        # if sensorCategoryCodes is an array, join it into a comma-separated string
        if 'sensorCategoryCodes' in filters and isinstance(filters['sensorCategoryCodes'], list):
            filters['sensorCategoryCodes'] = ",".join(filters['sensorCategoryCodes'])

        try:
            response = self._doRequest(url, filters)
            if response[dataKey] != None:
                nextReq = response['next']

                # Grab the next pages if needed
                while allPages and nextReq != None:
                    nextResponse = self._doRequest(url, nextReq['parameters'])
                    
                    # stitch next page into full response, with the right format
                    if service == 'scalardata':
                        for i in range(len(response['sensorData'])):
                            sensorData = response['sensorData'][i]
                            sensorCode = sensorData['sensorCode']
                            for nextSensor in nextResponse['sensorData']:
                                if nextSensor['sensorCode'] == sensorCode:
                                    sensorData['data']['qaqcFlags']   += nextSensor['data']['qaqcFlags']
                                    sensorData['data']['sampleTimes'] += nextSensor['data']['sampleTimes']
                                    sensorData['data']['values']      += nextSensor['data']['values']
                    
                    elif service == 'rawdata':
                        response['data']['lineTypes'] += nextResponse['data']['lineTypes']
                        response['data']['readings']  += nextResponse['data']['readings']
                        response['data']['times']     += nextResponse['data']['times']
                    
                    nextReq = nextResponse['next']
                response['next'] = None

            return response
        except Exception: raise