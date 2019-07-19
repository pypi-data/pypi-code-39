from .storyPattern import storyPattern
from ..cubeParameters import cubeParameters

class extComparison(storyPattern):

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
                            dims_to_compare=self.params["dims_to_compare"],
                            comp_type=self.params["comp_type"],
                            meas_to_compare=self.params["meas_to_compare"])
           
            #print(self.data)
            #print(self.params)
            self.datastories=patternAnalysis.datastories
            return self