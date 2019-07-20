from .storyPattern import storyPattern
from ..cubeParameters import cubeParameters

class narrChangeOT(storyPattern):

    def __radd__(self,patternAnalysis):
        if isinstance(patternAnalysis,storyPattern) or isinstance(patternAnalysis,cubeParameters):
            self.cube=patternAnalysis.cube
            self.dimensions=patternAnalysis.dimensions
            self.measures=patternAnalysis.measures
            self.hierdimensions=patternAnalysis.hierdimensions
            data=patternAnalysis.datastories
            self.data=data.narrChangeOT(cube=patternAnalysis.cube,
                            dims=patternAnalysis.dimensions,
                            meas=patternAnalysis.measures,
                            hierdims=patternAnalysis.hierdimensions,
                            df=patternAnalysis.data,
                            meas_to_narrate=self.params["meas_to_narrate"],
                            narr_type=self.params["narr_type"])
           
            #print(self.data)
            #print(self.params)
            self.datastories=patternAnalysis.datastories
            return self