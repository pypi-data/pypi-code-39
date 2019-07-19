import re
from winterboot.Autowired import Autowired
from winterboot.Service import Service

config = Autowired('config')
choiceAskService = Autowired('choiceAskService')

@Service
class ChoiceObtainerService:

    def obtainChoice(self,options):
        answer = choiceAskService.askUserForChoice()
        choice = self.computeChoiceFromAnswer(options, answer)
        return choice

    def computeChoiceFromAnswer(self,options, answer):
        asNum = self.num(answer)
        if asNum in options:
            choice = options[asNum][1]
        elif re.match(config.CHOICE_FORMAT_REGEX, answer):
            choice = answer.split(",")
        else:
            choice = None
        return choice

    def num(self,s):
        try:
            return int(s)
        except ValueError:
            return None

