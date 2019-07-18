import pandas as pd

class cubeParameters(object):

    def __init__(self,cube="",dimensions=[],measures=[],hierdimensions=[]):
        self.data=pd.DataFrame()
        self.datastories=None
        self.cube=cube
        self.dimensions=dimensions
        self.hierdimensions=hierdimensions
        self.measures=measures
        
    def __radd__(self, cubestory):
        try:
            self.datastories=cubestory.datastories
            return self
        except:
            raise Exception("Metadata/DataEndpoint not provided")


