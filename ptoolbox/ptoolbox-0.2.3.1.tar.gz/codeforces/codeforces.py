import requests
from bs4 import BeautifulSoup


class Codeforces:
    def __init__(self):
        self.s = requests.session()
        self._headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        }

    def get_problem_list(self, page_number):
        url = f'https://codeforces.com/problemset/page/{page_number}'

        headers = copy.deepcopy(self._headers)
        r = self.s.get(url, headers=headers)

        raw = r.text
        # print(raw)

        # problem = self.parse_problem(raw)

        return raw