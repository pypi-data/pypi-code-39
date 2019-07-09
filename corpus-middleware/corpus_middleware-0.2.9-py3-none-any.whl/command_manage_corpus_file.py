import csv
import os
import click
import uuid
import json
import asyncio
from middleware.utils.password import PassWord
from middleware.utils.time_util import TimeUtil
from middleware.utils.file_util import FileUtil
from middleware.utils.csv_merge import get_csv_data, merge_csv
from middleware.api.corpus_file_manger import CorpusFileManager


@click.group()
# @click.option('--version', '-V', default="", type=str, help='corpus-middleware version.')
def cli():
    """corpus-middleware package"""


@cli.command('version', short_help='corpus-middleware version.')
def version():
    click.echo('corpus-middleware 0.1.3')


@cli.command('convert', short_help='Convert origin corpus data txt file to csv file')
@click.option('--path', "-p", required=True, type=str,
              help='The origin corpus data file path or origin corpus data files directory.')
@click.option('--separator', "-s", required=True, type=str, help='The separator to split each column.')
@click.option('--titles', "-t", required=True, default="", type=str,
              help='if origin corpus data don\'t have title row,use this variable to append.')
@click.option('--need_append_uuid', "-i", default=False, type=bool, show_default=True,
              help='if origin corpus data don\'t have id column,set the variable True.')
def convert(path, separator, titles, need_append_uuid):
    """Convert origin corpus data txt file to csv file."""
    if os.path.exists(path):
        if os.path.isdir(path):
            click.echo('The path is a directory')
            origin_file_dir = path
            origin_file_list = os.listdir(path)
            for i in range(0, len(origin_file_list)):
                file_path = os.path.join(origin_file_dir, origin_file_list[i])
                file_name = os.path.basename(file_path)
                file_name_text, extension = os.path.splitext(file_name)
                if extension != ".txt":
                    continue
                click.echo(file_name + " Convert start")
                convert_file(file_path, file_name_text, separator, titles, need_append_uuid)
        else:
            click.echo('The path is a file')
            file_name = os.path.basename(path)
            file_name_text, extension = os.path.splitext(file_name)
            if extension != ".txt":
                click.echo('The path is not a txt file,Please check your path parameter')
            click.echo(file_name + " Convert start")
            convert_file(path, file_name_text, separator, titles, need_append_uuid)
    else:
        click.echo('The path:{} do not exist,Please check your path parameter'.format(path))


def convert_file(path, file_name_text, separator, titles, need_append_uuid):
    read_origin_list = read_origin_file(path, separator, titles, need_append_uuid)
    if len(read_origin_list) != 0:
        origin_file_dir = os.path.dirname(path)
        output_file_name = file_name_text + ".csv"
        write_output_file(os.path.join(origin_file_dir, output_file_name), read_origin_list)
        click.echo(os.path.join(origin_file_dir, output_file_name) + " Convert Finish")
    else:
        click.echo(file_name_text + " Convert error,The file read fail")


def read_origin_file(origin_file_path, separator, titles, need_append_uuid=False):
    origin_list = []
    if titles != "":
        title_list = titles.split(',')
        if len(title_list) <= 0:
            return origin_list
        else:
            title_list.insert(0, 'uuid')
            origin_list.append(title_list)
    if os.path.exists(origin_file_path):
        with open(origin_file_path, "r", encoding="utf-8") as f:
            line_num = 0
            for line in f:
                line_num += 1
                if line.strip() == "":
                    continue
                line_list = line.strip('\n').split(separator)
                if need_append_uuid:
                    if line_num == 0:
                        line_list.insert(0, "uuid")
                    else:
                        line_list.insert(0, str(uuid.uuid4()))
                origin_list.append(line_list)
    else:
        pass
    return origin_list


def write_output_file(out_put_file, origin_list):
    with open(out_put_file, "w", encoding="utf-8", newline='') as out:
        csv_write = csv.writer(out)
        csv_write.writerows(origin_list)


@cli.command('upload', short_help='upload corpus file')
@click.option('--account', '-a', required=True, prompt='enter your meta account')
@click.option('--password', '-p', required=True, prompt='enter your password', hide_input=True)
@click.option('--url', '-u', prompt='enter your cloud server url', required=True, type=str)
@click.option('--project_name', '-n', prompt='enter your nmt project name', required=True, type=str)
@click.option('--sub_directory', '-s', default="", type=str,
              help='The sub directory for the file in project')
