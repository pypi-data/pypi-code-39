import requests

url = 'https://rfabbri.linked.data.world/sparql/linked-open-social-data'

prefix = 'PREFIX po: <http://purl.org/socialparticipation/po/>\n'

def query(q, verbose=False):
    q_ = prefix + q
    r = requests.post(url=url, data={'query': q_}, timeout=1000000)
    r_ = r.json()
    if verbose:
        print('done query:\n', q, 'res:', r_)
    return r_
