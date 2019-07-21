
import sys
from winterboot.Autowired import Autowired
from winterboot.Service import Service

config = Autowired('config')
displayAccuracyService = Autowired('displayAccuracyService')
accuracyErrorDisplayService = Autowired('accuracyErrorDisplayService')

@Service
class AccuracyCheckService:
    
    def checkAccuracy(self, accuracy):

        displayAccuracyService().displayAccuracy(accuracy)
        if accuracy < config().MIN_ACCURACY:
            accuracyErrorDisplayService().displayAccurracyError()
            sys.exit(-1)

