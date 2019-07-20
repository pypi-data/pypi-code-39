import pandas as pd

class cubeParameters(object):

    def __init__(self,**kwargs):
        self.data=pd.DataFrame()
        self.datastories=None
        self.cube=kwargs.get("cube")
        self.dimensions=kwargs.get("dimensions")
        self.hierdimensions=kwargs.get("hierdimensions")
        self.measures=kwargs.get("measures")
        
    def __radd__(self, cubestory):
        try:
            self.datastories=cubestory.datastories
            return self
        except:
            raise Exception("Metadata/DataEndpoint not provided")


