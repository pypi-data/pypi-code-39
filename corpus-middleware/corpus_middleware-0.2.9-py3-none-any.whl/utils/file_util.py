#!/usr/bin/env python
# -*- coding: utf-8 -*-
import aiofiles
import os
import csv
from tqdm import tqdm


class FileUtil:

    @staticmethod
    def path_join(root, file):
        return os.path.join(root, file)

    @staticmethod
    def list_dir(file_path):
        files = []
        try:
            dir_list = os.listdir(file_path)
            for cur_file in dir_list:
                path = os.path.join(file_path, cur_file)
                if os.path.isdir(path):
                    next_folder_files, next_folder_status = FileUtil.list_dir(path)
                    if len(next_folder_files) != 0 and next_folder_status != 201:
                        files.extend(next_folder_files)
                elif os.path.isfile(path):
                    files.append(cur_file)
        except FileNotFoundError as e:
            print(e)
        return files

    @staticmethod
    def check_directory_exist(path):
        if os.path.exists(path) and os.path.isdir(path):
            return True
        else:
            return False

    @staticmethod
    def fill_the_full_path(path):
        if FileUtil.check_directory_exist(path) is False:
            os.makedirs(path)

    @staticmethod
    def path_join_for_cache_path(cache_directory, sub_directory, project_name):
        cache_path = FileUtil.path_join(cache_directory, project_name + '/')
        if sub_directory is not None and sub_directory.strip() != "":
            cache_path = FileUtil.path_join(cache_path, sub_directory + '/')
        return cache_path

    @staticmethod
    async def file_upload_sender(file_path):
        try:
            with tqdm(desc='文件上传进度', unit="b", unit_scale=True, total=os.path.getsize(file_path)) as upload_bar:
                async with aiofiles.open(file_path, 'rb') as f:
                    chunk = await f.read(64 * 1024)
                    while chunk:
                        yield chunk
                        chunk = await f.read(64 * 1024)
                        upload_bar.update(len(chunk))
        except KeyboardInterrupt:
            upload_bar.close()
            raise
        upload_bar.close()

    @staticmethod
    def check_cache_file_for_file(cache_directory, pre_check_file_name):
        is_exit = False
        if FileUtil.check_directory_exist(cache_directory) is False:
            return is_exit
        # 检查请求的文件是否存在于缓存文件夹内
        files = FileUtil.list_dir(cache_directory)
        for file in files:
            file_path = FileUtil.path_join(cache_directory, file)
            file_name = os.path.basename(file_path)
            if file_name == pre_check_file_name:
                is_exit = True
                break
        return is_exit

    @staticmethod
    def get_need_merge_csv_file_list(project_name, cache_directory):
        files = []
        try:
            dir_list = os.listdir(cache_directory)
            for cur_file in dir_list:
                path = os.path.join(cache_directory, cur_file)
                if os.path.isdir(path):
                    pass
                    # next_folder_files, next_folder_status = FileUtil.list_dir(path)
                    # if len(next_folder_files) != 0 and next_folder_status != 201:
                    #     files.extend(next_folder_files)
                elif os.path.isfile(path):
                    file_path, file_name = os.path.split(path)
                    file_name_text, extension = os.path.splitext(file_name)
                    if extension == ".csv" and file_name_text != (project_name + '_merged'):
                        files.append(file_name)
        except FileNotFoundError as e:
            print(e)
        return files

    @staticmethod
    def fill_in_dir_path(path):
        if not path.endswith('/'):
            path = path + '/'
        return path

    @staticmethod
    def write_csv_data(path, csv_data):
        with open(path, 'w', encoding="utf-8", newline='') as f:
            from_writer = csv.writer(f)
            from_writer.writerows(csv_data)
