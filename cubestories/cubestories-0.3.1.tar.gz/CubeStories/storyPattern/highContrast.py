from .storyPattern import storyPattern
from ..cubeParameters import cubeParameters

class highContrast(storyPattern):
    def __radd__(self,patternAnalysis):
        if isinstance(patternAnalysis,storyPattern) or isinstance(patternAnalysis,cubeParameters):
            self.cube=patternAnalysis.cube
            self.dimensions=patternAnalysis.dimensions
            self.measures=patternAnalysis.measures
            self.hierdimensions=patternAnalysis.hierdimensions
            data=patternAnalysis.datastories
            self.data=data.AnalysisByCategory(cube=patternAnalysis.cube,
                            dims=patternAnalysis.dimensions,
                            meas=patternAnalysis.measures,
                            hierdims=patternAnalysis.hierdimensions,
                            df=patternAnalysis.data,
                            dim_to_contrast=self.params["dim_to_contrast"],
                            contrast_type=self.params["contrast_type"],
                            meas_to_contrast=self.params["meas_to_contrast"])
           
            #print(self.data)
            #print(self.params)
            self.datastories=patternAnalysis.datastories
            return self