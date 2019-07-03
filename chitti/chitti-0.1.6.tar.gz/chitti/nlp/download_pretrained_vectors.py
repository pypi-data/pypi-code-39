
import os

import pandas as pd
from progressbar import Bar, ETA, FileTransferSpeed, ProgressBar, Percentage, RotatingMarker
from six.moves.urllib.request import urlretrieve
import zipfile

def load_datasets(path=os.path.join(os.path.dirname(__file__), 'data/pretrained_embeddings_web_urls.csv')):
    datasets = pd.read_csv(path)
    return datasets

def unzip_file(path_to_zip_file, dir):
    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    zip_ref.extractall(dir)
    zip_ref.close()

def download(number=-1, name="", save_dir='./'):
    """Download pre-trained word vector
    :param number: integer, default ``None``
    :param save_dir: str, default './'
    :return: file path for downloaded file
    """
    df = load_datasets()

    if number > -1:
        row = df.iloc[[number]]
    elif name:
        row = df.loc[df["Name"] == name]

    url = ''.join(row.URL)
    if not url:
        print('The word vector you specified was not found. Please specify correct name.')

    widgets = ['Test: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets)

    def dlProgress(count, blockSize, totalSize):
        if pbar.maxval is None:
            pbar.maxval = totalSize
            pbar.start()

        pbar.update(min(count * blockSize, totalSize))

    file_name = url.split('/')[-1]
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, file_name)
    if os.path.exists(save_path):
        return save_path

    path, _ = urlretrieve(url, save_path, reporthook=dlProgress)
    pbar.finish()
    unzip_file(path, save_dir)
    return path
