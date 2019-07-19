from winterboot.Autowired import Autowired
from winterboot.Service import Service

rowProviderService = Autowired('rowProviderService')
transactionDisplayService = Autowired('transactionDisplayService')
updateDBService = Autowired('updateDBService')
optionPreparatorService = Autowired('optionPreparatorService')
choiceObtainerService = Autowired('choiceObtainerService')

@Service
class RowUpdateService:

    def handleOneRow(self, rowNumber, data, connection, categories):
        oidAsStr = str(data.problemOids[rowNumber])
        row = rowProviderService.getRowByOid(connection, oidAsStr)
        transactionDisplayService.displayTransaction(row)
        options = optionPreparatorService.prepareOptionsToOffer(rowNumber, data, categories)
        choice = choiceObtainerService.obtainChoice(options)
        if choice is not None:
            updateDBService.updateRow(connection, oidAsStr, row, choice)
