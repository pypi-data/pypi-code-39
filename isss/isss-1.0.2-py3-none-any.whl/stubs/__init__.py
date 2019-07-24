###############################################################################################################
# Module: script.py
# Author: Romain Lienard (rlienard@gmail.com)
# Description : A library providing several wrappers for IBM Security Secret Server REST APIs
# License : Apache Licence version 2.0 + Cookieware variant - if you like this module, please send me biscuits
###############################################################################################################

class Stub:
    def __init__(self,isss,payload,allowCreate=True):
        self.isss = isss
        self.payload = payload
        self.api = None
        self.allowCreate = allowCreate
    
    def __getitem__(self,item):
        for i in self.payload:
            if i.lower() == item.lower():
                return self.payload[i]
        
        if "items" in self.payload:
            for i in self.payload["items"]:
                if i["fieldName"].lower() == item.lower():
                    return i["itemValue"]
            
        print(("warning: item not found (%s)"%(item)))
        return None
        
    def __setitem__(self,item,value):
        for i in self.payload:
            if i.lower() == item.lower():
                self.payload[i] = value
                return
        
        if "items" in self.payload:
            for i in self.payload["items"]:
                if i["fieldName"].lower() == item.lower():
                    i["itemValue"] = value
                    return
        
        allitems = []
        if "items" in self.payload:
            for i in self.payload["items"]:
                allitems.append("+ " + i["fieldName"] + " : " + str(i["itemValue"]))
        
        for i in self.payload:
            if i != "items":
                allitems.append("- " + i + " : " + str(self.payload[i]))

        raise Exception ("The field '%s' is not available in this stub. Possible fields are : \n%s " % (item, "\n".join(allitems) ) )
        return
    
    def __str__(self):
        allitems = []
        if "items" in self.payload:
            for i in self.payload["items"]:
                allitems.append("+ " + i["fieldName"] + " : " + str(i["itemValue"]))
                
        for i in self.payload:
            if i != "items":
                allitems.append("- " + i + " : " + str(self.payload[i]))

        return "\n".join(allitems)
    
    def create(self):
        if not self.allowCreate:
            raise Exception("This secret has already been created. Please use stub.update() instead")
    
    def update(self):
        if self.allowCreate:
            raise Exception("This secret has not been created and cannot be updated. Please use stub.create() instead")
            
    def delete(self):
        if self.allowCreate:
            raise Exception("This secret has not been created yet and cannot be deleted.")
    
    
class ResultStub(Stub):
    def __init__(self,isss,payload):
        Stub.__init__(self,isss,payload)
    
class SecretStub(Stub):
    def __init__(self,isss,payload,allowCreate=True):
        Stub.__init__(self,isss,payload)
        self.allowCreate = allowCreate
        if allowCreate:
            self.payload["siteId"] = 1
            
    def __repr__(self):
        return "<Secret id='%s' name='%s' template='%s' />" % (self["id"],self["name"],self["secretTemplateName"])
    
    def create(self):
        Stub.create(self)
        self.payload = self.isss.createSecret(self)            
        self.allowCreate = False
        return self
            
    def update(self):
        Stub.update(self)
        self.payload = self.isss.putSecret(self)
        return self 
    
    def delete(self):
        Stub.delete(self)
        self.isss.deleteSecret(self)
        return None
    
    def getPermissions(self):
        return self.isss.getSecretPermission(self["id"])
    
    def generatePassword(self,fieldName="password"):
        for i in self.payload["items"]:
            if i["fieldName"].lower() == fieldName.lower():
                fieldId = i["fieldId"]
                rep = self.isss.post("/secret-templates/generate-password/" + str(fieldId))
                return rep
        raise "No '"+ fieldName +"' field in this template. Unable to create a password with appropriate policy."
    

class UserStub(Stub):
    def __init__(self,isss,payload,allowCreate=True):
        Stub.__init__(self,isss,payload)
        self.payload["password"] = None
        self.payload["enabled"] = True
        self.allowCreate = allowCreate
    
    def create(self):
        Stub.create(self)
        self.payload = self.isss.createUser(self)
        self.payload["password"] = None
        self.allowCreate = False
        return self
    
    def update(self):
        Stub.update(self)
        self.payload = self.isss.putUser(self)
        self.payload["password"] = None
        return self

    def delete(self):
        Stub.delete(self)
        self.isss.deleteUser(self)
        return None
    
    def __repr__(self):
        return "<User id='%s' username='%s' displayName='%s' />" % (self["id"],self["userName"],self["displayName"])
    
    
