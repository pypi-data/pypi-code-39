# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd">
#   Copyright (c) 2003-2019 Aspose Pty Ltd
# </copyright>
# <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# -----------------------------------------------------------------------------------

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from groupdocs_annotation_cloud.auth import Auth
from groupdocs_annotation_cloud.api_client import ApiClient
from groupdocs_annotation_cloud.api_exception import ApiException
from groupdocs_annotation_cloud.configuration import Configuration

class PreviewApi(object):
    """
    GroupDocs.Annotation Cloud API

    :param configuration: API configuration
    """

    def __init__(self, configuration):
        api_client = ApiClient(configuration)

        self.auth = Auth(configuration, api_client)
        self.api_client = api_client
        self.configuration = configuration

    def close(self):  # noqa: E501
        """
        Closes thread pool. This method should be called when 
        methods are executed asynchronously (is_async=True is passed as parameter)
        and this instance of PreviewApi is not going to be used any more.
        """
        if self.api_client is not None:
            if(self.api_client.pool is not None):
                self.api_client.pool.close()
                self.api_client.pool.join()
                self.api_client.pool = None

    @classmethod
    def from_keys(cls, app_sid, app_key):
        """
        Initializes new instance of PreviewApi with API keys

        :param app_sid Application identifier (App SID)
        :param app_key Application private key (App Key)
        """
        configuration = Configuration(app_sid, app_key)
        return PreviewApi(configuration)

    @classmethod
    def from_config(cls, configuration):
        """
        Initializes new instance of PreviewApi with configuration options

        :param configuration API configuration
        """
        return PreviewApi(configuration)

    def delete_pages(self, request,**kwargs):  # noqa: E501
        """Removes document&#39;s pages image representations  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str file_path: Document path in storage (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True

        if kwargs.get('is_async'):
            return self._delete_pages_with_http_info(request, **kwargs)  # noqa: E501
        
        self._delete_pages_with_http_info(request, **kwargs)  # noqa: E501
        

    def _delete_pages_with_http_info(self, request, **kwargs):  # noqa: E501
        """Removes document&#39;s pages image representations  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param DeletePagesRequest request object with parameters
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_pages" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'file_path' is set
        if request.file_path is None:
            raise ValueError("Missing the required parameter `file_path` when calling `delete_pages`")  # noqa: E501

        collection_formats = {}
        path = '/annotation/pages'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('filePath') in path:
            path = path.replace('{' + self.__downcase_first_letter('filePath' + '}'), request.file_path if request.file_path is not None else '')
        else:
            if request.file_path is not None:
                query_params.append((self.__downcase_first_letter('filePath'), request.file_path))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        call_kwargs = {
            'resource_path':path, 
            'method':'DELETE',
            'path_params':path_params,
            'query_params':query_params,
            'header_params':header_params,
            'body':body_params,
            'post_params':form_params,
            'files':local_var_files,
            'response_type':None,  # noqa: E501
            'auth_settings':self.auth.get_auth_settings(),
            'is_async':params.get('is_async'),
            '_return_http_data_only':params.get('_return_http_data_only'),
            '_preload_content':params.get('_preload_content', True),
            '_request_timeout':params.get('_request_timeout'),
            'collection_formats':collection_formats
        }

        return self.api_client.call_api(**call_kwargs)  # noqa: E501

    def get_pages(self, request,**kwargs):  # noqa: E501
        """Generates image representations from documents pages  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param str file_path: Document path in storage (required)
        :param int count_pages_to_convert: The count pages to convert
        :param int page_number: The start page number
        :param list[int] page_numbers_to_convert: The list of page numbers to convert
        :param bool without_annotations: If true returns specific pages without annotations
        :param bool enable_caching: Indicates whether to use previously cached document or not
        :param str cache_storage_path: The cache storage path
        :param str password: Source document opening password
        :return: PageImages
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True

        if kwargs.get('is_async'):
            return self._get_pages_with_http_info(request, **kwargs)  # noqa: E501
        
        (data) = self._get_pages_with_http_info(request, **kwargs)  # noqa: E501
        return data

    def _get_pages_with_http_info(self, request, **kwargs):  # noqa: E501
        """Generates image representations from documents pages  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True

        :param is_async bool
        :param GetPagesRequest request object with parameters
        :return: PageImages
                 If the method is called asynchronously,
                 returns the request thread.
        """
        params = locals()
        params['is_async'] = ''
        params['_return_http_data_only'] = False
        params['_preload_content'] = True
        params['_request_timeout'] = ''
        for key, val in six.iteritems(params['kwargs']):
            if key not in params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_pages" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'file_path' is set
        if request.file_path is None:
            raise ValueError("Missing the required parameter `file_path` when calling `get_pages`")  # noqa: E501

        collection_formats = {}
        path = '/annotation/pages'
        path_params = {}

        query_params = []
        if self.__downcase_first_letter('filePath') in path:
            path = path.replace('{' + self.__downcase_first_letter('filePath' + '}'), request.file_path if request.file_path is not None else '')
        else:
            if request.file_path is not None:
                query_params.append((self.__downcase_first_letter('filePath'), request.file_path))  # noqa: E501
        if self.__downcase_first_letter('countPagesToConvert') in path:
            path = path.replace('{' + self.__downcase_first_letter('countPagesToConvert' + '}'), request.count_pages_to_convert if request.count_pages_to_convert is not None else '')
        else:
            if request.count_pages_to_convert is not None:
                query_params.append((self.__downcase_first_letter('countPagesToConvert'), request.count_pages_to_convert))  # noqa: E501
        if self.__downcase_first_letter('pageNumber') in path:
            path = path.replace('{' + self.__downcase_first_letter('pageNumber' + '}'), request.page_number if request.page_number is not None else '')
        else:
            if request.page_number is not None:
                query_params.append((self.__downcase_first_letter('pageNumber'), request.page_number))  # noqa: E501
        if self.__downcase_first_letter('pageNumbersToConvert') in path:
            path = path.replace('{' + self.__downcase_first_letter('pageNumbersToConvert' + '}'), request.page_numbers_to_convert if request.page_numbers_to_convert is not None else '')
        else:
            if request.page_numbers_to_convert is not None:
                query_params.append((self.__downcase_first_letter('pageNumbersToConvert'), request.page_numbers_to_convert))  # noqa: E501
                collection_formats[self.__downcase_first_letter('pageNumbersToConvert')] = 'multi'  # noqa: E501
        if self.__downcase_first_letter('withoutAnnotations') in path:
            path = path.replace('{' + self.__downcase_first_letter('withoutAnnotations' + '}'), request.without_annotations if request.without_annotations is not None else '')
        else:
            if request.without_annotations is not None:
                query_params.append((self.__downcase_first_letter('withoutAnnotations'), request.without_annotations))  # noqa: E501
        if self.__downcase_first_letter('enableCaching') in path:
            path = path.replace('{' + self.__downcase_first_letter('enableCaching' + '}'), request.enable_caching if request.enable_caching is not None else '')
        else:
            if request.enable_caching is not None:
                query_params.append((self.__downcase_first_letter('enableCaching'), request.enable_caching))  # noqa: E501
        if self.__downcase_first_letter('cacheStoragePath') in path:
            path = path.replace('{' + self.__downcase_first_letter('cacheStoragePath' + '}'), request.cache_storage_path if request.cache_storage_path is not None else '')
        else:
            if request.cache_storage_path is not None:
                query_params.append((self.__downcase_first_letter('cacheStoragePath'), request.cache_storage_path))  # noqa: E501
        if self.__downcase_first_letter('password') in path:
            path = path.replace('{' + self.__downcase_first_letter('password' + '}'), request.password if request.password is not None else '')
        else:
            if request.password is not None:
                query_params.append((self.__downcase_first_letter('password'), request.password))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = []

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        call_kwargs = {
            'resource_path':path, 
            'method':'GET',
            'path_params':path_params,
            'query_params':query_params,
            'header_params':header_params,
            'body':body_params,
            'post_params':form_params,
            'files':local_var_files,
            'response_type':'PageImages',  # noqa: E501
            'auth_settings':self.auth.get_auth_settings(),
            'is_async':params.get('is_async'),
            '_return_http_data_only':params.get('_return_http_data_only'),
            '_preload_content':params.get('_preload_content', True),
            '_request_timeout':params.get('_request_timeout'),
            'collection_formats':collection_formats
        }

        return self.api_client.call_api(**call_kwargs)  # noqa: E501

    def __downcase_first_letter(self, s):
        if len(s) == 0:
            return str
        else:
            return s[0].lower() + s[1:]

# coding: utf-8

# --------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="delete_pages_request.py">
#   Copyright (c) 2003-2019 Aspose Pty Ltd
# </copyright>
# <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
# 
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
# 
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# --------------------------------------------------------------------------------

class DeletePagesRequest(object):
    """
    Request model for delete_pages operation.
    :param file_path Document path in storage
    """

    def __init__(self, file_path):
        """Initializes new instance of DeletePagesRequest."""  # noqa: E501
        self.file_path = file_path
# coding: utf-8

# --------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="get_pages_request.py">
#   Copyright (c) 2003-2019 Aspose Pty Ltd
# </copyright>
# <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
# 
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
# 
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# --------------------------------------------------------------------------------

class GetPagesRequest(object):
    """
    Request model for get_pages operation.
    :param file_path Document path in storage
    :param count_pages_to_convert The count pages to convert
    :param page_number The start page number
    :param page_numbers_to_convert The list of page numbers to convert
    :param without_annotations If true returns specific pages without annotations
    :param enable_caching Indicates whether to use previously cached document or not
    :param cache_storage_path The cache storage path
    :param password Source document opening password
    """

    def __init__(self, file_path, count_pages_to_convert=None, page_number=None, page_numbers_to_convert=None, without_annotations=None, enable_caching=None, cache_storage_path=None, password=None):
        """Initializes new instance of GetPagesRequest."""  # noqa: E501
        self.file_path = file_path
        self.count_pages_to_convert = count_pages_to_convert
        self.page_number = page_number
        self.page_numbers_to_convert = page_numbers_to_convert
        self.without_annotations = without_annotations
        self.enable_caching = enable_caching
        self.cache_storage_path = cache_storage_path
        self.password = password
