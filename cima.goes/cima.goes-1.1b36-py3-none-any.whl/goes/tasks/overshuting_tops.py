import os
from cima.goes.gcs import get_datasets, band
from cima.goes.gcs import close_datasets
from cima.goes.tiles import load_tiles, get_data, get_lats_lons, vis_correction
from cima.goes.img import save_image, get_SMN_palette
from cima.goes.utils import get_usage


def vis_ir_images(images_path, year, day_of_year, hour, tiles):
    datasets = get_datasets(year, day_of_year, hour, [band.RED, band.CLEAN_LONGWAVE_WINDOW])
    for ds in datasets:
        for tile_number in map(str, range(len(tiles.RED.keys()))):
            filepath_prefix = os.path.join(images_path, f'{ds.start[:4]}/{ds.start[4:7]}/{ds.start}')
            print(filepath_prefix, tile_number)
            print(get_usage())

            lats, lons = get_lats_lons(ds.RED, tiles.RED[tile_number])
            data = get_data(ds.RED, tiles.RED[tile_number])
            gray = vis_correction(data)
            save_image(gray,
                       f'{filepath_prefix}_{tile_number}_vis',
                       tiles.RED[tile_number],
                       lats, lons)

            lats, lons = get_lats_lons(ds.CLEAN_LONGWAVE_WINDOW, tiles.CLEAN_LONGWAVE_WINDOW[tile_number])
            data = get_data(ds.CLEAN_LONGWAVE_WINDOW, tiles.CLEAN_LONGWAVE_WINDOW[tile_number])
            ir = data - 273
            save_image(ir,
                       f'{filepath_prefix}_{tile_number}_ir',
                       tiles.CLEAN_LONGWAVE_WINDOW[tile_number],
                       lats, lons,
                       cmap=get_SMN_palette(),
                       vmin=-90, vmax=50)
        close_datasets(ds)

    return f'end of {year} {day_of_year} {hour}'
