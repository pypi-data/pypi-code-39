from winterboot.Autowired import Autowired
from winterboot.Service import Service

config = Autowired('config')

@Service
class RowProviderService:

    def getRowByOid(self, connection, oidAsStr):
        cursor = connection.cursor()
        sqlCommand = config().SQL_TO_OBTAIN_TRANSACTION_BY_OID.format(oidAsStr)
        cursor.execute(sqlCommand)
        row = cursor.fetchone()
        cursor.close()
        return row
