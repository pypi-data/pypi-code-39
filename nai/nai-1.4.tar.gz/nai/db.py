'''
___NDB___
DEV : Nasir Ali
GITHUB : github.com/nasirxo
'''

#Standard Libraries
import json
import zlib
import sys
import os

#Available DB's
def dblist(path):  
 dir = os.listdir(path)
 dbs = []
 for file in dir:
   try:
     if file[-3:] == 'ndb':
       dbs.append(file)    
   except:
     pass
 return dbs

#DB Creation Class
class makedb:
  def __init__(self,dbr):
    with open(dbr,"wb") as dbc:
       dbc.write(zlib.compress("{}"))

#DB Connection Class  
class ndbconnect:
 def __init__(self,rx):
  self.rxx = zlib.decompress(open(rx,"rb").read())
  self.rx = rx
  if len(self.rxx) != 0:
      self.darray = json.loads(self.rxx)
  else:
      self.darray = []
      
 def add(self,dx,dy):
  self.darray[dx] = dy
  with open(self.rx,"wb") as dbw:
    dbw.write(zlib.compress(json.dumps(self.darray)))

 def show(self):
   return self.darray

 def find(self,word):
   return self.darray.get(word)
   
 def findval(self,value):
   for word in self.darray.keys():
    if str(type(self.darray.get(word))) == "<type 'list'>":
       if value in self.darray.get(word):
          return self.darray.get(word)
     
 def findtext(self,text):
  for key in self.darray.keys():
    try:
      if text in self.darray.get(key):
         return self.darray.get(key)
      else:
         continue
    except:
      pass
         
 def size(self):
   return {
   'db_name':self.rx,
   'db_type':'nex_ndb',
   'memory':sys.getsizeof(self.darray),
   'length':len(self.darray.keys()),
   'size':'{} bytes'.format(len(str(self.darray)))
   }
   
 def remove(self,query):
  return {
    'query':query,
    'value':self.darray.pop(query),
    'status':'removed'
  } 

 def clear(self):
  sz = len(str(self.darray))
  self.darray.clear()
  return {
    'query':'all',
    'status':'cleared_all',
    'data':'{} bytes'.format(sz)
  }
  
