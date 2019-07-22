from cima.goes.gcs import set_credentials
from cima.goes.gcs import get_datasets, band
from cima.goes.utils import timeit
from cima.goes.tiles import load_tiles, get_data, get_lats_lons, compose_RGB
from cima.goes.img import plot
import numpy as np
set_credentials('/Users/fido/projects/cima/Categoriza/generate_images/goes_cloud_storage/credentials.json')


tiles = load_tiles()
tile_number = str(8)

@timeit
def all():
  datasets = get_datasets(2018, 50, 15, [band.RED, band.VEGGIE, band.BLUE])
  for ds in datasets:

      gray, RGB = compose_RGB(ds.RED, ds.VEGGIE, ds.BLUE,
                              tiles.RED[tile_number],
                              tiles.VEGGIE[tile_number],
                              tiles.BLUE[tile_number])

      lons, lats = get_lats_lons(ds.RED, tiles.RED[tile_number])
      # data = get_data(ds.RED, tiles.RED[tile_number])
      # plot(data, tiles.RED[tile_number], lons, lats)
      plot(gray, RGB, tiles.RED[tile_number], lons, lats)

all()

