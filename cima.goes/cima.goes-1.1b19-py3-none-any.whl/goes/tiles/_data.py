import os
import json
import cv2
from collections import namedtuple
from dataclasses import dataclass
import pyproj
try:
    import cupy as cp
    import numpy as np
    asnumpy = cp.asnumpy
except:
    import numpy as np
    # import numpy as cp
    asnumpy = lambda x: x


FORTRAN_ORDER = 'F'
LOCAL_BASE_PATH = os.path.dirname(os.path.abspath(__file__))


@dataclass
class Tile:
    extent: list
    min_x: float = None
    max_x: float = None
    min_y: float = None
    max_y: float = None


def generate_tiles_extent(
        lats_from=-45,
        lats_to=-20,
        lons_from=-75,
        lons_to=-45,
        step=5,
        overlap=1.5):
    tiles = {}
    lats = [x for x in range(lats_from, lats_to, step)]
    lons = [x for x in range(lons_from, lons_to, step)]
    tiles_coordinates = [(lon, lon + step, lat, lat + step) for lat in lats for lon in lons]
    for index, coord in enumerate(tiles_coordinates):
        tiles[str(index)] = Tile(extent=[
                    coord[0] - overlap,
                    coord[1] + overlap,
                    coord[2] - overlap,
                    coord[3] + overlap,
                ])
    return tiles


def nearest_indexes(lat, lon, lats, lons, major_order):
    distance = (lat-lats)*(lat-lats) + (lon-lons)*(lon-lons)
    return np.unravel_index(np.argmin(distance), lats.shape, major_order)


def find_indexes(tile, lats, lons, major_order):
    lon1, lon2, lat1, lat2 = tile.extent

    x1, y1 = nearest_indexes(lat1, lon1, lats, lons, major_order)
    x2, y2 = nearest_indexes(lat1, lon2, lats, lons, major_order)
    x3, y3 = nearest_indexes(lat2, lon1, lats, lons, major_order)
    x4, y4 = nearest_indexes(lat2, lon2, lats, lons, major_order)

    tile.min_x = min(x1, x2, x3, x4)
    tile.max_x = max(x1, x2, x3, x4)
    tile.min_y = min(y1, y2, y3, y4)
    tile.max_y = max(y1, y2, y3, y4)


def add_indexes(tiles, lats, lons, order):
    for index, tile in tiles.items():
        find_indexes(tile, lats, lons, order)


def generate_tiles(dataset):
    major_order = FORTRAN_ORDER
    tiles = generate_tiles_extent()
    lats, lons = get_lats_lons(dataset)
    add_indexes(tiles, lats, lons, major_order)
    return tiles


def get_lats_lons(dataset, tile: Tile):
    sat_height = dataset['goes_imager_projection'].perspective_point_height
    sat_lon = dataset['goes_imager_projection'].longitude_of_projection_origin
    sat_sweep = dataset['goes_imager_projection'].sweep_angle_axis
    projection = pyproj.Proj(proj='geos', h=sat_height, lon_0=sat_lon, sweep=sat_sweep)
    x = dataset['x'][tile.min_x : tile.max_x] * sat_height
    y = dataset['y'][tile.min_y : tile.max_y] * sat_height
    XX, YY = np.meshgrid(np.array(x), np.array(y))
    lons, lats = projection(asnumpy(XX), asnumpy(YY), inverse=True)
    # del x, y, XX, YY
    return np.array(lats),  np.array(lons)


def resize(image, new_size):
  return cv2.resize(image, dsize=new_size, interpolation=cv2.INTER_CUBIC)


def vis_correction(image):
    image = np.clip(image, 0, 1)
    # gamma = 2.2
    # return np.power(image, 1 / gamma)
    return image


def ir_correction(image):
    image = np.clip(image, 0, 1)
    gamma = 2.2
    return np.power(image, 1 / gamma)


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


def save_tiles_to_file(filepath, tiles):
    tiles_dict = {}
    for band, v in tiles.items():
        tiles_dict[band] = {}
        for tile_number, tile_data in v.items():
            tiles_dict[band][tile_number] = {
                'extent': tile_data.extent,
                'min_x': tile_data.min_x,
                'max_x': tile_data.max_x,
                'min_y': tile_data.min_y,
                'max_y': tile_data.max_y,
            }
    with open(filepath, 'w') as f:
        f.write(json.dumps(tiles_dict, indent=2))


def load_tiles(filepath=os.path.join(LOCAL_BASE_PATH, 'default_tiles.json')):
    tiles = {}
    with open(filepath) as f:
        tiles_dict = json.load(f)
        Tiles = namedtuple('Tiles', [k for k, _ in tiles_dict.items()])
        for band, v in tiles_dict.items():
            tiles[band] = {}
            for tile_number, tile_data in v.items():
                tiles[band][tile_number] = Tile(**tile_data)
        tiles_object = Tiles(**tiles)
    return tiles_object
