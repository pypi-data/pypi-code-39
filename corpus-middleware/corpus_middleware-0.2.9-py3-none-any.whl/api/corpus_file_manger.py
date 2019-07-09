#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

# from middleware.settings import logger
from middleware.downloader.http import post, download_file, post_file
from middleware.utils.csv_merge import get_csv_data, merge_csv
from middleware.utils.file_util import FileUtil


class CorpusFileManager:
    def __init__(self):
        pass

    # """
    # 根据文件名列表检查缓存目录中是否存在在相应文件
    # 返回两个列表，分别为：不存在文件名列表，存在文件名列表
    # """
    #
    # async def __check_cache_file_for_list(self, cache_directory, pre_check_file_name_list):
    #     exist_file_list = []
    #     if FileUtil.check_directory_exist(cache_directory) is False:
    #         return pre_check_file_name_list, exist_file_list
    #     # 检查请求的文件是否存在于缓存文件夹内
    #     files = FileUtil.list_dir(cache_directory)
    #     for file in files:
    #         file_path = FileUtil.path_join(cache_directory, file)
    #         file_name = os.path.basename(file_path)
    #         if file_name in pre_check_file_name_list:
    #             exist_file_list.append(file_name)
    #             pre_check_file_name_list.remove(file_name)
    #     not_exist_file_list = pre_check_file_name_list
    #     return not_exist_file_list, exist_file_list
    #
    # """
    # 根据文件名检查缓存目录中是否存在在相应文件
    # 返回是或否
    # """
    #
    # @staticmethod
    # def check_cache_file_for_file(cache_directory, pre_check_file_name):
    #     is_exit = False
    #     if FileUtil.check_directory_exist(cache_directory) is False:
    #         return is_exit
    #     # 检查请求的文件是否存在于缓存文件夹内
    #     files = FileUtil.list_dir(cache_directory)
    #     for file in files:
    #         file_path = FileUtil.path_join(cache_directory, file)
    #         file_name = os.path.basename(file_path)
    #         if file_name == pre_check_file_name:
    #             is_exit = True
    #             break
    #     return is_exit
    #
    # """
    # 根据文件创建时间来读取语料文件
    # 逻辑为：
    #     先搜索符合条件的文件列表
    #     检查符合条件的文件是否存在已下载的缓存目录中
    #     下载不存在缓存目录中的文件
    #     读取所有符合条件的文件，并merge返回
    # """
    #
    # async def get_for_time(self, cloud_url, cache_directory, sub_directory, project_name, start_time, end_time):
    #     cache_path = FileUtil.path_join_for_cache_path(cache_directory, sub_directory, project_name)
    #     # 先搜索符合条件的文件列表
    #     option = {
    #         "start_time": start_time,
    #         "end_time": end_time,
    #         "project_name": project_name,
    #         "sub_directory": sub_directory
    #     }
    #     search_status, msg, paths = await self.__search_for_paths(cloud_url, option)
    #     print(paths)
    #     if search_status != 200:
    #         return dict(status=search_status, msg=msg, resp=[])
    #
    #     # 检查符合条件的文件是否存在已下载的缓存目录中
    #     pre_check_file_name_list = []
    #     for path in paths:
    #         pre_check_file_name_list.append(path["name"])
    #     pre_download_list, exist_file_list = await self.__check_cache_file_for_list(cache_path,
    #                                                                                 pre_check_file_name_list)
    #
    #     # 下载不存在缓存目录中的文件
    #     pre_download_file_list = []
    #     for path in paths:
    #         if path["name"] in pre_download_list:
    #             pre_download_file_list.append(path)
    #     if len(pre_download_file_list) > 0:
    #         FileUtil.fill_the_full_path(cache_path)
    #         await self.download_common(cloud_url, cache_path, pre_download_file_list)
    #     else:
    #         msg = "cloud have no file in accordance with conditions and the file is not in cache "
    #         return dict(status=0, msg=msg, resp=[])
    #     # 读取所有符合条件的文件，并merge返回
    #     final_file_name_list = []
    #     for path in paths:
    #         final_file_name_list.append(path["name"])
    #     return await self.__get_common(final_file_name_list, cache_path)
    #
    # """
    # 根据文件文件名列表来读取语料文件
    # 逻辑为：
    #     检查符合条件的文件是否存在已下载的缓存目录中
    #     下载不存在缓存目录中的文件
    #     读取所有符合条件的文件，并merge返回
    # """
    #
    # async def get_for_name_multiple(self, cloud_url, cache_directory, sub_directory, project_name, file_name_list):
    #     # 检查符合条件的文件是否存在已下载的缓存目录中
    #     cache_path = FileUtil.path_join_for_cache_path(cache_directory, sub_directory, project_name)
    #     pre_download_list, exist_file_list = await self.__check_cache_file_for_list(cache_path, file_name_list)
    #
    #     # 下载不存在缓存目录中的文件
    #     if len(pre_download_list) > 0:
    #         option = {
    #             "file_name_list": pre_download_list,
    #             "project_name": project_name,
    #             "sub_directory": sub_directory
    #         }
    #         search_status, msg, paths = await self.__search_for_paths(cloud_url, option)
    #         if search_status != 200:
    #             return dict(status=search_status, msg=msg, resp=[])
    #         if len(paths) > 0:
    #             FileUtil.fill_the_full_path(cache_path)
    #             await self.download_common(cloud_url, cache_path, paths)
    #         else:
    #             return dict(status=0,
    #                         msg="cloud have no file in accordance with conditions and the files are not in cache",
    #                         resp=[])
    #     # 读取所有符合条件的文件，并merge返回
    #     pre_download_list.extend(exist_file_list)
    #     final_file_name_list = pre_download_list
    #     return await self.__get_common(final_file_name_list, cache_path)
    #
    # """
    # 根据单个文件文件名来读取语料文件
    # 逻辑为：
    #     检查符合条件的文件是否存在已下载的缓存目录中
    #     下载不存在缓存目录中的文件
    #     读取所有符合条件的文件，并merge返回
    # """
    #
    # async def get_for_name_single(self, cloud_url, cache_directory, sub_directory, project_name, file_name,
    #                               merge_content):
    #     # 检查符合条件的文件是否存在已下载的缓存目录中
    #     cache_path = FileUtil.path_join_for_cache_path(cache_directory, sub_directory, project_name)
    #     print(cache_path)
    #     is_exit = await self.check_cache_file_for_file(cache_path, file_name)
    #     print(is_exit)
    #     # 下载不存在缓存目录中的文件
    #     if not is_exit:
    #         pre_download_list = [file_name]
    #         option = {
    #             "file_name_list": pre_download_list,
    #             "project_name": project_name,
    #             "sub_directory": sub_directory
    #         }
    #         print(option)
    #         search_status, msg, paths = await self.__search_for_paths(cloud_url, option)
    #         print(paths)
    #         if search_status != 200:
    #             return dict(status=search_status, msg=msg, resp=[])
    #         if len(paths) > 0:
    #             FileUtil.fill_the_full_path(cache_path)
    #             await self.download_common(cloud_url, cache_path, paths)
    #         else:
    #             return dict(status=0,
    #                         msg="cloud have no file in accordance with conditions and the file is not in cache",
    #                         resp=[])
    #     # 读取所有符合条件的文件，并merge返回
    #     final_file_name_list = [file_name]
    #     return await self.__get_common(final_file_name_list, cache_path, merge_content)
    #
    # """
    # 读取语料文件公共方法
    # 逻辑为：
    #     按文件名请求时：
    #     单个文件时，根据输入的参数来确定是直接返回CSV内容，还是merge后再返回
    #     多个文件时，一定merge
    #     按时间参数请求时：
    #     一定merge
    # """
    #
    # async def __get_common(self, final_file_name_list, cache_directory, merge_content=True):
    #     merge_status = 200
    #     msg = ""
    #     paths = ["{0}{1}".format(cache_directory, file_name) for file_name in final_file_name_list]
    #     merged = None
    #     if len(final_file_name_list) > 0:
    #         if merge_content:
    #             merged = merge_csv(paths)
    #         else:
    #             if len(final_file_name_list) == 1:
    #                 merged = get_csv_data(paths[0])
    #             else:
    #                 merged = merge_csv(paths)
    #     else:
    #         merge_status = 0
    #         msg = "there is no file in accordance with conditions "
    #     return dict(status=merge_status, msg=msg, resp=merged)
    #
    # """
    # 仅用于按时间参数下载文件
    # 需要检查本地缓存是否存在该文件
    # """
    #
    # async def download_for_time(self, cloud_url, cache_directory, sub_directory, project_name, start_time, end_time):
    #     cache_path = FileUtil.path_join_for_cache_path(cache_directory, sub_directory, project_name)
    #     option = {
    #         "start_time": start_time,
    #         "end_time": end_time,
    #         "project_name": project_name,
    #         "sub_directory": sub_directory
    #     }
    #     search_status, msg, paths = await self.__search_for_paths(cloud_url, option)
    #     if search_status != 200:
    #         return dict(status=search_status, msg=msg, resp=[])
    #     if len(paths) > 0:
    #         # 检查符合条件的文件是否存在已下载的缓存目录中
    #         pre_check_file_name_list = []
    #         for path in paths:
    #             pre_check_file_name_list.append(path["name"])
    #         pre_download_list, exist_file_list = await self.__check_cache_file_for_list(cache_path,
    #                                                                                     pre_check_file_name_list)
    #         # 下载不存在缓存目录中的文件
    #         pre_download_file_list = []
    #         for path in paths:
    #             if path["name"] in pre_download_list:
    #                 pre_download_file_list.append(path)
    #         if len(pre_download_file_list) > 0:
    #             FileUtil.fill_the_full_path(cache_path)
    #             await self.download_common(cloud_url, cache_path, pre_download_file_list)
    #     else:
    #         msg = "there is no file in accordance with conditions "
    #         return dict(status=0, msg=msg, resp=[])
    #
    # """
    # 仅用于按文件名列表下载文件
    # 需要检查本地缓存是否存在该文件
    # """
    #
    # async def download_for_name_multiple(self, cloud_url, cache_directory, sub_directory, project_name, file_name_list):
    #     # 检查符合条件的文件是否存在已下载的缓存目录中
    #     cache_path = FileUtil.path_join_for_cache_path(cache_directory, sub_directory, project_name)
    #     pre_download_list, exist_file_list = await self.__check_cache_file_for_list(cache_path, file_name_list)
    #
    #     # 下载不存在缓存目录中的文件
    #     if len(pre_download_list) > 0:
    #         option = {
    #             "file_name_list": pre_download_list,
    #             "project_name": project_name,
    #             "sub_directory": sub_directory
    #         }
    #         search_status, msg, paths = await self.__search_for_paths(cloud_url, option)
    #         if search_status != 200:
    #             return dict(status=search_status, msg=msg, resp=[])
    #         if len(paths) > 0:
    #             FileUtil.fill_the_full_path(cache_path)
    #             await self.download_common(cloud_url, cache_path, paths)
    #             return dict(status=200, msg="", resp=[])
    #         else:
    #             return dict(status=0,
    #                         msg="cloud have no file in accordance with conditions and the files are not in cache",
    #                         resp=[])
    #
    #     else:
    #         return dict(status=200, msg="the file is exit in cache", resp=[])
    #
    # """
    # 仅用于按单个文件名下载文件
    # 需要检查本地缓存是否存在该文件
    # """
    #
    # async def download_for_name_single(self, cloud_url, cache_directory, sub_directory, project_name, file_name):
    #     # 检查符合条件的文件是否存在已下载的缓存目录中
    #     cache_path = FileUtil.path_join_for_cache_path(cache_directory, sub_directory, project_name)
    #     is_exit = await self.check_cache_file_for_file(cache_path, file_name)
    #     # 下载不存在缓存目录中的文件
    #     if not is_exit:
    #         pre_download_list = [file_name]
    #         option = {
    #             "file_name_list": pre_download_list,
    #             "project_name": project_name,
    #             "sub_directory": sub_directory
    #         }
    #         search_status, msg, paths = await self.__search_for_paths(cloud_url, option)
    #         print(paths)
    #         if search_status != 200:
    #             return dict(status=search_status, msg=msg, resp=[])
    #         if len(paths) > 0:
    #             FileUtil.fill_the_full_path(cache_path)
    #             await self.download_common(cloud_url, cache_path, paths)
    #             return dict(status=200, msg="", resp=[])
    #         else:
    #             return dict(status=0,
    #                         msg="cloud have no file in accordance with conditions and the file is not in cache",
    #                         resp=[])
    #     else:
    #         return dict(status=200, msg="the file is exit in cache", resp=[])
    #
    # """
    # 根据条件请求所有符合条件的语料文件信息
    # 返回 状态吗 简略信息 语料信息列表
    # """
    #
    # async def __search_for_paths(self, cloud_url, option):
    #     resp = await post("{0}file/search".format(cloud_url), option)
    #     status = resp["status"]
    #     msg = ""
    #     if status != 200:
    #         if status == 201:
    #             msg = "this project_name is not found"
    #         elif status == 202:
    #             msg = "there is no variable named start_time and file_name_list"
    #         return status, msg, []
    #     paths = resp["paths"]
    #     return status, msg, paths

    """
    下载文件公共代码
    """

    @staticmethod
    async def download_common(cloud_url, params, cache_path, paths):
        for path in paths:
            await download_file("{0}/file/download?path={1}".format(cloud_url, path["path"]), params,
                                FileUtil.path_join(cache_path, path["name"]))

    @staticmethod
    async def upload_file(url, params, file_path):
        resp = await post_file('{0}/file/upload'.format(url), params, file_path)
        status = resp["status"]
        msg = "上传完成"
        if status != 200:
            if status == 201:
                msg = "云端项目名称不存在"
            elif status == 202:
                msg = "数据库更新失败"
            elif status == 203:
                msg = "用户名或密码错误"
            elif status == 204:
                msg = "你没有操作该项目的权限"
            elif status == 205:
                msg = "无法连接到这个地址 :{}".format(url)
            elif status == 206:
                msg = "无效的URL"
            elif status == 207:
                msg = "服务器连接超时"
            elif status == 208:
                msg = "服务器无法连接"
        return msg

    @staticmethod
    async def search_for_file_info(url, option):
        resp = await post("{0}/file/fileinfo".format(url), option)
        status = resp["status"]
        msg = ""
        if status != 200:
            if status == 201:
                msg = "云端项目名称不存在"
            elif status == 203:
                msg = "用户名或密码错误"
            elif status == 204:
                msg = "你没有操作该项目的权限"
            elif status == 205:
                msg = "无法连接到这个地址 :{}".format(url)
            elif status == 206:
                msg = "无效的URL"
            elif status == 207:
                msg = "服务器连接超时"
            elif status == 208:
                msg = "服务器无法连接"
            return status, msg, []
        file_info_list = resp["file_info"]
        return status, msg, file_info_list