class GroupStub(Stub):
    def __init__(self,isss,payload,allowCreate=True):
        Stub.__init__(self,isss,payload)
        self.allowCreate = allowCreate
        if allowCreate:
            self.payload["enabled"] = True
    
    def create(self):
        Stub.create(self)
        self.payload = self.isss.createGroup(self)
        self.allowCreate = False
        return self

    def update(self):
        Stub.update(self)
        self.payload = self.isss.putGroup(self)
        return self
            
    def add(self,usernameOrUserId):
        
        if isinstance(usernameOrUserId,str):
            user = self.isss.getUser(usernameOrUserId)
            if len(user) ==0:
                raise Exception("Unable to find a user with the query '%s'"%(usernameOrUserId))
            elif len(user) >1:
                raise Exception("More than one user has been returned. Unable to add the user (consider using a userId instead)")
            else:
                user = user[0]
            self.isss.post("/groups/%s/users"%(self.payload["id"]),{"userId":user["id"]})
        else:
            self.isss.post("/groups/%s/users"%(self.payload["id"]),{"userId":usernameOrUserId})
        
        return self
    
    def remove(self,usernameOrUserId):
        
        if isinstance(usernameOrUserId,str):
            user = self.isss.getUser(usernameOrUserId)
            if len(user) ==0:
                raise Exception("Unable to find a user with the query '%s'"%(usernameOrUserId))
            elif len(user) >1:
                raise Exception("More than one user has been returned. Unable to remove the user (consider using a userId instead)")
            else:
                user = user[0]
            self.isss.delete("/groups/%s/users/%s" % (self.payload["id"],user["id"]) )
        else:
            self.isss.delete("/groups/%s/users/%s" % (self.payload["id"],usernameOrUserId) )
        
        return self
    
    def delete(self):
        Stub.delete(self)
        self.isss.deleteGroup(self)
        return None
    
    def getUsers(self):
        res = self.isss.get("/groups/%s/users"%(self.payload["id"]))
        users =  [{"id":u["userId"],"username":u["userName"]} for u in res["records"]]
        return users
    
    def __repr__(self):
        return "<Group id='%s' name='%s' enabled='%s' />" % (self["id"],self["name"],self["enabled"])
        
        
class SecretPermissionStub(Stub):
    def __init__(self,isss,payload,allowCreate=True):
        Stub.__init__(self,isss,payload)
        self.allowCreate = allowCreate
        
    
    def create(self):
        Stub.create(self)
        self.payload = self.isss.createSecretPermission(self)
        self.allowCreate = False
        return self  
    
    def update(self):
        Stub.update(self)
        self.payload = self.isss.putSecretPermission(self)
        return self 
    
    def delete(self):
        Stub.delete(self)
        self.isss.deleteSecretPermission(self)
        return None

    def __setitem__(self,item,value):
        if item.lower() == "secretaccessrolename":
            if value.lower() not in ["owner","view","list","edit"]:
                raise Exception("This specific stub value must be one of the following : Owner, View, List, Edit")
        Stub.__setitem__(self,item,value)
        
    def __repr__(self):
        return "<SecretPermission id='%s' secretAccessRoleName='%s' secretId='%s' username='%s' />" % (self["id"],self["secretAccessRoleName"],self["secretId"],self["userName"])
    
    
class FolderPermissionStub(Stub):
    def __init__(self,isss,payload,allowCreate=True):
        Stub.__init__(self,isss,payload)
        self.allowCreate = allowCreate
        
    
    def create(self):
        Stub.create(self)
        self.payload = self.isss.createFolderPermission(self)
        self.allowCreate = False
        return self  
    
    def update(self):
        Stub.update(self)
        self.payload = self.isss.putFolderPermission(self)
        return self 
    
    def delete(self):
        Stub.delete(self)
        self.isss.deleteFolderPermission(self)
        return None

    def __setitem__(self,item,value):
        if item.lower() == "secretaccessrolename":
            if value.lower() not in ["owner","view","list","edit"]:
                raise Exception("This specific stub value must be one of the following : Owner, View, List, Edit")
        Stub.__setitem__(self,item,value)
        
    def __repr__(self):
        return "<FolderPermission id='%s' secretAccessRoleName='%s' folderId='%s' username='%s' />" % (self["id"],self["secretAccessRoleName"],self["folderId"],self["userName"])
    
    
class FolderStub(Stub):
    def __init__(self,isss,payload,allowCreate=True):
        Stub.__init__(self,isss,payload)
        self.allowCreate = allowCreate
        
    
    def create(self):
        Stub.create(self)
        self.payload = self.isss.createFolder(self)
        self.allowCreate = False
        return self  
    
    def update(self):
        Stub.update(self)
        self.payload = self.isss.putFolder(self)
        return self 
    
    def getPermissions(self):
        return self.isss.getFolderPermission(self["id"])
    
    def delete(self):
        Stub.delete(self)
        self.isss.deleteFolder(self)
        return None
        
    def __repr__(self):
        return "<Folder id='%s' name='%s' path='%s'/>" % (self["id"],self["folderName"],self["folderPath"])