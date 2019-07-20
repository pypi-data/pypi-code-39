from ..storyPattern import *
from ..cubeParameters import cubeParameters
from ..metaData import metaData 
#from ..storyPattern import *


class storyTeller(object):

    def __init__(self, metadataparameters,cubeparameters,patternparameters):
        self.meta=metaData(**metadataparameters)
        self.cubeparams=cubeParameters(**cubeparameters)
        self.storytelling=None
        self.analysispipeline=patternparameters
        self.analysisResults=None
    

    def tellStory(self):
        analysisList=[]
        self.storytelling=self.meta+self.cubeparams
        try:
            for patanalysis in self.analysispipeline:
                if(patanalysis=="MeasCount"):
                    pattern=measCount(**self.analysispipeline[patanalysis])
                    analysisList.append([patanalysis,pattern])
                elif(patanalysis=="LeagueTab"):
                    pattern=leagueTable(**self.analysispipeline[patanalysis])
                    analysisList.append([patanalysis,pattern])
                elif(patanalysis=="DissFact"):
                    pattern=dissFactors(**self.analysispipeline[patanalysis])
                    analysisList.append([patanalysis,pattern])
                elif(patanalysis=="ExpInt"):
                    pattern=exploreIntersection(**self.analysispipeline[patanalysis])
                    analysisList.append([patanalysis,pattern])
                elif(patanalysis=="ExtComp"):
                    pattern=extComparison(**self.analysispipeline[patanalysis])
                    analysisList.append([patanalysis,pattern])
                elif(patanalysis=="HighCont"):
                    pattern=highContrast(**self.analysispipeline[patanalysis])
                    analysisList.append([patanalysis,pattern])
                elif(patanalysis=="IntComp"):
                    pattern=intComparison(**self.analysispipeline[patanalysis])
                    analysisList.append([patanalysis,pattern])
                elif(patanalysis=="ProfOut"):
                    pattern=profOutliers(**self.analysispipeline[patanalysis])
                    analysisList.append([patanalysis,pattern])
                elif(patanalysis=="StBigDrillDown"):
                    pattern=startBigDrillDown(**self.analysispipeline[patanalysis])
                    analysisList.append([patanalysis,pattern])
                elif(patanalysis=="StSmallZoomOut"):
                    pattern=startSmallZoomOut(**self.analysispipeline[patanalysis])
                    analysisList.append([patanalysis,pattern])
                elif(patanalysis=="NarrChangeOT"):
                    pattern=narrChangeOT(**self.analysispipeline[patanalysis])
                    analysisList.append([patanalysis,pattern])
                elif(patanalysis=="AByCategory"):
                    pattern=analysisByCategory(**self.analysispipeline[patanalysis])
                    analysisList.append([patanalysis,pattern])
                else:
                    raise ValueError("Wrong Type of Story Pattern Selected")
        
            for patternname,pattern in analysisList:
                self.storytelling+=pattern
                self.analysisResults+={patternname:self.storytelling.data}
        except Exception as e:
            print("Storytelling failed: "+repr(e))
    
    def showStory(self):
        return self.analysisResults
            


