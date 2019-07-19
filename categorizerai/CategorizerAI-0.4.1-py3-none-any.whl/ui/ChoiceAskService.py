from winterboot.Service import Service

PROMPT = "choice: "

@Service
class ChoiceAskService:
    
    def askUserForChoice(self):
        answer = input(PROMPT)
        return answer
