#!/usr/bin/env python3

import sys
sys.path.insert(1,"../src")
import ivlog
import time

#from pyvn import ivlog

def logdata(log):
	log.file="test.log"
	#log.ivlog=True
	log.app="KM"
	log.ver="8.25"
	log.apim="R"
	log.apin="3"
	log.traceid="DMS4LVYXYUTFK"
	log.ip="216.58.201.131"
	log.user="none"

	log.info("* Init")
	log.enter(ivlog.INFO, "func")
	log.debug("uno")
	log.enter(ivlog.DEBUG, "func2")
	log.user="jbiosca"
	log.info("dos")
	log.exit(ivlog.DEBUG, "func2")
	log.trace("tres")
	log.exit(ivlog.INFO,"func")

#log.ivlog=True

log=ivlog.logger()
log.level=ivlog.TRACE
logdata(log)

#print("---")

log=ivlog.logger()
log.level=ivlog.INFO
logdata(log)