@click.option('--file_path', '-f', prompt='enter your pre upload file path', required=True, type=str,
              help='pre upload file path')
def upload(account, password, url, project_name, sub_directory, file_path):
    encrypt_password = str(PassWord.rsa_encrypt(password), 'utf-8')
    if os.path.exists(file_path):
        file_parent_path, file_name = os.path.split(file_path)
        file_name_text, extension = os.path.splitext(file_name)
        if extension != ".csv":
            click.echo("待上传文件格式不是csv格式文件")
            return
        params = {
            "account": account,
            "password": encrypt_password,
            "file_name": file_name,
            "project_name": project_name,
            "sub_directory": sub_directory
        }
        msg = asyncio.get_event_loop().run_until_complete(CorpusFileManager.upload_file(url, params, file_path))
        click.echo(msg)
    else:
        click.echo("待上传的文件路径不存在")


@cli.command('download', short_help='download corpus file')
@click.option('--account', '-a', required=True, prompt='enter your meta account')
@click.option('--password', '-p', required=True, prompt='enter your password', hide_input=True)
@click.option('--url', '-u', prompt='enter your cloud server url', required=True, type=str)
@click.option('--cache_path', '-c', prompt='enter your nmt project name', required=True, type=str)
@click.option('--project_name', '-n', prompt='enter your download file cache path', required=True, type=str)
@click.option('--sub_directory', '-s', default="", type=str, help='The sub directory for the file in project')
@click.option('--start_time', '-st', default="", type=str, )
@click.option('--end_time', '-et', default="", type=str)
def download(account, password, url, cache_path, project_name, sub_directory, start_time, end_time):
    cache_path = FileUtil.fill_in_dir_path(cache_path)
    FileUtil.fill_the_full_path(cache_path)
    file_info_list_cache = read_project_cache_file(cache_path, project_name)
    if start_time:
        start_time = TimeUtil.data_time_valid_and_formatter(start_time)
        if not start_time:
            click.echo("start_time 参数格式不正确,请确认是否为'yyyy-MM-dd hh:mm:ss'或者'yyyy-MM-dd'格式")
            return
    if end_time:
        end_time = TimeUtil.data_time_valid_and_formatter(end_time)
        if not end_time:
            click.echo("end_time 参数格式不正确,请确认是否为'yyyy-MM-dd hh:mm:ss'或者'yyyy-MM-dd'格式")
            return
    encrypt_password = str(PassWord.rsa_encrypt(password), 'utf-8')
    params = {
        "account": account,
        "password": encrypt_password,
        "project_name": project_name,
        "sub_directory": sub_directory
    }
    if start_time:
        params.update({'start_time': start_time})
    if end_time:
        params.update({'end_time': end_time})
    status, msg, file_info_list = asyncio.get_event_loop().run_until_complete(
        CorpusFileManager.search_for_file_info(url, params))
    if status != 200:
        click.echo(msg)
        return
    else:
        pre_download_file_list = check_file_info_cache_for_download_list(cache_path, file_info_list,
                                                                         file_info_list_cache)
        if len(pre_download_file_list) > 0:
            write_project_cache_file(cache_path, project_name, file_info_list)
            download_params = {
                "account": account,
                "password": encrypt_password,
                "project_name": project_name
            }
            asyncio.get_event_loop().run_until_complete(CorpusFileManager.download_common(url, download_params,
                                                                                          cache_path,
                                                                                          pre_download_file_list))
            click.echo('所有文件已下载完毕 开始自动合并')
            merge_msg = merge_corpus_file(project_name, cache_path)
            click.echo(merge_msg)
        else:
            click.echo('所有文件均已存在于缓存目录中，且云端文件未发生改变')


def merge_corpus_file(project_name, cache_directory):
    merge_msg = "合并完成"
    final_file_name_list = FileUtil.get_need_merge_csv_file_list(project_name, cache_directory)
    paths = ["{0}{1}".format(cache_directory, path) for path in final_file_name_list]
    if len(final_file_name_list) > 0:
        status, merged = merge_csv(paths)
        if status:
            FileUtil.write_csv_data(FileUtil.path_join(cache_directory, project_name + '_merged.csv'), merged)
        else:
            merge_msg = '合并失败, {} 该文件的 header首位不是 "uuid" ,请处理, 然后通过 merge 命令再次合并'.format(merged)
    else:
        merge_msg = "没有需要合并的csv文件"
    return merge_msg


