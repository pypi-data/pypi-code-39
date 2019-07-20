from .storyPattern import storyPattern
from ..cubeParameters import cubeParameters
import pandas as pd

class startBigDrillDown(storyPattern):
    def __radd__(self,patternAnalysis):
        if isinstance(patternAnalysis,storyPattern) or isinstance(patternAnalysis,cubeParameters):
            self.cube=patternAnalysis.cube
            self.dimensions=patternAnalysis.dimensions
            self.measures=patternAnalysis.measures
            self.hierdimensions=patternAnalysis.hierdimensions
            data=patternAnalysis.datastories
            if isinstance(patternAnalysis.data,pd.DataFrame) and patternAnalysis.data.empty:
                self.data=data.StartBigDrillDown(cube=patternAnalysis.cube,
                                                dims=patternAnalysis.dimensions,
                                                meas=patternAnalysis.measures,
                                                hierdim_drill_down=self.params.get("hierdim_drill_down"))
            else:
                raise ValueError("Start Big Drill Down can be perfomed as initial pattern only")
           
            #print(self.data)
            #print(self.params)
            self.datastories=patternAnalysis.datastories
            return self