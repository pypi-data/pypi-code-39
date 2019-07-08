from PIL import Image
from glob import glob
from tqdm import tqdm
import os

def clean(path):
    loss = 0
    print("Cleaning data...")
    data = glob(str(path))

    for image in tqdm(data):
        try:
            img = Image.open(image)
        except OSError:
            loss += 1
            os.system(str("sudo rm "+str(image)))
    print("Data Cleaned, loss = "+str(loss))
