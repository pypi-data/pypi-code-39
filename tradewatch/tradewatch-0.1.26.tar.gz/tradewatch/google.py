import sys, requests, json

api_url = 'https://www.googleapis.com/customsearch/v1/siterestrict'
def search_gsce(q,cred):
	try:
		return json.loads(requests.get(api_url,params={"cx":cred['cx'],"key":cred['key'],"q":q}).text)
	except Exception:
		return None
if __name__ == "__main__":
	if len(sys.argv)>=2:
		q=sys.argv[1]
		print(json.dumps(search_gsce(q)))
	else:
		print(json.dumps({"code":404,"message":"Provide search param for Allegro.pl"}))