@cli.command('list', short_help='download corpus file')
@click.option('--account', '-a', required=True, prompt='enter your meta account')
@click.option('--password', '-p', required=True, prompt='enter your password', hide_input=True)
@click.option('--url', '-u', prompt='enter your cloud server url', required=True, type=str)
@click.option('--project_name', '-n', prompt='enter your nmt project name', required=True, type=str)
@click.option('--sub_directory', '-s', default="", type=str, help='The sub directory for the file in project')
@click.option('--start_time', '-st', default="", type=str, )
@click.option('--end_time', '-et', default="", type=str)
def fil(account, password, url, project_name, sub_directory, start_time, end_time):
    if start_time:
        start_time = TimeUtil.data_time_valid_and_formatter(start_time)
        if not start_time:
            click.echo("start_time 参数格式不正确,请确认是否为'yyyy-MM-dd hh:mm:ss'或者'yyyy-MM-dd'格式")
            return
    if end_time:
        end_time = TimeUtil.data_time_valid_and_formatter(end_time)
        if not end_time:
            click.echo("end_time 参数格式不正确,请确认是否为'yyyy-MM-dd hh:mm:ss'或者'yyyy-MM-dd'格式")
            return
    encrypt_password = str(PassWord.rsa_encrypt(password), 'utf-8')
    params = {
        "account": account,
        "password": encrypt_password,
        "project_name": project_name,
        "sub_directory": sub_directory
    }
    if start_time:
        params.update({'start_time': start_time})
    if end_time:
        params.update({'end_time': end_time})
    status, msg, file_info_list = asyncio.get_event_loop().run_until_complete(
        CorpusFileManager.search_for_file_info(url, params))
    if status != 200:
        click.echo(msg)
        return
    else:

        file_name_list = ''
        for file_info in file_info_list:
            file_name_list += (file_info.get('name') + '\n')
        click.echo('[{}] 项目云端储存目录中有如下文件:\n{}'.format(project_name, file_name_list))


def read_project_cache_file(cache_path, project_name):
    file_info = {}
    file_info_cache_path = FileUtil.path_join(cache_path, project_name + '_file_info_cache.json')
    if os.path.exists(file_info_cache_path):
        with open(file_info_cache_path, 'r') as f:
            file_info = json.load(f)
    return file_info


def write_project_cache_file(cache_path, project_name, file_info):
    file_info_cache_path = FileUtil.path_join(cache_path, project_name + '_file_info_cache.json')
    with open(file_info_cache_path, 'w') as f:
        json.dump(file_info, f)


def check_file_info_cache_for_download_list(cache_path, file_info_list, file_info_list_cache):
    need_download_file_list = []
    for file_info in file_info_list:
        need_down_load = True
        for file_info_cache in file_info_list_cache:
            if TimeUtil.date_compare(file_info.get('mtime'), file_info_cache.get('mtime')) == 0:
                if FileUtil.check_cache_file_for_file(cache_path, file_info.get('name')):
                    need_down_load = False
        if need_down_load:
            need_download_file_list.append(file_info)
    return need_download_file_list


@cli.command('merge', short_help='merge download corpus file')
@click.option('--cache_path', '-c', prompt='enter your nmt project name', required=True, type=str)
@click.option('--project_name', '-n', prompt='enter your download file cache path', required=True, type=str)
def merge(cache_path, project_name):
    cache_path = FileUtil.fill_in_dir_path(cache_path)
    merge_msg = merge_corpus_file(project_name, cache_path)
    click.echo(merge_msg)


if __name__ == '__main__':
    cli()

    # python -m  middleware.command_manage_corpus_file list -a 13438329868 -p Xl19920814 -u http://172.168.1.26:8002 -n 文档
    # python -m  middleware.command_manage_corpus_file upload -a 13438329868 -p Xl19920814 -u http://172.168.1.26:8002 -n 语料 -f D:\Temp\origin_corpus\origin_valid.csv

