from __future__ import print_function
from pywebhdfs.errors import FileNotFound, PyWebHdfsException
from datetime import datetime
import os
import sys
from .tools import get_filename, permission_to_str, fail, cut_tail_slash, add_tail_slash, get_config

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

__DOWNLOAD_CHUNK_SIZE = 1024*1024
__UPLOAD_CHUNK_SIZE   = 1024*1024

def dfs_ls(hdfs, remote_filename):
    r = hdfs.get_file_dir_status(remote_filename)

    if r["FileStatus"]["type"] == "FILE":
        remote_filename = cut_tail_slash(remote_filename)
        r["FileStatus"]["pathSuffix"] = get_filename(remote_filename)
        result = [r["FileStatus"]]
    else:
        result = hdfs.list_dir(remote_filename)["FileStatuses"]["FileStatus"]

    max_namelen = 0
    max_ownerlen = 0
    max_grouplen = 0
    for file_summary in result:
        max_namelen = max(max_namelen, len(file_summary["pathSuffix"]))
        max_ownerlen = max(max_ownerlen, len(file_summary["owner"]))
        max_grouplen = max(max_grouplen, len(file_summary["group"]))

    fmt = '{{permission_str}} {{owner:{}}} {{group:{}}} {{length:16}} {{modification_time:10}} {{filename:{}}}'.format(
        max_ownerlen, max_grouplen, max_namelen)
    for file_summary in result:
        modification_time = datetime.fromtimestamp(file_summary["modificationTime"] / 1000).strftime(
            "%Y-%m-%d %H:%M:%S")

        print(
            fmt.format(
                permission_str=permission_to_str(file_summary),
                owner=file_summary["owner"],
                group=file_summary["group"],
                filename=file_summary["pathSuffix"],
                length=file_summary["length"],
                modification_time=modification_time,
            )
        )

def _download_internal(
        hdfs,
        remote_filename,
        local_filename,
        local_file_handle=None,
        opened_in_binary_moode=False
):
    chunk_size = get_config().get("download_chunk_size", __DOWNLOAD_CHUNK_SIZE)
    # if caller supply local_file_handle, then opened_in_binary_moode tells
    # if the file is opened in text mode or binary mode
    if local_filename is None and local_file_handle is None:
        fail("You must provide local_filename or local_file_handle")

    def do_copy(f, opened_in_binary_moode):
        offset = 0
        while True:
            b = hdfs.read_file(
                remote_filename,
                offset=offset,
                length=chunk_size
            )
            if len(b) > 0:
                if opened_in_binary_moode:
                    f.write(b)
                else:
                    f.buffer.write(b)
            if len(b) < chunk_size:
                break
            offset += len(b)


    if local_file_handle is None:
        with open(local_filename, "wb") as f:
            do_copy(f, True)
    else:
        do_copy(local_file_handle, opened_in_binary_moode)

def dfs_download(hdfs, remote_filename, local_filename):
    remote_filename = cut_tail_slash(remote_filename)
    if os.path.isdir(local_filename):
        # if local filename is a directory, we are copy file into this directory
        local_filename = add_tail_slash(local_filename) + get_filename(remote_filename)

    try:
        r = hdfs.get_file_dir_status(remote_filename)
        if r["FileStatus"]["type"] != "FILE":
            # exist but not a file, consider file not found
            fail("File not found: {}".format(remote_filename))
    except FileNotFound:
        fail("File not found: {}".format(remote_filename))

    return _download_internal(hdfs, remote_filename, local_filename)

def dfs_cat(hdfs, remote_filename):
    _download_internal(
        hdfs, 
        remote_filename, 
        None, 
        local_file_handle=sys.stdout, 
        opened_in_binary_moode=False
    )

def dfs_mkdir(hdfs, remote_filename):
    try:
        r = hdfs.get_file_dir_status(remote_filename)
        if r["FileStatus"]["type"] == "FILE":
            fail("File with the same name exists")
        if r["FileStatus"]["type"] == "DIRECTORY":
            # shortcut, since the directory already exist
            return
    except FileNotFound:
        pass
    hdfs.make_dir(remote_filename)

def dfs_rm(hdfs, remote_filename, recursive):
    # WebHDFS does not fail if remote_filename does not exist
    hdfs.delete_file_dir(remote_filename, recursive=recursive)

# When force is True, if file already exist on the target, it will remote it
def dfs_upload(hdfs, local_filename, remote_filename, force):
    local_filename = cut_tail_slash(local_filename)
    # remote_filename could be a path name

    if not os.path.isfile(local_filename):
        fail("File not found: {}".format(local_filename))

    # if remote_filename is a path, file gets copied into that directory
    try:
        r = hdfs.get_file_dir_status(remote_filename)
        if r["FileStatus"]["type"] == "DIRECTORY":
            remote_filename = add_tail_slash(remote_filename) + get_filename(local_filename)
    except FileNotFound:
        # it is ok if the remote file does not exist
        # how the caller created the directory first
        pass

    if force:
        try:
            r = hdfs.get_file_dir_status(remote_filename)
            if r["FileStatus"]["type"] == "FILE":
                hdfs.delete_file_dir(remote_filename, recursive=False)
        except FileNotFound:
            # it is ok if the remote file does not exist
            # how the caller created the directory first
            pass

    hdfs.create_file(remote_filename, b'')
    chunk_size = get_config().get("upload_chunk_size", __UPLOAD_CHUNK_SIZE)
    with open(local_filename, "rb") as f:
        while True:
            b = f.read(chunk_size)
            if len(b) > 0:
                hdfs.append_file(remote_filename, b)
            if len(b) < chunk_size:
                break

def dfs_mv(hdfs, source_filename, destination_filename):
    r = hdfs.rename_file_dir(source_filename, destination_filename)
    if not r["boolean"]:
        fail("Move file failed")
