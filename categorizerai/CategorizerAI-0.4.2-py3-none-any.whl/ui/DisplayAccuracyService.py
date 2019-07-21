from winterboot.Service import Service

ACCURACY_STRING = "accuracy:{0}"

@Service
class DisplayAccuracyService:
    
    def displayAccuracy(self,accuracy):
        return print(ACCURACY_STRING.format(str(accuracy)))

