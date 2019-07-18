from .storyPattern import storyPattern
from ..cubeParameters import cubeParameters
class leagueTable(storyPattern):

    
    def __radd__(self,patternAnalysis):
        if isinstance(patternAnalysis,storyPattern) or isinstance(patternAnalysis,cubeParameters):
            self.cube=patternAnalysis.cube
            self.dimensions=patternAnalysis.dimensions
            self.measures=patternAnalysis.measures
            self.hierdimensions=patternAnalysis.hierdimensions
            data=patternAnalysis.datastories
            #if patternAnalysis.data is not None and isinstance(patternAnalysis.data, pd.DataFrame) :
        #data=datastories.DataStoryPattern(patternAnalysis.sparqlEndPointUrl,patternAnalysis.metaDataDict)
        #print(self.count_type+"\n\n\n\n\n")
            self.data=data.LTable(cube=patternAnalysis.cube,
                            dims=patternAnalysis.dimensions,
                            meas=patternAnalysis.measures,
                            hierdims=patternAnalysis.hierdimensions,
                            df=patternAnalysis.data,
                            columns_to_order=self.params["columns_to_order"],
                            order_type=self.params["order_type"],
                            number_of_records=self.params["number_of_records"])
            #print(self.params)

            self.datastories=patternAnalysis.datastories
            return self
