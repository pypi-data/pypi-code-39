from tqdm import tqdm
from bs4 import BeautifulSoup
from shutil import copyfile
from urllib.parse import urljoin
from urllib.request import urlretrieve
from .exceptions import ThUraException
import requests
import os

class ThUra(object):

    def threads_all(self, sort=None, x=20, y=10, l=4, thumbnail_size=6):
        url = "https://dec.2chan.net/55/futaba.php"
        params = {'mode': 'cat', 'sort': sort}
        cookies = {'cxyl': '{}x{}x{}x0x{}'.format(x, y, l, thumbnail_size)}
        threads = []

        r = requests.get(url, params=params, cookies=cookies)
        self._errorCheck(r.status_code)

        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('table', id='cattable')
        tds = table.find_all('td')

        for td in tds:
            url = urljoin("https://dec.2chan.net/55/", td.find('a')['href'])
            title = td.find('small').get_text()
            thumbnail = urljoin("https://dec.2chan.net/", td.find('img')['src'])
            comments = td.find('font').get_text()
            threads.append({
                'url': url,
                'title': title,
                'thumbnail': thumbnail,
                'comments_total': comments,
            })

        return threads

    def _errorCheck(self, status_code):
        if status_code != 200:
            if status_code == 404:
                raise ThUraException('Thread does not exist')
            else:
                raise ThUraException('Something went wrong.')

    def get_thread_images(self, id):
        url = "https://dec.2chan.net/55/res/{}.htm".format(id)

        r = requests.get(url)
        self._errorCheck(r.status_code)

        soup = BeautifulSoup(r.text, 'html.parser')
        imgs = soup.select_one('.thre').find_all('img')
        sources = [urljoin("https://dec.2chan.net/", img.parent['href']) for img in imgs if img.parent.name == 'a']

        return sources

    def download_images(self, id, directory=None, custom=False):
        if directory is None:
            directory = os.path.expanduser("~/Desktop/touhou_ura/images/{}".format(id))
        else:
            if custom == False:
                directory = "{}/touhou_ura/images/{}".format(directory, id)

        sources = self.get_thread_images(id)
        os.makedirs(directory, exist_ok=True)

        for source in tqdm(sources, desc="Downloading"):
            urlretrieve(source, '{}/{}'.format(directory, os.path.basename(source)))

    def download_archive(self, id, directory=None, custom=False):
        url = "https://dec.2chan.net/55/res/{}.htm".format(id)

        if directory is None:
            directory = os.path.expanduser("~/Desktop/touhou_ura/archives/{}".format(id))
        else:
            if custom == False:
                directory = "{}/touhou_ura/archives/{}".format(directory, id)

        r = requests.get(url)
        self._errorCheck(r.status_code)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        thread = soup.select_one('.thre')

        os.makedirs(directory, exist_ok=True)
        cur_path = os.path.dirname(os.path.abspath(__file__))

        copyfile('{}/style4.css'.format(cur_path), '{}/style4.css'.format(directory))
        self.download_images(id, '{}/images'.format(directory), custom=True)

        with open('{}/main.html'.format(cur_path)) as html:
            thread_html = BeautifulSoup(html, 'html.parser')
            thread_html.body.append(thread)
            for i, img in enumerate(thread.find_all('img')):
                filenames = [filename for filename in os.listdir('{}/images'.format(directory))]
                new_src = img['src'].replace(img['src'], 'images/{}'.format(os.path.basename(filenames[i])))
                img['src'] = new_src


        with open('{}/{}'.format(directory, '{}.html'.format(id)), 'wb+') as f:
            f.write(thread_html.encode('utf-8'))

        


        
        