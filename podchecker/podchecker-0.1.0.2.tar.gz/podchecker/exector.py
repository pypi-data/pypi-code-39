#! /usr/local/bin/python3
# encoding: utf-8
# Author: LiTing


"""
    USAGE

        python3 <script_name>.py -s <src_path> -d <dst_path> [-h]


    SUPPORT FUNCTIONS

        1. support compare files as below
            ------------------------------------------------------------
              Platform      SRC_FILE                DST_FILE
            ------------------------------------------------------------
              iOS           podfile					podfile
              iOS           podfile					podfile.lock
              iOS           podfile.lock			podfile
              iOS           podfile.lock			podfile.lock
              Android       version.properties      version.properties
            ------------------------------------------------------------
              TODO:
              Compounded    pods.cfg                pods.cfg
            ------------------------------------------------------------

        2. group output
            - compare rslts: src & dst (equal)
            - compare rslts: src & dst (unequal)
            - compare rslts: src - dst (dst None)
            - compare rslts: dst - src (src None)


    SUPPORT OPTIONS

        -s, --src_path
            [Required] src file path (local url or remote url is FINE)

        -d, --dst_path
            [Required] dst file path (local url or remote url is FINE)

        -h, --help
            [Optional] Show this USAGE and exit.

    MORE

        requires python3

        requires valid file path (case insensitive):
            xxx/**/podfile
            xxx/**/podfile.lock
            xxx/**/version.properties
"""

import os
import sys
import getopt
import requests
import re
import subprocess
from enum import Enum, unique

# add search path
sys.path.append(os.path.abspath(os.path.curdir))
from .utils import *
from humanfriendly.terminal import usage, warning


def main(argv):
    # parse args
    try:
        opts, args = getopt.getopt(argv, 's:d:l:h', ['src_path=', 'dst_path=', 'log_path=', 'help'])
    except getopt.GetoptError:
        warning(__doc__)
        sys.exit(2)

    # 默认值
    src_path = ''
    dst_path = ''
    log_path = ''

    # 解析参数
    for opt, arg in opts:
        if opt in {'-s', '--src_path'}:
            src_path = arg
        elif opt in {'-d', '--dst_path'}:
            dst_path = arg
        elif opt in {'-l', '--log_path'}:
            log_path = arg
        elif opt in {'-h', '--help'}:
            usage(__doc__)
            return

    # 入口函数调用
    do_check(src_path, dst_path, log_path)


def do_check(src_path, dst_path, log_path):
    # set file logger
    LoggerAdapter.setfilepath(log_path)

    # script begin
    LoggerAdapter.logblue(f'\n-> begin {os.path.basename(__file__)}')

    # extract files
    LoggerAdapter.logblue(f'-> extracting files...')
    src_fileinfo, dst_fileinfo = FileInfo(src_path), FileInfo(dst_path)
    if src_fileinfo.location is FileLocation.invalid or dst_fileinfo.location is FileLocation.invalid:
        LoggerAdapter.logred(f'[!] error: src_path or dst_path is unreachable!')
        return

    if src_fileinfo.filetype is FileType.invalid or dst_fileinfo.filetype is FileType.invalid:
        LoggerAdapter.logred(f'[!] error: src_path or dst_path has invalid file type! (podfile|')
        return

    # extract pod
    src_extractor = PodExtractorFactory.extractor(src_fileinfo).run()
    dst_extractor = PodExtractorFactory.extractor(dst_fileinfo).run()
    if not src_extractor or not dst_extractor:
        LoggerAdapter.logred(f'[!] error: src or dst extractor failed!')
        return

    # compare
    a, b, c, d = PodComparer().compare(src_extractor, dst_extractor)

    # concole log
    # TODO: logger
    pass

    # say
    LoggerAdapter.logblue(f'\n-> saying rslts...')
    say_content = f'相同库:{a}个, 不同库:{b}个, 源-目标差集库:{c}个, 目标-源差集库:{d}个, 共计:{a+b+c+d}个 依赖库. \(仅供参考\)'
    subprocess.call(f'say {say_content}', shell=True)

    # end
    LoggerAdapter.logblue(f'\n-> end {os.path.basename(__file__)}\n')


# -------------------- Define --------------------

