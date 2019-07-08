import pandas as pd
from virtualitics import vip_plot
from virtualitics import exceptions


class VipResult:
    """
    Chasis for any and all responses from VIP
    """
    def __init__(self, results):
        self.data = None
        self.plot = None
        for result in results:
            if isinstance(result, pd.DataFrame):
                self.data = result
            elif isinstance(result, vip_plot.VipPlot):
                self.plot = result
            else:
                raise exceptions.InvalidResultTypeException("VipResult's must be pd.DataFrame or VipPlot type.")
