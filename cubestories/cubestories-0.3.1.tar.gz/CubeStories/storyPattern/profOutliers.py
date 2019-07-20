from .storyPattern import storyPattern
from ..cubeParameters import cubeParameters

class profOutliers(storyPattern):

    
    def __radd__(self,patternAnalysis):
        if isinstance(patternAnalysis,storyPattern) or isinstance(patternAnalysis,cubeParameters):
            self.cube=patternAnalysis.cube
            self.dimensions=patternAnalysis.dimensions
            self.measures=patternAnalysis.measures
            self.hierdimensions=patternAnalysis.hierdimensions
            data=patternAnalysis.datastories
            self.data=data.ProfileOutliers(cube=patternAnalysis.cube,
                            dims=patternAnalysis.dimensions,
                            meas=patternAnalysis.measures,
                            hierdims=patternAnalysis.hierdimensions,
                            df=patternAnalysis.data,
                            display_type=self.params["display_type"])
            
            #print(self.data)
            #print(self.params)
            self.datastories=patternAnalysis.datastories
            return self