class LoggerAdapter(object):
    logger: logging.Logger = None

    @classmethod
    def setfilepath(cls, fp):
        cls.logger = LoggerBuilder.build('podchecker', logging.DEBUG, msgOnly=True).addFile(fp).logger()

    @classmethod
    def filelog(cls, log):
        if cls.logger:
            cls.logger.info(log)

    @classmethod
    def logblue(cls, log):
        PrintWithColor.blue(log)
        cls.filelog(log)

    @classmethod
    def loggreen(cls, log):
        PrintWithColor.green(log)
        cls.filelog(log)

    @classmethod
    def logred(cls, log):
        PrintWithColor.red(log)
        cls.logger.info(log)

    @classmethod
    def logyellow(cls, log):
        PrintWithColor.yellow(log)
        cls.logger.info(log)

    @classmethod
    def logcyan(cls, log):
        PrintWithColor.cyan(log)
        cls.logger.info(log)

@unique
class FileLocation(Enum):
    invalid = 0
    disk = 1
    remote = 2

@unique
class FileType(Enum):
    invalid = 'invalid'                 # invalid
    podfile = 'podfile'                 # iOS Podfile
    podfilelock = 'podfile.lock'        # iOS Podfile.lock
    properties = 'version.properties'   # Android version.properties
    config = '.cfg'                     # All pods.cfg

class FileInfo(object):
    filepath: str = ''
    location: FileLocation = FileLocation.invalid
    filetype: FileType = FileType.invalid

    def __init__(self, filepath):
        self.filepath = filepath
        self.location = self._verify_location(filepath)
        self.filetype = self._verify_filetype(filepath)

    def _verify_location(self, fp):
        if os.path.isfile(fp):
            return FileLocation.disk
        elif fp.startswith('http'):
            return FileLocation.remote
        return FileLocation.invalid

    def _verify_filetype(self, fp):
        if re.compile(r'podfile\.lock$', re.IGNORECASE).search(fp):
            return FileType.podfilelock
        elif re.compile(r'podfile$', re.IGNORECASE).search(fp):
            return FileType.podfile
        elif re.compile(r'version\.properties$', re.IGNORECASE).search(fp):
            return FileType.properties
        elif re.compile(r'\.cfg$', re.IGNORECASE).search(fp):
            return FileType.config
        return FileType.invalid


# -------------------- Pods --------------------


class Pod(object):
    name = ''
    version = ''

    def __init__(self, name, version):
        self.name = name
        self.version = version

    def __eq__(self, other):
        a = self.__class__ == other.__class__
        b = self.name == other.name
        c = self.version == other.version
        return a and b and c

    def __ne__(self, other):
        return not (self == other)

class PodExtractor(object):
    fileInfo: FileInfo
    pods: list = []

    def __init__(self, fileInfo):
        self.fileInfo = fileInfo
        self.pods = []

    def _get_all_content(self):
        f_text = ''
        if self.fileInfo.location is FileLocation.disk:
            LoggerAdapter.logblue(f'-> reading file content: {self.fileInfo.filepath}')
            with open(self.fileInfo.filepath, encoding='utf-8') as f:
                f_text = f.read()
        elif self.fileInfo.location is FileLocation.remote:
            LoggerAdapter.logblue(f'-> requesting file content: {self.fileInfo.filepath}')
            r = requests.get(self.fileInfo.filepath)
            f_text = r.text
        return f_text

    def extract(self, pattern):
        f_text = self._get_all_content()
        ai = re.compile(pattern).findall(f_text)
        if ai is not None:
            pod_dict = {t[0]: t[1] for t in ai}
            for k, v in pod_dict.items():
                tmp_pod = Pod(k, v)
                if tmp_pod not in self.pods:
                    self.pods.append(tmp_pod)

    def run(self):
        self.extract()
        return self

class IOSPodfileExtractor(PodExtractor):
    def extract(self):
        super().extract(r'pod[\s]+\'(.+?)\'[\s]*,[\s]*\'(.+?)\'')

class IOSPodfileLockExtractor(PodExtractor):
    def extract(self):
        super().extract(r'-[\s]*(.+?)[\s]*\([=~>\s]*(.+?)\)')

class AndroidPropertiesExtractor(PodExtractor):
    def extract(self):
        super().extract(r'(.+?)=(.+)')

class ConfigExtractor(PodExtractor):
    # TODO:
    def extract(self):
        pass

class PodExtractorFactory(object):
    @classmethod
    def extractor(cls, fileinfo) -> PodExtractor:
        if fileinfo.filetype is FileType.podfile:
            return IOSPodfileExtractor(fileinfo)
        elif fileinfo.filetype is FileType.podfilelock:
            return IOSPodfileLockExtractor(fileinfo)
        elif fileinfo.filetype is FileType.properties:
            return AndroidPropertiesExtractor(fileinfo)
        elif fileinfo.filetype is FileType.config:
            return ConfigExtractor(fileinfo)
        else:
            return None


