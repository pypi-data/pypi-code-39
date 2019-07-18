import json
import datastories.analytical as datastories

class metaData(object):
    def __init__(self,**kwargs):
        try:
            metadatafile=open(kwargs.get("jsonMetaDataFile")).read()
            jsonfile=json.loads(metadatafile)
            self.datastories=datastories.DataStoryPattern(sparqlEndpoint=kwargs.get("sparqlEndPointUrl"),
                                                            jsonmetadata=jsonfile)
        except Exception as e:
            raise Exception("Metadata/Endpoint error: " +e)