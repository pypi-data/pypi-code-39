from .factory.OFXReaderFactory import OFXReaderFactory
from .factory.XLSReaderFactory import XLSReaderFactory
from .factory.PDFReaderFactory import PDFReaderFactory
from .factory.XLSMWriterFactory import XLSMWriterFactory

import logging

logger = logging.getLogger(__name__)

class ProsperarCore():
    def run(self, files):
        #ler o caminho do arquivo e verificar se ele existe
        if (not files):
            logger.info('No files specified.')
            return

        xlsFiles = []
        ofxFiles = []
        pdfFiles = []

        for file in files:
            try:
                if ('.xls' in file.filename):
                    xlsFiles.append(file)
                elif ('.pdf' in file.filename):
                    pdfFiles.append(file)
                else:
                    ofxFiles.append(file)
            except AttributeError:
                if ('.xls' in file.name):
                    xlsFiles.append(file)
                elif ('.pdf' in file.name):
                    pdfFiles.append(file)
                else:
                    ofxFiles.append(file)

        logger.info(ofxFiles)
        logger.info(xlsFiles)
        logger.info(pdfFiles)

        #chamar o leitor ofx
        factoryOFX = OFXReaderFactory()
        readerController = factoryOFX.createReaderController()
        ofxBankStmts = readerController.read(factoryOFX, files=ofxFiles)

        #chamar o leitor xls
        factoryXLS = XLSReaderFactory()
        readerController = factoryXLS.createReaderController()
        xlsBankStmts = readerController.read(factoryXLS, files=xlsFiles)

        #chamar o leitor pdf
        factoryPDF = PDFReaderFactory()
        readerController = factoryPDF.createReaderController()
        pdfBankStmts = readerController.read(factoryPDF, files=pdfFiles)

        bankStmts = xlsBankStmts + ofxBankStmts + pdfBankStmts

        #chamar o escritor xlsm
        factory = XLSMWriterFactory()
        writerController = factory.createWriterController()
        return writerController.write(bankStmts, factory)