# -------------------- Compare --------------------


class PodComparer(object):
    def compare(self, src_extractor, dst_extractor):
        LoggerAdapter.logblue('-> comparing...')

        # pods
        src_pods = src_extractor.pods
        dst_pods = dst_extractor.pods

        # pods dict
        src_pods_dict = {pod.name: pod for pod in src_pods}
        dst_pods_dict = {pod.name: pod for pod in dst_pods}

        # pair
        class PodComparePair(object):
            name: str
            srcPod: Pod
            dstPod: Pod

            def __init__(self, name, srcPod, dstPod):
                self.name = name
                self.srcPod = srcPod
                self.dstPod = dstPod

        def print_pairs(pairs, header_desc):
            def _print_format(arg1, arg2, arg3, arg4, arg4Color=0):
                if arg4Color == 1:
                    arg4 = PrintWithColor.simple_preferred_formatted_string(kFore.GREEN, arg4)
                elif arg4Color == 2:
                    arg4 = PrintWithColor.simple_preferred_formatted_string(kFore.RED, arg4)
                # TODO: _debug_format_num()
                return f'{arg1:<60s} {arg2:<40s} {arg3:<40s} {arg4:<10s}'

            LoggerAdapter.logcyan('\n' + header_desc + '\n')

            LoggerAdapter.logyellow(_print_format(f'pod_name({len(pairs)})', 'src_version', 'dst_version', 'up_to_date'))
            LoggerAdapter.logyellow(_print_format('-----------------------', '-----------', '-----------', '----------'))
            for pair in sorted(pairs, key=lambda x: x.name):
                none = 'None'
                name = pair.name
                src = pair.srcPod.version if pair.srcPod else none
                dst = pair.dstPod.version if pair.dstPod else none
                if src == none or dst == none:
                    compare = 'False-S' if src == none else 'False-D'
                else:
                    compare = 'True' if pair.srcPod.version == pair.dstPod.version else 'False.'
                # 这里分段着色比较特殊，分开写log
                PrintWithColor.yellow(_print_format(name, src, dst, compare, 1 if compare == 'True' else 2))
                LoggerAdapter.filelog(_print_format(name, src, dst, compare, 0))
            LoggerAdapter.logyellow(_print_format('-----------------------', '-----------', '-----------', '----------'))

        # a & b
        intersection_keys = set(src_pods_dict.keys()) & set(dst_pods_dict.keys())
        intersection_pairs = [PodComparePair(k, src_pods_dict[k], dst_pods_dict[k]) for k in intersection_keys]

        intersection_equal_pairs = [x for x in intersection_pairs if x.srcPod == x.dstPod]
        print_pairs(intersection_equal_pairs, '--> begin to compare (src & dst) : equal')

        intersection_unequal_pairs = [x for x in intersection_pairs if x.srcPod != x.dstPod]
        print_pairs(intersection_unequal_pairs, '--> begin to compare (src & dst) : unequal')

        # a - b
        src2dst_keys = set(src_pods_dict.keys()) - set(dst_pods_dict.keys())
        src2dst_pairs = [PodComparePair(k, src_pods_dict[k], None) for k in src2dst_keys]
        print_pairs(src2dst_pairs, '--> begin to compare (src - dst)')

        # b - a
        dst2src_keys = set(dst_pods_dict.keys()) - set(src_pods_dict.keys())
        dst2src_pairs = [PodComparePair(k, None, dst_pods_dict[k]) for k in dst2src_keys]
        print_pairs(dst2src_pairs, '--> begin to compare (dst - src)')

        return len(intersection_equal_pairs), len(intersection_unequal_pairs), len(src2dst_pairs), len(dst2src_pairs)


# ---------- Main ----------


if "__main__" == __name__:
    main(sys.argv[1:])


# TEST
# if __name__ == "__main__":
#     main([
#         # '-s', '/Users/match/work/xiami/pxiami/Podfile',
#         # '-d', '/Users/match/Desktop/111222333/Podfile',

#         '-s', 'http://mtl.alibaba-inc.com/oss/mupp/10801747/current/Podfile.lock',
#         '-d', 'http://mtl.alibaba-inc.com/oss/mupp/11334208/current/Podfile.lock',
#         '-l', '/Users/match/Desktop/podchecker/testlog.txt'

#         # '-h'
#     ])
