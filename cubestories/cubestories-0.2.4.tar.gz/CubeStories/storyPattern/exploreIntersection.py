from .storyPattern import storyPattern
from ..cubeParameters import cubeParameters
import pandas as pd

class exploreIntersection(storyPattern):
    def __radd__(self,patternAnalysis):
        if isinstance(patternAnalysis,storyPattern) or isinstance(patternAnalysis,cubeParameters):
            self.cube=patternAnalysis.cube
            self.dimensions=patternAnalysis.dimensions
            self.measures=patternAnalysis.measures
            self.hierdimensions=patternAnalysis.hierdimensions
            data=patternAnalysis.datastories
            if isinstance(patternAnalysis.data,pd.DataFrame) and patternAnalysis.data.empty:
                self.data=data.exploreIntersection(analysis_type=self.params["dim_to_explore"])
            else:
                raise ValueError("Explore Intersection can be perfomed as initial pattern only")
           
            #print(self.data)
            #print(self.params)
            self.datastories=patternAnalysis.datastories
            return self