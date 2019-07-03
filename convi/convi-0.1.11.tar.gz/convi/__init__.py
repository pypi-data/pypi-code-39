import csv,json
import anarcute
from convi.json_to_csv import *
def csv_to_json(fcsv,fjson):
	open(fjson,"w+").write(json.dumps(list(csv.DictReader(open(fcsv,"r+")))))
	return fjson
