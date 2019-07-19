from __future__ import division

import numpy as np
import csv
import os
from os.path import join
import shutil
import pkg_resources
from data_utils.os_utils import create_dir
from utils import get_color_from_intensity, get_color_from_coors, get_color_from_height, create_dir, coors_normalize





class ThreejsConverter(object):
    def __init__(self, home, from_height=True, height_axis='z'):
        self.home = home
        self.from_height = from_height
        self.height_axis = height_axis
        self.cwd = os.getcwd()
        self.html_template = join(self.cwd, '../threejs/src/template.html')
        self.task_name = 'default'
        self.axis_dict = {'x': 0, 'y': 1, 'z': 2}
        assert height_axis in self.axis_dict.keys()
        if self.height_axis == 'x':
            self.axis_x = self.axis_dict['y']
            self.axis_y = self.axis_dict['x']
            self.axis_z = self.axis_dict['z']
        elif self.height_axis == 'y':
            self.axis_x = self.axis_dict['x']
            self.axis_y = self.axis_dict['y']
            self.axis_z = self.axis_dict['z']
        else:
            self.axis_x = self.axis_dict['x']
            self.axis_y = self.axis_dict['z']
            self.axis_z = self.axis_dict['y']
        create_dir(self.home, clean=False)
        create_dir(join(self.home, 'data'), clean=False)
        create_dir(join(self.home, 'html'), clean=False)
        try:
            shutil.copy(pkg_resources.resource_filename('threejs-test', 'src'), join(self.home, 'src'))
        except:
            pass

    def convert_pc_csv(self, task_name, coors, default_rgb, intensity):
        coors = coors_normalize(coors)
        if default_rgb is not None:
            assert len(coors) == len(default_rgb)
            rgb = default_rgb
        elif intensity is not None:
            assert len(coors) == len(intensity)
            rgb = get_color_from_intensity(intensity)
        elif self.from_height:
            rgb = get_color_from_height(coors, axis=self.axis_dict[self.height_axis])
        else:
            rgb = get_color_from_coors(coors)

        head = ['x', 'y', 'z', 'r', 'g', 'b']
        output_csv = join(self.home, 'data', '{}.csv'.format(task_name))

        with open(output_csv, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=head)
            writer.writeheader()
            for i in range(len(coors)):
                x = coors[i, self.axis_x]
                y = coors[i, self.axis_y]
                z = coors[i, self.axis_z]
                r = rgb[i, 0]
                g = rgb[i, 1]
                b = rgb[i, 2]
                writer.writerow({'x': x, 'y': y, 'z': z, 'r': r, 'g': g, 'b': b})

    def compile(self, task_name, coors, default_rgb=None, intensity=None, bbox=None):
        self.convert_pc_csv(task_name, coors, default_rgb, intensity)
        os.system("sed 's/INPUT_PC_CSV/{}/'  ".format(task_name + '.csv') +
                  "{} > ".format(join(self.home, 'src', 'template.html')) +
                  "{}".format(join(self.home, 'html', task_name + '.html')))





if __name__ == '__main__':
    import pickle
    frame_id = 2

    point_cloud_frames = np.load('/media/data1/detection/dataset/training_pc.npy')
    point_cloud = point_cloud_frames[frame_id]
    coors = point_cloud[:, :3]
    intensity = point_cloud[:, 3]
    rgbs = point_cloud[:, -3:]
    Converter = ThreejsConverter(home='/media/data1/threejs', from_height=True)
    Converter.compile(task_name='test', coors=coors, default_rgb=rgbs)
