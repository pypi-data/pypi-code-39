from .storypattern import storyPattern
from ..cubeParameters import cubeParameters


class measCount(storyPattern):

    def __radd__(self, patternAnalysis):
        #data=datastories.DataStoryPattern(patternAnalysis.sparqlEndPointUrl,patternAnalysis.metaDataDict)
        #print(self.count_type+"\n\n\n\n\n")
        if isinstance(patternAnalysis,storyPattern) or isinstance(patternAnalysis,cubeParameters):
            self.cube=patternAnalysis.cube
            self.dimensions=patternAnalysis.dimensions
            self.measures=patternAnalysis.measures
            self.hierdimensions=patternAnalysis.hierdimensions
            data=patternAnalysis.datastories
            print(patternAnalysis.data)
            self.data=data.MCounting(
                            df=patternAnalysis.data,
                            cube=patternAnalysis.cube,
                            dims=patternAnalysis.dimensions,
                            meas=patternAnalysis.measures,
                            hierdims=patternAnalysis.hierdimensions,
                            count_type=self.params["count_type"])
            
            print(self.data)
            #print(self.data.columns)
            #print(data.metaDataDict[patternAnalysis.cube])
            self.datastories=patternAnalysis.datastories
            return self
        else:
            raise Exception("Attempted non-pattern analysis")
