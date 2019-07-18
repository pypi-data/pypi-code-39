import pandas as pd

class storyPattern(object):

    def __init__(self,*args,**kwargs):
        self.datastories=None
        self.dimensions=None
        self.measures=None
        self.hierdimensions=None
        self.data=pd.DataFrame()
        self.cube=None
        self.params=kwargs