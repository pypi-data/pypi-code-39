#!/usr/bin/env python3

##############################################################################################################
# Module: isss.py
# Author: Romain Lienard (rlienard@gmail.com)
# Description : A library providing several wrappers for IBM Security Secret Server REST APIs
# License : Apache Licence version 2.0 + Cookieware variant - if you like this module, please send me biscuits
###############################################################################################################

import json
import urllib.request, urllib.parse, urllib.error,urllib.request,urllib.error,urllib.parse
import ssl
from http.cookiejar import CookieJar
from hashlib import md5
import re
import shutil
import os,os.path
import time
import tkinter
import sys
from threading import Thread
import sys
import time

cj = CookieJar()
ignoreSSL = ssl._create_unverified_context()
handler = urllib.request.HTTPSHandler(context=ignoreSSL)
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj),handler)

version = "1.0"
    

from isss.stubs import *
from isss.script import Script

    
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"    

class ISSS:
    
    def __init__(self,url,username,password,experimentalMode=False,ignoreWarning=False):
        self.OWNER = 1
        self.EDIT = 2
        self.VIEW = 3
        self.LIST = 4
        self.loginParams = {}
        self.url = url
        self.username = username
        self.password = password
        self.api = "/api/v1"
        self.cacheToken = None
        self.expireToken = None
        
        if experimentalMode:
            if not ignoreWarning:
                print("experimental mode is enabled. things might not work as expected :-)")
            self.login(username,password)
            self.adminScriptsToken = self.getTokenFromUrl("/AdminScripts.aspx","window.aftToken") 
    
    
    def getAccessToken(self):
        if not self.cacheToken or (self.expireToken < time.time()):
            data = {"username":self.username,"password":self.password,"grant_type":"password"}
            req = urllib.request.Request(self.url + "/oauth2/token",urllib.parse.urlencode(data).encode("utf-8"))
            res = urllib.request.urlopen(req,context=ignoreSSL)
            self.cacheToken = json.load(res)["access_token"]
            self.expireToken = time.time()+300
        
        return self.cacheToken
    
    def get(self,url,params=None):
        url = self.url + self.api + url
        
        if params and params != "":
            url+="?" + urllib.parse.urlencode(params)
        try:
            req = urllib.request.Request(url,headers={"Authorization":"Bearer " + self.getAccessToken()})
            return json.load(urllib.request.urlopen(req,context=ignoreSSL))
        
        except urllib.error.HTTPError as e:
            raise Exception("The server returned an error:\n" + e.read().decode())
        
        except Exception as e:
            print (e)
            raise Exception("Unexpected error.")
        
    def post(self,url,data="",method="POST"):
        url = self.url + self.api + url
        
        if data != "":
            data = json.dumps(data)
            
        try:
            req = urllib.request.Request(url,data.encode("utf-8"),headers={"Authorization":"Bearer " + self.getAccessToken(),"Content-Type":"application/json; charset=UTF-8",},method=method)
            return json.load(urllib.request.urlopen(req,context=ignoreSSL))
        
        except urllib.error.HTTPError as e:
            raise Exception("The server returned an error:\n" + e.read().decode())
            
        except Exception as e:
            print(e)
            raise Exception("Unexpected error.")
            
    def put(self,url,data=""):
        return self.post(url,data,"PUT")
    
    def delete(self,url,data=""):
        return self.post(url,data,"DELETE")
    
    def getAnything(self,url,idOrText=None):
        
        if isinstance(idOrText,int):
            return self.get(url+"/"+str(idOrText))
        
        elif isinstance(idOrText,str):
            params = {
                    "filter.searchText" : idOrText,
                    "take" : 100
                     }
            resp = self.get(url,params)
        else:
            resp = self.get(url)
            
        if resp != []:
            if "records" in resp:
                return resp["records"]
            else:
                return resp
        else:
            return []
        
    
    
    
    
    def getUser(self,idOrText=""):
        res = self.getAnything("/users",idOrText)
        if isinstance(idOrText,str):
            tab = []
            for r in res:
                tab.append(UserStub(self,r,False))
            return tab
        else:
            return UserStub(self,res,False)
    
    def getTemplate(self,idOrText=""):
        return self.getAnything("/secret-templates",idOrText)
    
    def getGroup(self,idOrText=""):
        res = self.getAnything("/groups",idOrText)
        if isinstance(idOrText,str):
            tab = []
            for r in res:
                tab.append(GroupStub(self,r,False))
            return tab
        else:
            return GroupStub(self,res,False)
    
    def getFolder(self,idOrText=""):
        res = self.getAnything("/folders",idOrText)  
        if isinstance(idOrText,str):
            tab = []
            for r in res:
                tab.append(FolderStub(self,r,False))
            return tab
        else:
            return FolderStub(self,res,False) 
    
    def getSecret(self,idOrText=""):
        res = self.getAnything("/secrets",idOrText) 
        if isinstance(idOrText,str):
            tab = []
            for r in res:
                tab.append(SecretStub(self,r,False))
            return tab
        else:
            return SecretStub(self,res,False) 

    def getSecretPermission(self,secretId):
        res = self.getAnything("/secret-permissions?filter.secretId=" + str(secretId)) 
        tab = []
        for r in res:
            tab.append(SecretPermissionStub(self,r,False))
        return tab
    
    def getFolderPermission(self,folderId):
        res = self.getAnything("/folder-permissions?filter.folderId=" + str(folderId)) 
        tab = []
        for r in res:
            tab.append(FolderPermissionStub(self,r,False))
        return tab
    
    
    
    
    
    
    def getUserStub(self):
        return UserStub(self,self.getAnything("/users/stub"))
    
    def getSecretStub(self,templateId):
        res = self.getAnything("/secrets",idOrText) 
        if isinstance(idOrText,str):
            tab = []
            for r in res:
                tab.append(SecretStub(self,r,False))
            return tab
        else:
            return SecretStub(self,res,False) 
    
    def getGroupStub(self):
        return GroupStub(self,self.getAnything("/groups/stub"))
    
    def getFolderStub(self):
        return FolderStub(self,self.getAnything("/folders/stub"))
    
    def getSecretPermissionStub(self,secretId):
        return SecretPermissionStub(self,self.getAnything("/secret-permissions/stub?secretId="+str(secretId)))
    
    def getFolderPermissionStub(self,folderId):
        return FolderPermissionStub(self,self.getAnything("/folder-permissions/stub?folderId="+str(folderId)))
    
    def createSecret(self,stub):    
        rep = self.post("/secrets",stub.payload)
        return rep
    def createUser(self,stub):    
        rep = self.post("/users",stub.payload)
        return rep
    
    def createGroup(self,stub):    
        rep = self.post("/groups",stub.payload)
        return rep
    
    def createSecretPermission(self,stub):    
        rep = self.post("/secret-permissions",stub.payload)
        return rep
    
    def createFolder(self,stub):    
        rep = self.post("/folders",stub.payload)
        return rep
    
    def createFolderPermission(self,stub):    
        rep = self.post("/folder-permissions",stub.payload)
        return rep
    
    
    
    def putAnything(self,url,payload):
        return self.put(url,payload)
    
    def putSecret(self,stub):
        rep = self.put("/secrets/"+str(stub["id"])+"/restricted",stub.payload)
        return rep
    
    def putUser(self,stub):
        rep = self.put("/users/"+str(stub["id"]),stub.payload)
        return rep
    
    def putSecretPermission(self,stub):
        rep = self.put("/secret-permissions/"+str(stub["id"]),stub.payload)
        return rep
    
    def putFolderPermission(self,stub):
        rep = self.put("/folder-permissions/"+str(stub["id"]),stub.payload)
        return rep
    
    def putGroup(self,stub):
        rep = self.put("/groups/"+str(stub["id"]),stub.payload)
        return rep
    
    def putFolder(self,stub):
        rep = self.put("/folders/"+str(stub["id"]),stub.payload)
        return rep
    
    
    def deleteSecret(self,stub):
        self.delete("/secrets/"+str(stub["id"]))
        
    def deleteUser(self,stub):
        self.delete("/users/"+str(stub["id"]))
        
    def deleteSecretPermission(self,stub):
        self.delete("/secret-permissions/"+str(stub["id"]))
        
    def deleteFolderPermission(self,stub):
        self.delete("/folder-permissions/"+str(stub["id"]))
        
    def deleteGroup(self,stub):
        self.delete("/groups/"+str(stub["id"]))
        
    def deleteFolder(self,stub):
        self.delete("/folders/"+str(stub["id"]))
    
    
    ####################################
    #Experimental section
    ####################################
    
    
    def getLoginPage(self):
        req = urllib.request.Request(self.url + "/login.aspx",headers={
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"})
        #data = urllib2.urlopen(req,context=ignoreSSL).read()
        data = opener.open(req).read().decode()
        toSearch = ["__VIEWSTATE","__VIEWSTATEGENERATOR","__EVENTVALIDATION","__RequestVerificationToken"]

        for item in toSearch:
            r = re.compile('name="('+item+')" (id=".+?" )?(type="hidden" )?value="(.+?)"')
            for m in re.finditer(r,data):
                #print m.group(1),"=>",m.group(4)
                self.loginParams[m.group(1)] = m.group(4)
            
    def login(self,username,password):
        self.getLoginPage()
        url = self.url + "/login.aspx"
        data = {
                "LoginUserControl1$HasAddSecretPermissionControl":"false",
                "LoginUserControl1$UserNameTextBox":username,
                "LoginUserControl1$UserNameOriginalHiddenField":"",
                "LoginUserControl1$PasswordTextBox":password,
                "LoginUserControl1$LoginButton":"Login",
                "LoginUserControl1$LoginDialog_IsCollapsed":"0",
                "__SCROLLPOSITIONX" : "0",
                "__SCROLLPOSITIONY" : "0",
                "__EVENTTARGET" : "",
                "__EVENTARGUMENT" : ""
               }
        
        for k in self.loginParams:
            data[k] = self.loginParams[k]
        
        req = urllib.request.Request(url,urllib.parse.urlencode(data).encode("utf-8"),headers={
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Content-Type":"application/x-www-form-urlencoded",
            
        })
        data = opener.open(req).read()
        
   
    
    def getTokenFromUrl(self,url,name):
        req = urllib.request.Request(
        self.url + url,
        headers={
            "User-Agent":USER_AGENT,
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        }
        )
        data = opener.open(req).read().decode()
        
        r = re.compile(name + " = '(.+?)'");
        for m in re.finditer(r,data):
            return m.group(1)
        
        return None
    
    
    def getScriptList(self):
        req = urllib.request.Request(
        self.url + "/AdminScripts.aspx",
        headers={
            "User-Agent":USER_AGENT,
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        }
        )
        data = opener.open(req).read().decode()
        
        r = re.compile("var scripts = (\\[.+?\\]);");
        
        for m in re.finditer(r,data):
            scripts = json.loads(m.group(1))
            result = []
            for s in scripts:
                script = Script(self.url,s,self.adminScriptsToken,True)
                result.append(script)
            return result
        else:
            return []
        

    def getScript(self, scriptOrScriptId):
        if isinstance(scriptOrScriptId,Script):
            scriptId = scriptOrScriptId._id
        else:
            scriptId = scriptOrScriptId
        
        try:
            req = urllib.request.Request(
                self.url + "/ajax/AjaxServices.asmx/GetPowershellScript",
                str({"powershellScriptId":scriptId}).encode("utf-8"),
                headers={
                    "User-Agent":USER_AGENT,
                    "Content-Type":"application/json; charset=UTF-8",
                    "X-Requestverificationtoken":self.adminScriptsToken
                }
            )
            parsed = json.load(opener.open(req))
            script = Script(self.url,parsed,self.adminScriptsToken)
            return script
        
        except Exception as e:
            print (e)
            return []

            
    
    def showPopup(self,message,color="black"):
        root = tkinter.Tk()
        
        def callback():
            root.destroy()
            
        root.title("python for isss")
        label = tkinter.Label(root, text=" " + message + " ",fg=color)
        btn = tkinter.Button(root, text="close",command=callback)
        label.pack()
        btn.pack()
        #root.after(2000, root.destroy)
        root.mainloop()
    
    def fw(self,directory):
        def getsum(directory,f):
            try:
                with open(os.path.join(directory,f)) as ff:
                    return md5(ff.read().encode("utf-8")).hexdigest()
            except Exception as e:
                print (e)
                print(("error while getsum('%s')"%(os.path.join(directory,f))))
        
        if os.path.isfile(directory):
            raise Exception ("The specified path is not a directory but an existing file.")
        
        if os.path.exists(directory):
            rep = input ("The specified directory already exists, existing content will be deleted. Continue (y/n) [y] ? ").strip().lower()
            if rep == "y" or rep == "":
                print(("Cleaning directory %s ..." % (directory)))
                shutil.rmtree(directory)
                os.mkdir(directory)
            else:
                print("Aborting.")
                return
        
        if not os.path.exists(directory):
            print(("Directory %s doesn't exist. Creating directory..." % (directory)))
            os.mkdir(directory)
        
        sys.stdout.write("Starting Filewatcher [----------]")
        
        scripts = self.getScriptList()
        scriptmap = {}
        
        if len(scripts) == 0:
            print ("\nUnable to retrieve any script. Please check your connection settings and try again.")
            sys.exit(1)
        
        sys.stdout.flush()
        
        pos = 0
        step = 100.0/len(scripts)
        
        for s in scripts:
            script = self.getScript(s)
            pos+=step
            prog = int(round(pos / 10.0,0))
            sys.stdout.write("\rStarting Filewatcher ["+ ("*" * prog) + ("-" * (10-prog)) + "]")
            sys.stdout.flush()
            scriptmap [s.filename] = script
            with open(os.path.join(directory,s.filename),"w") as out:
                out.write(script.content)
                
        sums = {}
        
        init = True
        
        sys.stdout.write( "\rFilewatcher is now open for e-business ! (press ctrl+c to quit)\n")
        sys.stdout.flush()

        try:
            while True:
                for f in os.listdir(directory):
                    if f not in sums:
                        if init:
                            sums[f] = getsum(directory,f)
                        else: 
                            print(("new file detected : " + f))
                            sums[f] = getsum(directory,f)
                    else:
                        newSum = getsum(directory,f)
                        if sums[f] != newSum:
                            print(("file modified : " + f))
                            sums[f] = newSum
                            if (re.match("^.+?[.](ps|sh|sql)$",f)):
                                with open(os.path.join(directory,f)) as ff:
                                    scriptmap[f].content = ff.read()
                                    if scriptmap[f].update(): #todo : find a way to display a popup which doesn't hang :-/
                                        print ("file updated successfully on server")
                                        #self.showPopup("Success : '%s' updated successfully on server"%(f),"green")
                                        
                                    else:
                                        print ("error while updating file on server")
                                        #self.showPopup("Error : '%s' has NOT been updated on server."%(f),"red")
                                        
                        else:
                            pass
                init = False
                time.sleep(1)
                
                
        except KeyboardInterrupt:
            print("Filewatcher is now stopped. Bye")
   
