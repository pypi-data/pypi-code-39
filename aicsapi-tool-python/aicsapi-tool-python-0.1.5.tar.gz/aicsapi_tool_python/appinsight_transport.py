from applicationinsights import TelemetryClient
from applicationinsights.flask.ext import AppInsights

class AppinsightLogger(object):
    '''
    Used for logging to Azure AppInsights
    '''

    def __init__(self, app, appins_key):
        '''
        Creates AppInsightLogger instance

        Parameters
        ----------
        app : obj
            Flask instance
        appins_key : str
            Instrumentation key for Azure AppInsights subscription

        Returns
        -------
        obj
            AppInsightLogger instance
        '''

        # for customEvent logging
        self.tc = TelemetryClient( appins_key )
        self.tc.channel.sender.send_interval_in_milliseconds = 10 * 1000
        self.tc.channel.queue.max_queue_length = 10
        
        # automatically logs request, traces, and failures 
        self.appinsights = AppInsights(app)

    def send_custEvent(self, name, dim=None, measure=None):
        '''
        Logs to customEvent on Azure AppInsights

        Parameters
        ----------
        name : str
            name of customEvent
        dim : dict
            customDimensions of customEvent
        measure : dict
            customMeasurements of customEvent
        '''
        
        if dim and measure:
            self.tc.track_event(name, dim, measure)
        elif dim and not measure:
            self.tc.track_event(name, dim)
        elif not dim and measure:
            self.tc.track_event(name, None, measure)
        else:
            self.tc.track_event(name)