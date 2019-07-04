import os, sys, requests, json
from selectolax.parser import HTMLParser

import tradewatch
def follow_link(link):
	lax=HTMLParser(requests.get(link).text)

	for selector in ["article h2 a",".app-container h1 a",".carousel-item a"]:

		if not title:
			if lax.css_first(selector):
				a=lax.css_first(selector)
				title=a.text()
				the_selector=selector
				href=a.attributes['href']
				if not "allegro" in href:
					prefix= "http://archiwum.allegro.pl" if "archiwum" in link else "http://allegro.pl"
					href=prefix+href
					return follow_link(href)
				atts=tradewatch.get_atts(link=href)
			else:
				title=""
				href=""
				atts={}
	return {"title":title,"href":href,"atts":atts}
def get_aukcja(name,category="",cred=None):
	title=""
	the_selector=""
	error={"title":"","href":"","atts":{}}
	q="{} {}".format(name,category) if category else name
	res=tradewatch.google.search_gsce(q,cred)
	if not "items" in res.keys():
		
		return error
	if category:
		items=list(filter(lambda item: "listitem" in item["pagemap"].keys(),res['items']))
		items=list(filter(lambda item: category in list(map(lambda i: i['name'].lower() if "name" in i else "",item['pagemap']['listitem'])),items))
		if not items:
			items=res['items']
	else:
		items=res['items']

	if not items:

		return {}
	else:
		link = items[0]['link']

	return follow_link(link)
get_item=get_aukcja
if __name__=="__main__":
	full="-f" in sys.argv[-1] or "-full" in sys.argv[-1]
	res=get_aukcja(sys.argv[1] if len(sys.argv)>=2 else "BRB Lalka",sys.argv[2] if len(sys.argv)>=3 and sys.argv[2][0]!='-' else "Dziecko")
	if full:
		print(json.dumps(res))
	else:
		print(res['title'])
