#
# Copyright (c) 2018, deepsense.io
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


def paginated_http_request(request_call, params, page_size):

    offset = params.get('offset', 0)
    limit = params.get('limit')

    last = (offset + limit) if limit else None
    total = 0

    ceiling = limit or float('inf')

    while total < ceiling:

        if last is None:
            limit = page_size
        else:
            left = last - offset

            if not left:
                raise StopIteration

            limit = left if left < page_size else page_size

        params = params.copy()
        params['limit'] = limit
        params['offset'] = offset

        response = request_call(params)
        entities = response['entries']

        if not entities:
            raise StopIteration

        offset += len(entities)

        for entity in entities:
            yield entity
