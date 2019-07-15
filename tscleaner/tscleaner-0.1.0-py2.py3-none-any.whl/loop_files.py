import os
from tqdm import tqdm
from tscleaner.figure_plotter import process


def process_all():
    path_data = 'C:/src/paper-global-reservoirs/data/time_series/'
    path_figure = 'C:/src/time_series_figures_removed_values/'

    single_file = 'water_area_62847.geojson.json'
    single_file_2 = 'water_area_62474.geojson.json'
    single_file_3 = 'water_area_62259.geojson.json'

    i = 0
    i_max = 500
    redo_figures = True

    with tqdm(total=i_max) as pbar:
        for file in os.listdir(path_data):
            process(file, path_data, path_figure, redo_figures)

            i += 1
            pbar.update(1)

            if i >= i_max:
                break

    process(single_file, path_data, path_figure, redo_figures)
    process(single_file_2, path_data, path_figure, redo_figures)
    process(single_file_3, path_data, path_figure, redo_figures)
