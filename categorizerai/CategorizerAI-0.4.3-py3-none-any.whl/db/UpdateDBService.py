from winterboot.Autowired import Autowired
from winterboot.Service import Service
import types

config = Autowired('config')

@Service
class UpdateDBService:
    
    def updateRow(self, connection, oid, row, choice):
        table = config().figureOutTable(row)
        sentence = self.createUpdateSentence(oid, choice, table)
        cursor = connection.cursor()
        cursor.execute(sentence)
        connection.commit()
        cursor.close()

    def createUpdateSentence(self, oid, choice, table):
        args = types.SimpleNamespace()
        args.table = table
        args.choice = choice
        args.oid = oid
        sentence = config().SQL_TO_UPDATE_RECORD.format(args)
        return sentence

