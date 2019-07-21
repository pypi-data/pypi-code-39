from winterboot.Service import Service

@Service
class TransactionDisplayService:

    def displayTransaction(self,row):
        print(row)
