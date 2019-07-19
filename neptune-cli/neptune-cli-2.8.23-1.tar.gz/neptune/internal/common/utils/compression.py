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
from future import standard_library

standard_library.install_aliases()

# pylint: disable=wrong-import-position

import gzip
import io


def gzip_compress(data):
    output_buffer = io.BytesIO()
    gzip_stream = gzip.GzipFile(fileobj=output_buffer, mode='w')
    gzip_stream.write(data)
    gzip_stream.close()
    return output_buffer.getvalue()
