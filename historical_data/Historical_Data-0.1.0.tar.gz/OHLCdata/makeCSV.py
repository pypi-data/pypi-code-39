import requests, json, csv

#Given a filename and json data from TD Ameritrade API (endpoint)
#method with create a csv file (filename.csv)
#assumes that file name is a string that is named 'filename'.csv
def json_to_csv(filename, json_data):
	json_parsed = json.loads(json_data)
        ohlc_data   = json_data['candles']
        filename    = open('/ohlc_prices/%s' % filename, 'w+')
        csvwriter   = csv.writer(json_data)
        count = 0
        for data in ohlc_data:
		if count == 0:
                	header = data.keys()
                	csvwriter.writerow(header)
                	count += 1
            	csvwriter.writerow(data.values())
        filename.close()