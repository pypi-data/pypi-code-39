import os
import json
import pyproj
from typing import Dict
from dataclasses import dataclass, make_dataclass, asdict
from cima.goes.gcs import get_blobs, get_dataset_from_blob
from cima.goes import Bands
try:
    import cupy as cp
    import numpy as np
    asnumpy = cp.asnumpy
except:
    import numpy as np
    # import numpy as cp
    asnumpy = lambda x: x


FORTRAN_ORDER = 'F'


@dataclass
class Tile:
    extent: list
    min_x: int = None
    max_x: int = None
    min_y: int = None
    max_y: int = None


@dataclass
class BandsTiles:
    BLUE: Dict[str, Tile] = None
    RED: Dict[str, Tile] = None
    VEGGIE: Dict[str, Tile] = None
    CIRRUS: Dict[str, Tile] = None
    SNOW_ICE: Dict[str, Tile] = None
    CLOUD_PARTICLE_SIZE: Dict[str, Tile] = None
    SHORTWAVE_WINDOW: Dict[str, Tile] = None
    UPPER_LEVEL_TROPOSPHERIC_WATER_VAPOR: Dict[str, Tile] = None
    MID_LEVEL_TROPOSPHERIC_WATER_VAPOR: Dict[str, Tile] = None
    LOWER_LEVEL_WATER_VAPOR: Dict[str, Tile] = None
    CLOUD_TOP_PHASE: Dict[str, Tile] = None
    OZONE: Dict[str, Tile] = None
    CLEAN_LONGWAVE_WINDOW: Dict[str, Tile] = None
    IR_LONGWAVE_WINDOW: Dict[str, Tile] = None
    DIRTY_LONGWAVE_WINDOW: Dict[str, Tile] = None
    CO2_LONGWAVE_INFRARED: Dict[str, Tile] = None


def generate_tiles(bands: Bands,
        lats_from=-45,
        lats_to=-20,
        lons_from=-75,
        lons_to=-45,
        step=5,
        overlap=1.5) -> BandsTiles:
    def new_tiles():
        return _get_tiles_one_band(
            lats_from=lats_from,
            lats_to=lats_to,
            lons_from=lons_from,
            lons_to=lons_to,
            step=step,
            overlap=overlap)
    bands_tiles: BandsTiles = BandsTiles()
    blobs = get_blobs(2018, 360, 12, bands)
    for band in bands:
        dataset = get_dataset_from_blob(getattr(blobs[0], band.name))
        tiles = new_tiles()
        tiles = _add_indexes_for_dataset(dataset, tiles)
        setattr(bands_tiles, band.name, tiles)
    return bands_tiles


def save_tiles(filepath: str, tiles: BandsTiles):
    dirpath = os.path.dirname(os.path.abspath(filepath))
    if not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(json.dumps(asdict(tiles), indent=2))


def load_tiles(filepath) -> BandsTiles:
    tiles = {}
    with open(filepath) as f:
        tiles_dict = json.load(f)
        bands_tiles: BandsTiles = BandsTiles()
        for band, v in tiles_dict.items():
            if v is not None:
                setattr(bands_tiles, band, {})
                for tile_number, tile_data in v.items():
                    getattr(bands_tiles, band)[tile_number] = Tile(**tile_data)
    return bands_tiles


def get_lats_lons(dataset, tile: Tile = None):
    sat_height = dataset['goes_imager_projection'].perspective_point_height
    sat_lon = dataset['goes_imager_projection'].longitude_of_projection_origin
    sat_sweep = dataset['goes_imager_projection'].sweep_angle_axis
    projection = pyproj.Proj(proj='geos', h=sat_height, lon_0=sat_lon, sweep=sat_sweep)
    if tile is None:
        x = dataset['x'][:] * sat_height
        y = dataset['y'][:] * sat_height
    else:
        x = dataset['x'][tile.min_x : tile.max_x] * sat_height
        y = dataset['y'][tile.min_y : tile.max_y] * sat_height
    XX, YY = np.meshgrid(np.array(x), np.array(y))
    lons, lats = projection(asnumpy(XX), asnumpy(YY), inverse=True)
    # del x, y, XX, YY
    return np.array(lats),  np.array(lons)


def _get_tiles_one_band(lats_from, lats_to, lons_from, lons_to, step, overlap):
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


def _add_indexes_for_dataset(dataset, tiles):
    major_order = FORTRAN_ORDER
    lats, lons = get_lats_lons(dataset)
    _add_indexes(tiles, lats, lons, major_order)
    return tiles


def _nearest_indexes(lat, lon, lats, lons, major_order):
    distance = (lat-lats)*(lat-lats) + (lon-lons)*(lon-lons)
    return np.unravel_index(np.argmin(distance), lats.shape, major_order)


def _find_indexes(tile: Tile, lats, lons, major_order):
    lon1, lon2, lat1, lat2 = tile.extent

    x1, y1 = _nearest_indexes(lat1, lon1, lats, lons, major_order)
    x2, y2 = _nearest_indexes(lat1, lon2, lats, lons, major_order)
    x3, y3 = _nearest_indexes(lat2, lon1, lats, lons, major_order)
    x4, y4 = _nearest_indexes(lat2, lon2, lats, lons, major_order)

    tile.min_x = int(min(x1, x2, x3, x4))
    tile.max_x = int(max(x1, x2, x3, x4))
    tile.min_y = int(min(y1, y2, y3, y4))
    tile.max_y = int(max(y1, y2, y3, y4))


def _add_indexes(tiles, lats, lons, order):
    for index, tile in tiles.items():
        _find_indexes(tile, lats, lons, order)
