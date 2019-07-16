#!/usr/bin/env python3
# v2019.02.13

import datetime
import time
import platform
import os
import threading

NONE = 0
TRACE = 1
DEBUG = 2
INFO = 3
WARN = 4
ERROR = 5
FATAL = 6
levelstr = [ "-", "T", "D", "I", "W", "E", "F" ]

#tlist={}

class logger:

	def __init__(self):
		self.file=None
		self.level=INFO
		self.indent=0
		self.host=platform.node()
		self.app="-"
		self.ver="-"
		self.api="-"
		self.traceid="-"
		self.userhost="-"
		self.username="-"
		self.pid=str(os.getpid())
		self.disabletid=False
		self._timezone=None
		self._timezonename=""

	# Propiedad timezone
	def get_timezone(self): return self._timezone
	def set_timezone(self, timezone):
		if timezone=="utc":
			self._timezone=datetime.timezone.utc
			self._timezonename="Z"
		elif timezone=="local":
			tz=datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
			self._timezone=tz
			self._timezonename=str(tz)
		elif timezone==None:
			self._timezone=None
			self._timezonename=""
		else:
			self._timezone=timezone
			self._timezonename=str(timezone)
	def del_timezone(self):
		del self._timezone
		self._timezonename=""
	timezone=property(get_timezone, set_timezone, del_timezone)

	def enter(self, level=0, msg=""): self.write(level, msg, ind=1)
	def exit(self, level=0, msg=""): self.write(level, msg, ind=2)
	def call(self, level=0, msg=""): self.write(level, msg, ind=3)
	def inside(self, level=0, msg=""): self.write(level, msg, ind=4)

	def trace(self, msg, ind=0): self.write(TRACE,msg,ind)
	def debug(self, msg, ind=0): self.write(DEBUG,msg,ind)
	def info(self, msg, ind=0): self.write(INFO,msg,ind)
	def warn(self, msg, ind=0): self.write(WARN,msg,ind)
	def error(self, msg, ind=0): self.write(ERROR,msg,ind)
	def fatal(self, msg, ind=0): self.write(FATAL,msg,ind)

	def write(self,level=0,msg="",ind=0):

		if level<self.level: return

		tt=time.time()
		
		# fecha
		isotime=datetime.datetime.fromtimestamp(tt,self._timezone).strftime("%Y-%m-%dT%H:%M:%S.%f"+self._timezonename) # [0:26]

		# thread id
		if self.disabletid==True: tid=""
		else:
			tid=threading.current_thread().name
			if tid[0:7] == "Thread-": tid=tid.replace("Thread-", "").zfill(4)
			if tid=="MainThread": tid="0000"
			tid="."+tid

		# level
		lvl=levelstr[level]

		# indentación
		if ind==2: self.indent-=1
		sepstr=""
		for i in range(0,self.indent): sepstr+="| "
		if ind==0: indchar="|"
		else:
			if ind==1: indchar="/"
			if ind==2: indchar="\\"
			if ind==3: indchar=">"
			if ind==4: indchar="]"
			sepstr+=indchar+" "
		if ind==0: indnum="0"
		else: indnum=str(self.indent+1)
		if ind==1: self.indent+=1
		
		# juntamos
		line="\t".join((isotime,self.host,self.pid+tid,self.app,self.ver,self.api,self.traceid,self.userhost,self.username,lvl,indnum,indchar,sepstr+msg))

		if self.file!=None:
			f=open(self.file, "a")
			f.write(line+"\n")
		else:
			print(line,flush=True)

#def method(fn):
#
#    @wraps(fn)
#    def wrapped(*args, **kws):
#
#        global tloc
#        if getattr(tloc, 'sep', None) is None: tloc.sep = 0
#
#        info("/ "+fn.__module__+"."+fn.__name__)
#        tloc.sep+=1
#        try:
#            ret=fn(*args, **kws)
#        except Exception as ex:
#            error("Error: "+type(ex).__name__+" "+str(ex))
#            tloc.sep-=1
#            info("\ "+fn.__module__+"."+fn.__name__)
#            raise
#        tloc.sep-=1
#        info("\ "+fn.__module__+"."+fn.__name__)
#        return ret
#
#    return wrapped

