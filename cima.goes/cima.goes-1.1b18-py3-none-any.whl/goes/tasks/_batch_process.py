import os
import asyncio
import time
import psutil
import gc
import concurrent.futures
from cima.goes.gcs import get_datasets, band
from cima.goes.gcs import close_datasets
from cima.goes.tiles import load_tiles, get_data, get_lats_lons, vis_correction
from cima.goes.img import save_image, get_SMN_palette


def _save_one_hour_OTs_images(images_path, year, day_of_year, hour):
    tiles = load_tiles()
    datasets = get_datasets(year, day_of_year, hour, [band.RED, band.CLEAN_LONGWAVE_WINDOW])
    for ds in datasets:
        for tile_number in map(str, range(len(tiles.RED.keys()))):
            filepath_prefix = os.path.join(images_path, f'{ds.start[:4]}/{ds.start[4:7]}/{ds.start}')
            print(filepath_prefix, tile_number)
            print(get_usage())

            lats, lons = get_lats_lons(ds.RED, tiles.RED[tile_number])
            data = get_data(ds.RED, tiles.RED[tile_number])
            gray = vis_correction(data)
            # save_image(gray,
            #            f'{filepath_prefix}_{tile_number}_vis',
            #            tiles.RED[tile_number],
            #            lats, lons)

            lats, lons = get_lats_lons(ds.CLEAN_LONGWAVE_WINDOW, tiles.CLEAN_LONGWAVE_WINDOW[tile_number])
            data = get_data(ds.CLEAN_LONGWAVE_WINDOW, tiles.CLEAN_LONGWAVE_WINDOW[tile_number])
            ir = data - 273
            # save_image(ir,
            #            f'{filepath_prefix}_{tile_number}_ir',
            #            tiles.CLEAN_LONGWAVE_WINDOW[tile_number],
            #            lats, lons,
            #            cmap=get_SMN_palette(),
            #            vmin=-90, vmax=50)
        close_datasets(ds)

    return f'end of {year} {day_of_year} {hour}'


async def _save_OTs_images(images_path, hours_list):
    with concurrent.futures.ProcessPoolExecutor(max_workers=len(hours_list)) as executor:
        futures = {executor.submit(_save_one_hour_OTs_images, images_path, *hour) for hour in hours_list}
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            print(data)


def get_usage():
    cpu = psutil.cpu_percent()
    # gives an object with many fields
    memory = psutil.virtual_memory()
    # you can convert that object to a dictionary
    return {'CPU%': cpu, "free GB": memory.free >> 30}


def save_OTs_images(images_path, hours_list):
    _start = time.time()
    loop = asyncio.get_event_loop()
    try:
        future = asyncio.ensure_future(_save_OTs_images(images_path, hours_list))
        loop.run_until_complete(future)
        print(f"Execution time: { time.time() - _start }")
    finally:
        loop.close()


# from cima.goes.gcs import mount_colab, set_credentials
# set_credentials('/Users/fido/projects/cima/Categoriza/generate_images/goes_cloud_storage/credentials.json')
# save_OTs_images('./downloads', [[2018, 53, 15]])