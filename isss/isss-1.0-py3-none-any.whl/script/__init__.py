###############################################################################################################
# Module: script.py
# Author: Romain Lienard (rlienard@gmail.com)
# Description : A library providing several wrappers for IBM Security Secret Server REST APIs
# License : Apache Licence version 2.0 + Cookieware variant - if you like this module, please send me biscuits
###############################################################################################################

class Script:
    
    extensions = {1:"ps",2:"sql",3:"sh"}
    
    def __init__(self,url,payload,token,scriptList=False):
        self._url = url
        self._payload = payload
        self._token = token
        self._scriptList = scriptList
        
        if not scriptList:
            self._id = payload["d"]["ScriptId"]
            self.scriptType = payload["d"]["ScriptType"]
            self.name = payload["d"]["Name"]
            self.content = payload["d"]["Script"]
            self.description = payload["d"]["Description"]
            self.active = payload["d"]["Active"]
            self.scriptCategoryId = payload["d"]["ScriptCategoryId"]    
        else:
            self._id = payload["ScriptId"]
            self.scriptType = payload["ScriptType"]
            self.name = payload["Name"]
            self.content = payload["Script"]
            self.description = payload["Description"]
            self.active = payload["Active"]
            self.scriptCategoryId = payload["ScriptCategoryId"] 
            
        self.filename = self.name + "." + Script.extensions[self.scriptType]
        
    def __str__(self):
        return '<ISSS_Script id="%s" name="%s" description="%s" content="%s" />' %(self._id,self.name,self.description,self.content)
    
    def update(self):
        if self._scriptList:
            raise Exception("Cannot update this script. You need to retrieve the full content using isss.getScript(<script>) first")
            
        updatePayload = {"script":
                {
                 "ScriptId":self._id,
                 "Name":self.name,
                 "Description":self.description,
                 "ScriptCategoryId":self.scriptCategoryId,
                 "Script":self.content,
                 "Active":self.active,
                 "ScriptType":self.scriptType,
                 "AdditionalData":self._payload["d"]["AdditionalData"]
                 }
        }
        
        updatePayload = json.dumps(updatePayload)
        
        try:
            req = urllib.request.Request(
                self._url + "/ajax/AjaxServices.asmx/UpdateScript",
                updatePayload.encode("utf-8"),
                headers={
                    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
                    "Content-Type":"application/json; charset=UTF-8",
                    "X-Requestverificationtoken":self._token,
                    "Accept" : "application/json, text/javascript, */*; q=0.01",
                    "X-Requested-With" : "XMLHttpRequest"
                }
            )
            parsed = json.load(opener.open(req))
            
            return parsed["d"]["Success"]
        
        except Exception as e:
            print (e)
            return False