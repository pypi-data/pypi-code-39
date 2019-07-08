from pathlib import Path
import logging
import os
import urllib.parse as urlparse
import string
import datetime
import random
import shutil
import io
import json

import pandas as pd
import numpy as np
from PIL import Image
from tqdm.auto import tqdm

from scrapy.http import TextResponse
import aiohttp

from .captcha_solver import manual_captcha_solver
from .scraper_utils import _batch
from .scraper_utils import _check_valid_cookie

from .utils import user_data_dir
from .utils import download_file


class RIPScraper:

  root_url = "https://www.referendum.interieur.gouv.fr"

  def __init__(self,
               incapsula_cookie=None,
               captcha_solver="manual",
               max_captcha_try=20,
               max_request_try=20,
               consultation_uri="/consultation_publique/8/",
               shuffle_urls=True,
               save_dir=None,
               tqdm_to_logger=False):

    self.log = logging.getLogger('RIPScraper')
    self.log.setLevel(logging.INFO)
    self.tqdm_to_logger = tqdm_to_logger

    self.consultation_uri = consultation_uri
    self.consultation_url = urlparse.urljoin(self.root_url, consultation_uri)

    if incapsula_cookie:
      self.cookies = incapsula_cookie
    else:
      if "RIP_COUNTER_COOKIE_NAME" not in os.environ.keys() or "RIP_COUNTER_COOKIE_VALUE" not in os.environ.keys():
        url = "https://www.referendum.interieur.gouv.fr/consultation_publique/8"
        mess = "Incapsula cookie values are not set. Please set the ENV variables " \
            "RIP_COUNTER_COOKIE_NAME and RIP_COUNTER_COOKIE_VALUE.\n" \
            f"You can get a cookie by solving the ReCaptcha at: {url}"
        raise ValueError(mess)

      cookie_name = os.environ['RIP_COUNTER_COOKIE_NAME']
      cookie_value = os.environ['RIP_COUNTER_COOKIE_VALUE']
      self.cookies = {}
      self.cookies[cookie_name] = cookie_value

    if save_dir:
      self.save_dir = Path(save_dir)
    else:
      if "RIP_COUNTER_DATA_DIR" not in os.environ.keys():
        mess = "Env variable 'RIP_COUNTER_DATA_DIR' is not set. Please set it."
        raise ValueError(mess)
      self.save_dir = Path(os.environ['RIP_COUNTER_DATA_DIR'])

    # Generate all URLs: ['/A/AA', '/A/AB', ...]
    self.uris = [f"{l}/{l}{ll}" for l in string.ascii_uppercase for ll in string.ascii_uppercase]
    self.urls = [urlparse.urljoin(self.consultation_url, uri) for uri in self.uris]

    self.all_urls = {}
    self.all_urls_flat = []

    # Randomize URLs
    self.shuffle_urls = shuffle_urls
    if self.shuffle_urls:
      random.shuffle(self.urls)

    if captcha_solver == "manual":
      self.captcha_solver = manual_captcha_solver
    elif callable(captcha_solver):
      self.captcha_solver = captcha_solver
    else:
      raise ValueError(f"Invalid captcha solver: {captcha_solver}")

    self.max_captcha_try = max_captcha_try
    self.max_request_try = max_request_try

    self.total_captcha_counter = 0
    self.solved_captcha_counter = 0

    self.start_count_datetime = datetime.datetime.now()

    self.chunks_dir = self.save_dir / 'chunks'
    self.all_urls_path = self.save_dir / "all_urls.json"

    self.data_name = self.start_count_datetime.strftime("%Y-%m-%d")
    self.data_path = self.save_dir / f'{self.data_name}_data.csv'
    self.data_by_communes_path = self.save_dir / f'data_by_communes.csv'

  def get_captcha_solver_rate(self):
    return self.solved_captcha_counter / self.total_captcha_counter

  def log_captcha_solver_rate(self):
    """Log success rate of the captcha solver.
    """
    if self.total_captcha_counter > 0:
      rate = self.get_captcha_solver_rate()
      self.log.info(f'Current captcha solver success rate is: {rate * 100:.01f}%'
                    f' ({self.solved_captcha_counter}/{self.total_captcha_counter}).')

  def tqdm(self, iterable, **kwargs):
    # TODO: Make TqdmToLogger to work
    #if self.tqdm_to_logger:
    #  file = TqdmToLogger(self.log, level=logging.INFO)
    #else:
    #  file = None
    return tqdm(iterable, file=None, **kwargs)

  def _parse_table(self, response):
    table_raw = response.css('#formulaire_consultation_publique table.table').get()
    if not table_raw:
      return None
    return pd.read_html(table_raw)[0]

  async def make_request(self, method, url, session, data=None):
    attempt = 0
    req = None
    error = None
    while attempt < self.max_request_try:
      try:
        req = await session.request(method, url, data=data)
        break
      except aiohttp.ServerDisconnectedError as error:
        attempt += 1

    if not req:
      self.log.error(f"Error during request of {url}: {error}")

    return req

  async def _get_captcha_image(self, response, session):
    """Extract the captcha image and the captcha token from the page.
    """
    captcha = response.css('img#captcha').xpath('@src').get()
    if not captcha:
      return None

    # Get the token
    token = response.css('#form__token').xpath('@value').get()

    # Get the image captcha URL
    captcha_uri = response.css('img#captcha').xpath('@src').get()
    captcha_url = urlparse.urljoin(self.root_url, captcha_uri)

    # Download the image
    req = await self.make_request('get', captcha_url, session)
    if not req:
      return None
    req.raise_for_status()
    captcha_content = await req.read()
    captcha_image = Image.open(io.BytesIO(captcha_content))
    return captcha_image, token

  async def fetch_page_async(self, url, session):
    """Fetch one page. Bypass captcha if any is detected.
    """
    req = await self.make_request('get', url, session)
    if not req:
      return None

    req.raise_for_status()
    response = TextResponse(str(req.url), body=await req.text(), encoding='utf-8')

    for _ in range(self.max_captcha_try):

      _check_valid_cookie(response)

      # Get captcha image and token.
      captcha = await self._get_captcha_image(response, session)

      # If not captcha is detected, the request is a success
      # and we return the response.
      if not captcha:
        self.solved_captcha_counter += 1
        return response

      captcha_image, token = captcha

      # Solve the captcha.
      captcha_solution = self.captcha_solver(np.array(captcha_image))
      self.total_captcha_counter += 1

      # Send captcha solution.
      form_data = {}
      form_data['form[captcha]'] = captcha_solution
      form_data['form[_token]'] = token

      # Get the actual page.
      req = await self.make_request('post', url, session, data=form_data)
      if req:
        req.raise_for_status()
        response = TextResponse(str(req.url), body=await req.text(), encoding='utf-8')

    return None

  async def fetch_pages_async(self, urls, description="", show_progress=True):
    """Fetch multiple URLs in a async manner. The functions needs to be called with the
    `await` keyword.
    """
    async def _fn_async(urls):
      session_args = {}
      session_args['cookies'] = self.cookies
      async with aiohttp.ClientSession(**session_args) as session:
        responses = []
        for _, url in enumerate(self.tqdm(urls,
                                          desc=description,
                                          total=len(urls),
                                          disable=not show_progress)):
          task = self.fetch_page_async(url, session)
          responses.append(await task)
        return responses
    responses = await _fn_async(urls)

    # Log stats and failing URLs.
    failed_url_indices = [i for i, resp in enumerate(responses) if resp is None]
    failed_urls = [urls[idx] for idx in failed_url_indices]
    if failed_urls:
      self.log.error(f'The following URLs failed to be fetched: {failed_urls}')

    return responses

  async def get_all_urls(self, show_progress=True, _test_mode=False):
    """Retrieve a URLs of type: ['/A/AA/?page=1', '/A/AA/?page=2', ..., '/A/AB/?page=1', '/A/AB/?page=2', ...].

      - Fetch all the first pages of type ['/A/AA', '/A/AB', ...].
      - Parse the pagination to build a list of all the urls that contain data.
    """

    if self.all_urls_path.is_file():
      self.log.info(f"A JSON file with all urls has been found: {self.all_urls_path}. "
                    "All URLs will be loaded from this file. Delete it if you want to "
                    "scrap the URLs from scratch.")
      self.all_urls = json.load(open(self.all_urls_path))

    else:
      self.all_urls = {}

      url_list = self.urls
      if _test_mode:
        url_list = url_list[:5]

      description = "Scrap all URLs"
      responses = await self.fetch_pages_async(url_list,
                                               description=description,
                                               show_progress=show_progress)

      for url, response in zip(url_list, responses):

        if not response:
          continue

        # Use the URL to parse the letters we are at.
        url_path = urlparse.urlsplit(url).path
        two_letters = url_path.split('/')[-1]

        if response:
          selector = '#formulaire_consultation_publique .navigation .pagination span a'
          pagination_uris = response.css(selector).xpath('@href').getall()

          self.all_urls[two_letters] = []

          # We add page #1.
          self.all_urls[two_letters].append(url)

          url_obj = urlparse.urlsplit(url)

          if len(pagination_uris) > 1:
            # We use the alst pagination element
            # to get the number of pages.
            query = urlparse.urlsplit(pagination_uris[-1])
            n_pages = int(query.query.split('=')[-1])

            # We generate all the pages
            page_urls = [url_obj._replace(query=f'page={i}').geturl() for i in range(2, n_pages + 1)]
            self.all_urls[two_letters].extend(page_urls)

      # Save all urls
      with open(self.all_urls_path, 'w') as f:
        json.dump(self.all_urls, f, indent=2)

    # Flatten all urls
    self.all_urls_flat = [item for sublist in self.all_urls.values() for item in sublist]

    if self.shuffle_urls:
      random.shuffle(self.all_urls_flat)

    self.log.info(f"{len(self.all_urls_flat)} URLs have been found.")

  async def scrap_urls(self, url_list, description="", show_progress=True):
    responses = await self.fetch_pages_async(url_list,
                                             description=description,
                                             show_progress=show_progress)

    data = pd.DataFrame()

    desc = "Build CSV files for this batch."
    for url, response in self.tqdm(zip(url_list, responses), total=len(url_list), desc=desc):

      if not response:
        continue

      # Check if the page has  table.
      no_table_content = response.css('#formulaire_consultation_publique h2::text').get()
      if no_table_content and 'Aucun soutien' in no_table_content:
        continue

      table = self._parse_table(response)
      if table is None:
        self.log.error(f"The table can't be found in the HTML string: {response.text}")
        self.log.error(f"Table at {url} can't be parsed.")
        continue

      # Use the URL to parse the letters we are at.
      url_path = urlparse.urlsplit(url).path
      two_letters = url_path.split('/')[-1]

      try:
        table['commune'] = table['Localité de vote']
        table = table[['commune']]
        table['letter'] = two_letters
        table['start_count_datetime'] = self.start_count_datetime
        table['count_datetime'] = pd.to_datetime(datetime.datetime.now())

        # Get page index
        query = urlparse.urlsplit(url).query
        if query:
          page_id = int(query.split('=')[-1])
        else:
          page_id = 1
        table['page_id'] = page_id

      except Exception as e:
        self.log.error(f"Error while parsing the table from {url}: {e}")
        self.log.error(f"Table: \n{table}")

      if self.save_dir:
        fpath = self.chunks_dir / f'{two_letters}_page_{page_id:05d}.csv'
        table.to_csv(fpath, index=False)

      data = pd.concat([data, table], ignore_index=True)

    data = data.reset_index(drop=True)
    return data

  async def scrap(self, batch_size=64, show_progress=True, _test_mode=False):
    """Scrap and save all data to count votes.

    - Fetch all URLs by looking t the pagination HTML element of letter pages
      ['/A/AA/', '/A/AB/', ..., '/Z/ZZ/'].
    - Iterate over all URLs:
      - Fetch HTML page.
      - Parse the HTML table if any to a Pandas Dataframe.
      - Save the table as a CSV file in `save_dir + "/chunks"`.

    Args:
      - batch_size: int, the number of concurrent GET requests to do.
      - show_progress: bool, show progress bars during long steps.
      - _test_mode: bool, when enabled only scrap 5 pages for testing purposes.
    """

    self.log.info("Fetch all URLs of type ['/A/AA/?page=1', '/A/AA/?page=2', "
                  "..., '/A/AB/?page=1', '/A/AB/?page=2', ...]")
    await self.get_all_urls(_test_mode=_test_mode)

    self.log_captcha_solver_rate()

    url_list = self.all_urls_flat
    if _test_mode:
      url_list = url_list[:5]

    # Check if we can restore some chunk files.
    if self.chunks_dir.is_dir():
      n_chunk_files = len(list(self.chunks_dir.glob("*.csv")))
      if n_chunk_files > 0:
        mess = f"{n_chunk_files} chunk files found. Scraping will be restored from those chunk files."
        self.log.info(mess)

        chunk_paths = list(self.chunks_dir.glob("*.csv"))

        # Generate URLs to NOT scrap from the name of the CSV files.
        urls_to_not_scrap = []
        for chunk_path in chunk_paths:
          two_letters = chunk_path.stem.split('_')[0]
          page_index = int(chunk_path.stem.split('_')[-1])
          url = urlparse.urljoin(self.consultation_url, f"{two_letters[0]}/{two_letters}")
          if page_index > 1:
            url += f"?page={page_index}"
          urls_to_not_scrap.append(url)

        # Remove already scraped URLs from the list of URLs to scrap.
        new_url_list = []
        for url in url_list:
          if url not in urls_to_not_scrap:
            new_url_list.append(url)
        url_list = new_url_list

    batch_url_list = list(_batch(url_list, n=batch_size))

    self.log.info(f"Start counting votes with a batch size of {batch_size}.")
    self.log.info(f"{len(url_list)} URLs and {len(batch_url_list)} batches to process.")

    self.chunks_dir.mkdir(exist_ok=True)

    description = "Batch over all URLs"
    for i, batch_urls in enumerate(self.tqdm(batch_url_list[:],
                                             desc=description,
                                             total=len(batch_url_list),
                                             disable=not show_progress)):
      self.log.info(f"Scrap batch {i + 1}/{len(batch_url_list)}")
      if (i % 20) == 0:
        self.log_captcha_solver_rate()

      description = f"Batch {i + 1}/{len(batch_url_list)}"
      await self.scrap_urls(batch_urls, description=description, show_progress=show_progress)

    duration = datetime.datetime.now() - self.start_count_datetime
    self.log.info(f"Data collecton is done. It took {duration}")

    self.merge_chunks()

    # Remove chunks dir and all_urls file.
    shutil.rmtree(self.chunks_dir)
    self.all_urls_path.unlink()

  def merge_chunks(self):

    self.log.info("Merging all chunk files.")

    data = pd.DataFrame()

    chunk_paths = list(self.chunks_dir.glob("*.csv"))
    description = "Merge all CSV files"
    for chunk_path in self.tqdm(chunk_paths, desc=description, total=len(chunk_paths)):
      chunk = pd.read_csv(chunk_path)
      data = pd.concat([data, chunk], ignore_index=True)

    data = data.reset_index(drop=True)

    data.to_csv(self.data_path, index=False)

    self.log.info(f"Data saved at {self.data_path}")
    self.log.info(f"Number of votes: {len(data)}")

    master_data_path = self.save_dir / 'master_data.csv'
    if master_data_path.is_file():
      master_data = pd.read_csv(master_data_path)
    else:
      master_data = pd.DataFrame()

    df = {}
    df['name'] = self.data_name
    df['count_date_start'] = self.start_count_datetime
    df['count_date_end'] = datetime.datetime.now()
    df['vote_count'] = len(data)
    master_data = pd.concat([master_data, pd.DataFrame([df])])

    master_data.to_csv(master_data_path, index=False)

  def process_data(self):
    """Process collected data by matching each vote to a commune using INSEE dataset.
    """
    if not self.data_by_communes_path.is_file():
      # Download INSEE data about french cities.
      code_insee_url = "https://data.opendatasoft.com/explore/dataset/code-postal-code-insee-2015@public/download/?format=csv&use_labels_for_header=true"
      user_dir = user_data_dir(appname='rip-counter')
      code_insee_path = user_dir / 'code-postal-code-insee-2015@public.csv'
      download_file(code_insee_url, code_insee_path, progressbar=True)

      # Load INSEE code and do some cleaning on it.
      code = pd.read_csv(code_insee_path, sep=';')
      drop_cols = ['Geo Point', 'ID_GEOFLA', 'coordonnees_gps', 'Ligne_5', 'Code_postal']
      code = code.drop(drop_cols, axis=1)
      code['NOM_COM'] = code['NOM_COM'].str.replace(' ', '-')

      # Drop commune with multiples postal code.
      code = code.drop_duplicates(subset='INSEE_COM')

      # In INSEE dataset, mark communes as duplicated when they have homonyms.
      mask_duplicated = code['NOM_COM'].duplicated(keep=False)
      code['has_homonym'] = False
      code.loc[mask_duplicated, 'has_homonym'] = True

      commune_data = code
    else:
      commune_data = pd.read_csv(self.data_by_communes_path)

    if not self.data_path.is_file():
      self.log.error(f"Can't process because raw data does not exist at {self.data_path}.\n"
                     "Use `scraper.scrap()` to get the raw data.")
      return None

    data = pd.read_csv(self.data_path)

    # Clean scraped data
    data['commune'] = data['commune'].str.upper()
    data['commune'] = data['commune'].str.normalize('NFKD')
    data['commune'] = data['commune'].str.encode('ascii', errors='ignore')
    data['commune'] = data['commune'].str.decode('utf-8')
    data['commune'] = data['commune'].str.replace(' ', '-')

    # Replace NanN values by <UNKNOWN>
    data.loc[data['commune'].isna(), 'commune'] = '<UNKNOW>'

    data = data.reset_index(drop=True)

    # Count the number of votes for each communes in the scraped data.
    vote_count = data.groupby('commune').count()['page_id']

    vote_count_column_name = self.data_name

    # Add to the INSEE data the number of votes for each communes.
    def _count_fn(x): return vote_count.loc[x] if x in vote_count.index else 0
    commune_data[vote_count_column_name] = commune_data['NOM_COM'].apply(_count_fn)

    # For the homonyms communes we divide the number of votes for those communes
    # by the number of homonyms.
    # TODO: split number of votes proportionnaly to the population
    # of those communes.
    def _split_duplicated_vote_fn(x):
      return x[vote_count_column_name].iloc[0] / x[vote_count_column_name].count()
    duplicated_communes_average_vote_count = commune_data[commune_data['has_homonym']].groupby('NOM_COM').apply(_split_duplicated_vote_fn)
    items = list(duplicated_communes_average_vote_count.iteritems())
    for name, count in tqdm(items, total=len(items), desc="Detect homonym communes", leave=False):
      mask = commune_data['NOM_COM'] == name
      commune_data.loc[mask, vote_count_column_name] = count

    # Detect communes not in INSEE dataset.
    # TODO: this could be more efficient.
    liste_communes = commune_data['NOM_COM'].tolist()
    tqdm.pandas(desc='Detect communes absent from INSEE data', leave=False)
    mask = data['commune'].progress_apply(lambda x: x not in liste_communes)

    # Add extra communes to the dataset.
    extra_rows = data[mask].groupby('commune').count()['page_id']
    extra_rows = extra_rows.reset_index()
    extra_rows.columns = ['NOM_COM', vote_count_column_name]
    commune_data = pd.concat([commune_data, extra_rows], ignore_index=True, sort=False)
    commune_data = commune_data.reset_index(drop=True)

    # Check the difference of vote count before and after the processing.
    count_diff = commune_data[vote_count_column_name].sum() - data.shape[0]
    if count_diff != 0:
      self.log.error(f"There is a difference of counted vote before and after the processing of {count_diff}")

    # For the new (no INSEE) communes set `has_homonym` to False.
    commune_data.loc[commune_data['has_homonym'].isnull(), 'has_homonym'] = False

    # Save back processed data to `save_dir`.
    commune_data.to_csv(self.data_by_communes_path, index=False)
    self.log.info(f"Preprocessing done and data saved at {self.data_by_communes_path}")

    return commune_data
