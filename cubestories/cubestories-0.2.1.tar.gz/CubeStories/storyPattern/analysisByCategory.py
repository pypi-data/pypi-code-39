from .storyPattern import storyPattern
from ..cubeParameters import cubeParameters

class analysisByCategory(storyPattern):

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
                            dim_for_category=self.params["dim_for_category"],
                            meas_to_analyse=self.params["meas_to_analyse"],
                            analysis_type=self.params["analysis_type"])
           
            #print(self.data)
            #print(self.params)
            self.datastories=patternAnalysis.datastories
            return self