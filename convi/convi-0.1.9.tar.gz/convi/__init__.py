import csv,json
import anarcute
from convi.json_to_csv import *
def json_to_csv(fjson,fcsv):
	anarcute.write_csv(fcsv,json.load(open(fjson,"r+")))
	return fcsv