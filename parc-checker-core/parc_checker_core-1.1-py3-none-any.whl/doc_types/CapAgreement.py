from parc_checker_core import checkers
import json
from parc_checker_core.action import Action
from executor import task as tasks
from parc_checker_core.document_checker import DocumentChecker

DOC_TYPE = "CapAgreement"

def run(request, response, action):
    return DocumentTypeChecker(DOC_TYPE)(request, response, action)

class DocumentTypeChecker(DocumentChecker):

    def on_get(self, request, response):
        pass
    
    def on_create(self, request, response):
        pass

    def on_update(self, request, response):
        ARRW0721 = request["ARRW0721"]
        #ARRW0722 = request["ARRW0722"]
        ARRW0723 = request["ARRW0723"]
        #ARRW0725 = request["ARRW0725"]
        #ARRW0726 = request["ARRW0726"]

        self.add_task(tasks.Task("CapAgreement - UPDATE - REQ - Check ARID", checkers.getFieldHasValueChecker(ARRW0721, "ARID")))
        self.add_task(tasks.Task("CapAgreement - UPDATE - REQ - Check Open date", checkers.getFieldHasValueChecker(ARRW0721, "OPENDATE")))
        self.add_task(tasks.Task("CapAgreement - UPDATE - REQ - Check agreement status", checkers.getFieldValueChecker(ARRW0721, "LIFECYCLESTATUS", "EFFEC")))
        self.add_task(tasks.Task("CapAgreement - UPDATE - REQ - Check SEB party code", checkers.getFieldHasValueChecker(ARRW0721, "LGLPTCODE")))
        self.add_task(tasks.Task("CapAgreement - UPDATE - REQ - Check SEB party name", checkers.getFieldHasValueChecker(ARRW0721, "LGLPTNAME")))
        self.add_task(tasks.Task("CapAgreement - UPDATE - REQ - Check agreement type", checkers.getFieldValueChecker(ARRW0721, "DCTMPLTVER", "CAPAGREEMENT")))
        self.add_task(tasks.Task("CapAgreement - UPDATE - REQ - Check Jurisdiction", checkers.getFieldHasValueChecker(ARRW0721, "JURISDICTION")))
        self.add_task(tasks.Task("CapAgreement - UPDATE - REQ - Check Physical store", checkers.getFieldHasValueChecker(ARRW0721, "PHYSTORAGE")))
        self.add_task(tasks.Task("CapAgreement - UPDATE - REQ - Check Document id", checkers.getFieldHasValueChecker(ARRW0721, "DOCUMENTID")))
        self.add_task(tasks.Task("CapAgreement - UPDATE - REQ - Check Tracking id", checkers.getFieldHasValueChecker(ARRW0721, "TRACKING_ID")))

        self.add_task(tasks.Task("CapAgreement - UPDATE - REQ - Check NETTMETHTP has value", checkers.getFieldHasValueChecker(ARRW0723, "NETTMETHTP")))
        self.add_task(tasks.Task("CapAgreement - UPDATE - REQ - Check TRMNTCURR has value", checkers.getFieldHasValueChecker(ARRW0723, "TRMNTCURR")))
        self.add_task(tasks.Task("CapAgreement - UPDATE - REQ - Check INTCROSSDEFAULT has value", checkers.getFieldHasValueChecker(ARRW0723, "INTCROSSDEFAULT")))
        self.add_task(tasks.Task("CapAgreement - UPDATE - REQ - Check CUSCROSSDEFAULT has value", checkers.getFieldHasValueChecker(ARRW0723, "CUSCROSSDEFAULT")))
        self.add_task(tasks.Task("CapAgreement - UPDATE - REQ - Check REGAPPRNET has value", checkers.getFieldHasValueChecker(ARRW0723, "REGAPPRNET")))
        self.add_task(tasks.Task("CapAgreement - UPDATE - REQ - Check FORCEMAJAMENDMT has value", checkers.getFieldHasValueChecker(ARRW0723, "FORCEMAJAMENDMT")))

    def on_delete(self, request, response):
        pass

    def on_change_cp(self, request, response):
        pass
