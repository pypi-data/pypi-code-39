#
# Copyright (c) 2016, deepsense.io
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from future.builtins import str

from neptune.internal.common import NeptuneException


class NeptuneCannotOverrideFileWithDirectory(NeptuneException):
    def __init__(self, src, dst):
        super(NeptuneCannotOverrideFileWithDirectory, self).__init__(
            str(u"cannot overwrite non-directory '{1}' with directory '{0}'").format(src, dst))


class NeptuneCannotOverrideDirectory(NeptuneException):
    def __init__(self, dir_path, dir_name):
        super(NeptuneCannotOverrideDirectory, self).__init__(
            str(u"cannot overwrite directory '{1}' with directory '{0}'. "
                u"If you want to replace it, please first remove it "
                u"using 'neptune data rm -r {1}' command").format(dir_path, dir_name))


class NeptuneCannotOverrideFile(NeptuneException):
    def __init__(self, file_path, file_name):
        super(NeptuneCannotOverrideFile, self).__init__(
            str(u"cannot overwrite non-directory '{1}'. "
                u"If you want to override it, type 'neptune data upload {0} {1}'").format(file_path, file_name))


class NeptuneCreateFileFromDirectoryException(NeptuneException):
    def __init__(self, f):
        super(NeptuneCreateFileFromDirectoryException, self).__init__(
            str(u"Failed to access '{}': Not a directory").format(f))


class NeptuneNonRecursiveDirectoryUpload(NeptuneException):
    def __init__(self, f):
        super(NeptuneNonRecursiveDirectoryUpload, self).__init__(
            str(u"Cannot upload, because directory '{}' is not empty. Use -r/--recursive flag to upload").format(f))


class NeptuneNonRecursiveDirectoryDownload(NeptuneException):
    def __init__(self, f):
        super(NeptuneNonRecursiveDirectoryDownload, self).__init__(
            str(u"Cannot download, because '{}' is a directory. Use -r/--recursive flag to download").format(f))


class NeptuneFileNotFoundException(NeptuneException):
    def __init__(self, error_message):
        super(NeptuneFileNotFoundException, self).__init__(
            u"{} Try to use 'neptune data ls' to list the content of directory".format(error_message))


class NeptuneCantRemoveWithoutRecursiveException(NeptuneException):
    def __init__(self, error_message):
        super(NeptuneCantRemoveWithoutRecursiveException, self).__init__(
            u"{}. Use -r/--recursive flag to remove".format(error_message))


class NeptuneFileAccessForbidden(NeptuneException):
    def __init__(self, error_message):
        super(NeptuneFileAccessForbidden, self).__init__(
            u"{}. Use 'neptune data ls' to verify path to file".format(error_message))


class InsufficientFundsError(NeptuneException):
    def __init__(self):
        super(InsufficientFundsError, self).__init__(
            u"Insufficient funds.")
