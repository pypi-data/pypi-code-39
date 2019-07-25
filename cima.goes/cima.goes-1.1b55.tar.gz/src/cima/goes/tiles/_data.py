import os
import cv2
from cima.goes.tiles._tiles import Tile
try:
    import cupy as cp
    import numpy as np
    asnumpy = cp.asnumpy
except:
    import numpy as np
    # import numpy as cp
    asnumpy = lambda x: x


def resize(image, new_size):
  return cv2.resize(image, dsize=new_size, interpolation=cv2.INTER_CUBIC)


def vis_correction(image):
    image = np.clip(image, 0, 1)
    # gamma = 2.2
    # return np.power(image, 1 / gamma)
    return np.sqrt(image)


def compose_RGB(dataset_R, dataset_G, dataset_B, tile_R: Tile, tile_G: Tile, tile_B: Tile):
    R_size = (tile_R.max_x - tile_R.min_x, tile_R.max_y - tile_R.min_y)
    R = dataset_R.variables['CMI'][tile_R.min_y : tile_R.max_y, tile_R.min_x : tile_R.max_x]
    G = dataset_G.variables['CMI'][tile_G.min_y : tile_G.max_y, tile_G.min_x : tile_G.max_x]
    B = dataset_B.variables['CMI'][tile_B.min_y : tile_B.max_y, tile_B.min_x : tile_B.max_x]

    # Apply range limits for each channel. RGB values must be between 0 and 1
    R = np.clip(R, 0, 1)
    G = np.clip(G, 0, 1)
    B = np.clip(B, 0, 1)

    # Apply a gamma correction to the image to correct ABI detector brightness
    gamma = 2.2
    R = np.power(R, 1 / gamma)
    G = np.power(G, 1 / gamma)
    B = np.power(B, 1 / gamma)

    # Calculate the "True" Green
    G_resized = resize(G, R_size)
    B_resized = resize(B, R_size)
    #     G_true = 0.45 * R + 0.1 * G_resized + 0.45 * B_resized
    G_true = 0.48358168 * R + 0.45706946 * B_resized + 0.06038137 * G_resized
    G_true = np.clip(G_true, 0, 1)  # apply limits again, just in case

    RGB = np.dstack([R, G_true, B_resized])

    return R, RGB


def get_data(dataset, tile: Tile):
    return dataset.variables['CMI'][tile.min_y : tile.max_y, tile.min_x : tile.max_x]
