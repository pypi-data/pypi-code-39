import weakref

# Handles data multi-page downloads (scalardata, rawdata, archivefiles)
class _MultiPage:
    def __init__(self, parent: object):
        self.parent = weakref.ref(parent)
        self.result = None
    

    def getAllPages(self, service, url, filters):
        try:
            response = self.parent()._doRequest(url, filters)
            nextReq = response['next']

            while nextReq != None:
                nextResponse = self.parent()._doRequest(url, nextReq['parameters'])
                    
                # stitch next page into full response, with the right format
                if service == 'scalardata':
                    keys = response['sensorData'][0]['data'].keys()
                    for sensorData in response['sensorData']:
                        sensorCode = sensorData['sensorCode']
                        for nextSensor in nextResponse['sensorData']:
                            if nextSensor['sensorCode'] == sensorCode:
                                for key in keys:
                                    sensorData['data'][key] += nextSensor['data'][key]
                
                elif service == 'rawdata':
                    for key in response['data']:
                        response['data'][key] += nextResponse['data'][key]
                
                nextReq = nextResponse['next']
            response['next'] = None

            return response
        except Exception: raise
    
