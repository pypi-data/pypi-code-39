import requests, json, csv

#Gathers price data for a given symbol year to date from January 1, 2000
def get_data(symbol):
	endpoint = r"https://api.tdameritrade.com/v1/marketdata/{}/pricehistory?apikey=STYKNHGHRVODHDGAGPRTASY0QGZGKLUC&periodType=ytd&frequencyType=daily&startDate=946720800000".format(str(symbol))
	content  = requests.get(url = endpoint)
	data     = content.json
	return data