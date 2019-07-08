import json
import pandas as pd
import numpy as np
import os
import math
import websocket
from websocket import WebSocketConnectionClosedException
from uuid import getnode as get_mac
from virtualitics import exceptions, utils, vip_plot
from virtualitics import task_response_handlers as handlers
from virtualitics import encryption as enc
import virtualitics

LOG_HELP_LEVEL = 1
LOG_DEBUG_LEVEL = 2


# noinspection PyDictCreation
class VIP:
    """
    Virtualitics API handler for Python.

    The class will cache information about the VIP session and establish the VIP connection

    :param auth_token: User to pass Authentication Token; default: `None` will check environment variables for
        token under "VIP_AUTH_TOKEN"
    :param port: The port VIP is serving. default: 12345. Integer in [0, 65535]
    :param encryption_key: Optional encryption key; default: None
    :param host: default is localhost connection. Only change this if you intend on connecting to a remote VIP
        instance. This is an advanced functionality.
    :param log_level: :class:`int` from 0 to 2. 0: quiet, 1: help, 2: debug. Help level will print messages that
        guide the user of important internal events. Debug level will print messages that expose a greater level of
        the internal state, useful for development and debugging purposes. Each level will print what is also printed
        at lower levels.
    :param figsize: :class:`(int, int)` sets the figure size for showing any plots returned from VIP. The
        resolution of the plots shown is controlled by the 'imsize' parameter in the function calls. The default is
        [8, 8].
    :raises AuthenticationException: if the auth token is not provided and cannot be found in the expected
        locations.
    """

    def __init__(self, auth_token=None, port=12345, encryption_key=None, host="ws://localhost", log_level=0,
                 figsize=(8, 8)):
        # Validate argument types of port and log_level
        if not isinstance(port, int) or port < 0 or port > 65535:
            utils.raise_invalid_argument_exception(str(type(port)), "port", "int in [0, 65535]")
        if not isinstance(log_level, int):
            utils.raise_invalid_argument_exception(str(type(log_level)), "log_level",
                                                   [LOG_HELP_LEVEL, LOG_DEBUG_LEVEL, "other integer"])

        if auth_token is None:
            if "VIP_AUTH_TOKEN" in os.environ:
                self.auth_token = os.environ["VIP_AUTH_TOKEN"]
            else:
                raise (
                    exceptions.AuthenticationException("You must provide an Authentication Token as a parameter or " +
                                                       "save it as an environment variable. See documentation."))
        else:
            if not isinstance(auth_token, str):
                raise exceptions.InvalidInputTypeException("auth_token parameter is either None or a string.")

            self.auth_token = auth_token
        if encryption_key is None:
            if "VIP_ENCRYPTION_KEY" in os.environ:
                self.cipher = enc.VIPCipher(os.environ["VIP_ENCRYPTION_KEY"])
            else:
                self.cipher = None
            # it is not required for the user to encrypt their data.
        else:
            if not isinstance(encryption_key, str):
                raise exceptions.InvalidInputTypeException("encryption_key parameter is either None or a string.")
            self.cipher = enc.VIPCipher(encryption_key)

        # WebSocket Connection variables
        self.host = host
        self.port = port
        self.url = self.host + ":" + str(self.port)
        self.max_request_bytes = 1160000000000  # TODO: Adjust for 1.3.0
        self.ws = websocket.WebSocket()
        self.connection_url = self.url + "/api"
        self.debug = None
        self.log_level = log_level
        self.dataset_num = 1
        self._local_history = []
        self.figsize = figsize

        print("Setting up WebSocket connection to: " + self.connection_url)
        try:
            self.ws.connect(self.connection_url)
            print("Connection Successful! Initializing session.")
        except Exception as e:
            print("Connection Failed: " + e.__str__())
        self._api_request()

    def _reconnect(self):
        self.ws.connect(self.connection_url)

    def _send_request(self, payload, pagenum=None):
        """
        All API commands will make use of this function to do the final
        preparations and sending of the request. All requests are made as
        ASYNC POST requests

        :param payload: JSON structure that will be prepped for sending.
        """
        if self.cipher is not None:
            payload = self.cipher.encrypt(payload)
        try:
            self.ws.send_binary(payload)
            raw_response = self.ws.recv()
            if self.cipher is not None:
                raw_response = self.cipher.decrypt(raw_response)
        except ConnectionAbortedError:
            self._reconnect()
            self.ws.send_binary(payload)
            raw_response = self.ws.recv()
            if self.cipher is not None:
                raw_response = self.cipher.decrypt(raw_response)
        except WebSocketConnectionClosedException as e:
            print("There was an issue establishing the WebSocket connection. Here are some things to check: VIP must "
                  "be opened and logged in. You must explicitly launch the API WebSocket server from the settings "
                  "panel unless you have previously selected 'Launch at Login'. Make sure you have specified the "
                  "correct host address and port number for VIP. If you are still having issues connecting to VIP, "
                  "please discuss with your IT team and email 'support@virtualitics.com'. ")
            if self.log_level >= LOG_DEBUG_LEVEL:
                print("Connection Failed: " + e.__str__())
            return

        # Partition raw response
        if isinstance(raw_response, str):
            raise exceptions.ResponseFormatException("There was an issue in parsing the response from the software. "
                                                     "Please try executing the API call again.")
        self.debug = raw_response
        response_size = int(int.from_bytes(raw_response[:4], byteorder='little', signed=True))
        response = utils.decompress(raw_response[4:4 + response_size])
        response_payload = raw_response[4 + response_size:]

        cur_result = handlers.generic_callback(response, response_payload, self.log_level, self.figsize)
        if cur_result is None:
            return
        if cur_result.plot is not None:
            self._local_history.append(cur_result.plot)
        if cur_result.data is not None:
            return cur_result.data
        else:
            return

    def _api_request(self, params=None, data=None):
        """
        API Request formatter; hands off to _send_request
        :param params: defaults to None. parameters encoding VIP tasks
        :param data: defaults to None. data to be sent over to complete VIP tasks
        :return: may return a :class:`virtualitics.VipResult` or None
        """
        # self.params = params  # for debugging

        api_request = {}
        total_payload_size = 0
        api_request["AuthToken"] = self.auth_token
        api_request["ApiVersion"] = virtualitics.__version__
        api_request["ExpectedVIPVersion"] = virtualitics.__latest_compatible_vip_version__
        mac_address = ':'.join(("%012X" % get_mac())[i:i + 2] for i in range(0, 12, 2))
        api_request['MacAddress'] = mac_address
        if params is not None:
            api_request['RequestTasks'] = params
        else:
            api_request['RequestTasks'] = []

        # Encode and compress api_request
        request = json.dumps(api_request)
        request_bytes = utils.compress(request.encode('unicode_escape'))

        if self.log_level >= LOG_DEBUG_LEVEL:
            print(request)

        # The max payload size has to account for the request and the
        # pre-request info. The use of magic number (12)
        max_page_size = self.max_request_bytes - len(request_bytes) - 12
        total_pages = 1
        if total_payload_size > max_page_size:
            # minimum 1 page
            total_pages = math.ceil(total_payload_size / float(max_page_size))

        for i in range(total_pages):
            request_info = np.array([len(request_bytes), i, total_pages - 1])
            info_bytes = request_info.astype(np.int32).tobytes()
            cur_payload = info_bytes + request_bytes
            # get the bytearray that we will send in this request based on page num
            if data is None:
                data = bytearray()
            if total_pages == 1:
                cur_payload += data
            else:
                start_idx = i * max_page_size
                end_idx = start_idx + max_page_size
                if end_idx >= len(data):
                    cur_payload += data[start_idx:]
                else:
                    cur_payload += data[start_idx:end_idx]
            # print(len(cur_payload), self.max_request_bytes)
            return self._send_request(cur_payload, i)

    @property
    def local_history(self):
        """
        This is a list of :class:`VipPlot` instances that were generated by plotting request methods (e.g.
        :func:`VIP.show()`, :func:`VIP.hist()`, etc.) or AI routine methods (e.g. :func:`VIP.smart_mapping()`,
        :func:`VIP.pca()`, etc.). To control whether a :class:`VipPlot` object will be added to 'local_history',
        specify the 'save_to_local_history' parameter in your plotting/AI routine requests. The 'local_history'
        list is different from the :func:`VIP.history()` method, which allows the user to access :class:`VipPlot`
        objects saved to the Virtualitics Immersive Platform History panel.

        :return: :class:`[VipPlot]`
        """
        return self._local_history

    @property
    def log_level(self):
        """
        :class:`int` from 0 to 2. 0: quiet, 1: help, 2: debug. Help level will print messages that
        guide the user of important internal events. Debug level will print messages that expose a greater level of
        the internal state, useful for development and debugging purposes. Each level will print what is also printed
        at lower levels.

        :return: :class:`int`
        """
        return self._log_level

    @log_level.setter
    def log_level(self, value):
        """
        :class:`int` from 0 to 2. 0: quiet, 1: help, 2: debug. Help level will print messages that
        guide the user of important internal events. Debug level will print messages that expose a greater level of
        the internal state, useful for development and debugging purposes. Each level will print what is also printed
        at lower levels.

        :return: :class:`int`
        """
        if not isinstance(value, int):
            utils.raise_invalid_argument_exception(str(type(value)), "log_level",
                                                   "must be an `int` between 0 and 2. See Documentation. ")

        if not (0 <= value <= 2):
            utils.raise_invalid_argument_exception(str(type(value)), "log_level",
                                                   "must be an `int` between 0 and 2. See Documentation. ")

        self._log_level = value

    @property
    def figsize(self):
        """
        This is used as the setting for the matplotlib figure size when displaying the image of plots generated by
        VIP. The default value is (16, 16)

        :return: :class:`(int, int)`
        """
        return self._figsize

    @figsize.setter
    def figsize(self, value):
        """
        This is used as the setting for the matplotlib figure size when displaying the image of plots generated by
        VIP. The default value is (8, 8). Must be set to a :class:`(int, int)`.

        :param value: :class:`(int, int)`
        :return: :class:`None`
        """
        if not hasattr(value, "__iter__"):
            utils.raise_invalid_argument_exception(str(type(value)), "figsize", "must be a `(int, int)` with length "
                                                                                "of 2. The integers must be positive. ")
        if not len(value) == 2:
            utils.raise_invalid_argument_exception(str(type(value)), "figsize", "must be a `(int, int)` with length "
                                                                                "of 2. The integers must be positive. ")
        if not isinstance(value[0], int) or value[0] < 1:
            utils.raise_invalid_argument_exception(str(type(value)), "figsize", "must be a `(int, int)` with length "
                                                                                "of 2. The integers must be positive. ")
        if not isinstance(value[1], int) or value[1] < 1:
            utils.raise_invalid_argument_exception(str(type(value)), "figsize", "must be a `(int, int)` with length "
                                                                                "of 2. The integers must be positive. ")

        self._figsize = value

    def load_project(self, path):
        """
        Loads VIP project file into software from a path local to the machine running VIP. Note that any project
        currently open will be discarded. To save the project first, please use VIP.save_project().

        :param path: :class:`string`
        :return: :class:`None`
        """

        if not isinstance(path, str):
            utils.raise_invalid_argument_exception(str(type(path)), "path", "must be a string. ")

        # Following behavior in save_project(), append vip extension if it does not exist
        if path[-4:] != ".vip":
            path += ".vip"

        params = {"TaskType": "LoadProject", "Path": path}
        self._api_request(params=[params], data=None)

    def load_data(self, data, dataset_name=None):
        """
        Loads pandas dataframe into VIP. Uses column dtype to determine column
        type in VIP.

        :param data: :class:`pandas.DataFrame` object that contains the users data.
        :param dataset_name: optionally pass in a name for this dataset to show in Virtualitics
        :return: :class:`None`
        """
        if dataset_name is not None and not isinstance(dataset_name, str):
            raise exceptions.InvalidInputTypeException("dataset_name should be a string!")
        if not isinstance(data, pd.DataFrame):
            raise exceptions.InvalidInputTypeException("data should be a pd.DataFrame!")

        params = {"TaskType": "DataSet"}
        params['ColumnInfo'] = []
        column_bytes = []
        payload_idx = 0

        # Serialize columns
        for col in list(data.columns):
            serial_col = utils.serialize_column(data[col].values)
            col_info = {"ColumnName": col, "ColumnType": serial_col[0],
                        "BytesSize": serial_col[2],
                        "BytesStartIndex": payload_idx}
            params["ColumnInfo"].append(col_info)
            column_bytes.append(serial_col[1])
            payload_idx += serial_col[2]

        if dataset_name is None or dataset_name == "":
            dataset_name = "user_dataset_{i}".format(i=self.dataset_num)
        params["DataSetName"] = dataset_name
        data_bytes = b"".join(column_bytes)

        output = self._api_request(params=[params], data=data_bytes)

        # Now that data has been successfully loaded into VIP
        # Keep track of current columns and their data types
        self.dataset_num += 1
        return output

    def delete_dataset(self, dataset_name=None):
        """
        Deletes a dataset from VIP. This is particularly useful when you have a lot of datasets loaded into VIP and
        there is a performance slow down. If 'dataset_name' is passed, VIP will delete the dataset with the
        corresponding name. If 'dataset_name' is left as `None`, the currently loaded dataset will be deleted from VIP
        if there is a dataset loaded.

        :param dataset_name: :class:`str` specifying the name of the dataset to delete from VIP. Defaults to
            :class:`None`
        :return: :class:`None`
        """
        params = {"TaskType": "DeleteDataSet"}
        if dataset_name is None:
            params["CurrentDataSet"] = True
        else:
            if not isinstance(dataset_name, str):
                utils.raise_invalid_argument_exception(str(type(dataset_name)), "dataset_name",
                                                       "must be a 'str' specifying name of a dataset loaded into VIP")
            params["CurrentDataSet"] = False
            params["DataSetName"] = dataset_name

        self._api_request(params=[params], data=None)

    def switch_dataset(self, dataset_name: str):
        """
        Switches Dataset context in VIP.

        :param dataset_name: :class:`str` for the name of the dataset to bring into context.
        :return: :class:`None`
        """
        params = {"TaskType": "SwitchDataset"}
        params["DataSetName"] = dataset_name

        self._api_request(params=[params], data=None)

    def save_project(self, filename: str, overwrite=False):
        """
        Saves VIP project to the specified filepath.

        :param filename: absolute or relative path to the desired save location.
        :param overwrite: :class:`bool` that controls whether to write over a file that may exist at the specified path.
        :return: :class:`None`
        """
        try:
            path = os.path.abspath(filename)
            if path[-4:] != ".vip":
                path += ".vip"
            if os.path.isfile(path) and not overwrite:
                raise exceptions.ProjectAlreadyExistsException("There is already a project saved at '" + path + "'. ")
            params = {"TaskType": "SaveProject"}
            params["Path"] = path
        except Exception:
            raise exceptions.InvalidSavePathException("This is not a valid path.")

        self._api_request(params=[params], data=None)

    def convert_column(self, column, column_type: str):
        """
        Converts column to the specified type.

        :param column: expects column name (:class:`str`) or a :class:`pandas.Series`
        :param column_type: {"Continuous", "Categorical"}
        :return: :class:`None`
        """
        col_name = utils.get_name(column)
        column_type = utils.case_insensitive_match(utils.COLUMN_TYPE_CHOICES, column_type, "column_type")

        params = {"TaskType": "ConvertColumn"}
        params["ColumnName"] = col_name
        params["ColumnType"] = column_type

        self._api_request(params=[params], data=None)

    def add_column(self, data, name=None):
        """
        Add a pandas series to the currently loaded dataset in VIP. Uses column dtype to determine column type in VIP.

        :param data: :class:`pandas.core.Series` object that contains a column of the user's data.
        :param name: if not :class:`None`, sets this as the name of the series when it is added.
        :return: :class:`None`
        """
        if not isinstance(data, pd.Series):
            raise exceptions.InvalidInputTypeException("data should be a pd.Series!")

        if name is not None:
            data.rename(name, inplace=True)

        self._add_data([data], "Column")

    def add_rows(self, data):
        """
        Append a pandas data frame of rows to the currently loaded dataset in VIP.

        :param data: :class:`pandas.core.frame.DataFrame` object that contains rows of the user's data.
        :return: :class:`None`
        """
        if not isinstance(data, pd.DataFrame):
            raise exceptions.InvalidInputTypeException("data should be a pd.DataFrame")

        self._add_data([data[c] for c in data.columns], "AddRows")

    def _add_data(self, data, task_type):
        """
        Add a pandas data frame to the currently loaded dataset in VIP. If the number of columns is one, adds the
        data as a new column. Else, appends the data as new rows.

        :param data: :class:`pandas.core.frame.DataFrame` or `pandas.core.Series` object that contains the user's data.
        :param task_type: the type of add_data operation in ['AddRows', `Column`]
        :return: :class:`None`
        """
        params = {"TaskType": task_type}
        params['ColumnInfo'] = []
        data_bytes = []
        payload_idx = 0

        for col in data:
            serial_col = utils.serialize_column(col.values)
            col_info = {"ColumnName": col.name, "ColumnType": serial_col[0], "BytesSize": serial_col[2],
                        "BytesStartIndex": payload_idx}
            params["ColumnInfo"].append(col_info)
            data_bytes.append(serial_col[1])
            payload_idx += serial_col[2]

        data_bytes = b"".join(data_bytes)

        return self._api_request(params=[params], data=data_bytes)

    def filter(self, feature_name, min=None, max=None, include=None, exclude=None, export="ortho", imsize=(2048, 2048),
               path=None, save_to_local_history=True, keep_missing_value_columns=True):
        """
        :param feature_name: Name of feature to add filter to
        :param min: If feature is continuous, set the lower bound of the filter to "min"
        :param max: If feature is continuous, set the upper bound of the filter to "max"
        :param include: If feature is categorical, set these categories to be visible
        :param exclude: If feature is categorical, set these categories to be invisible
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param keep_missing_value_columns: :class:`bool` for whether to keep features with more than 50% missing
            values as part of the input for filtering. Default is `True`.
        :return: :class:`None`
        """
        if not isinstance(keep_missing_value_columns, bool):
            utils.raise_invalid_argument_exception(str(type(keep_missing_value_columns)), "keep_missing_value_columns",
                                                   "must be a `bool`. ")

        params = {"TaskType": "Filter", "Action": "Add", "FeatureName": feature_name}
        if min is not None or max is not None:
            if include or exclude:
                raise exceptions.InvalidInputTypeException("A filter can be applied only when the continuous min/max "
                                                           "or categorical include/exclude arguments are set but not "
                                                           "both")
            if min is not None:
                params["Min"] = min
            if max is not None:
                params["Max"] = max
            params["Type"] = "Continuous"
        elif include or exclude:
            if include:
                if type(include) is not list:
                    include = [str(include)]
                params["Include"] = utils.get_features(include)
            if exclude:
                if type(exclude) is not list:
                    exclude = [str(exclude)]
                params["Exclude"] = utils.get_features(exclude)
            params["Type"] = "Categorical"
        else:
            raise exceptions.InvalidInputTypeException("To apply a filter to %s, either min/max or include/"
                                                       "exclude arguments must be set" % feature_name)

        params["KeepMissingValueColumns"] = keep_missing_value_columns

        params = self._add_export_to_params(export, imsize, path, [params], ignore_no_plot=True)
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        return self._api_request(params=params, data=None)

    def remove_filter(self, feature_name, export="ortho", imsize=(2048, 2048), path=None, save_to_local_history=True):
        """
        :param feature_name: Name of feature to remove any filter on if it exists
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :return: :class:`None`
        """
        params = {"TaskType": "Filter", "Action": "Remove", "FeatureName": feature_name}
        params = self._add_export_to_params(export, imsize, path, [params], ignore_no_plot=True)
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        return self._api_request(params=params, data=None)

    def remove_all_filters(self, export="ortho", imsize=(2048, 2048), path=None, save_to_local_history=True):
        """
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :return: :class:`None`
        """
        params = {"TaskType": "Filter", "Action": "RemoveAll"}
        params = self._add_export_to_params(export, imsize, path, [params], ignore_no_plot=True)
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        return self._api_request(params=params, data=None)

    def get_column(self, feature_name):
        """
        Gets the column named <feature_name> from the currently loaded dataset

        :param feature_name: Name of column to get
        :return: :class:`pandas.core.Series`
        """
        params = {"TaskType": "ColumnSync", "Action": "GetColumn", "FeatureName": feature_name}
        return self._api_request(params=[params], data=None)

    def get_dataset(self, name=None):
        """
        Gets the entire loaded dataset from the software in its current state

        :param name: If specified, get the dataset named <name>. Else, gets the currently loaded dataset.
        :return: :class:`pandas.DataFrame`
        """
        params = {"TaskType": "ColumnSync", "Action": "GetDataset"}
        if name:
            params["Name"] = name
        return self._api_request(params=[params], data=None)

    def pull_new_columns(self):
        """
        Gets new columns that were added to the currently loaded dataset since the last invocation of this method.
        This does not include columns from the initial loading of a dataset (call get_dataset() to access these) or
        columns created from via ML routines, such as clustering and PCA, that have not been added to the feature list.

        :return: :class:`pandas.DataFrame`
        """
        params = {"TaskType": "ColumnSync", "Action": "PullNewColumns"}
        return self._api_request(params=[params], data=None)

    def get_screen(self, export="ortho", imsize=(2048, 2048), path=None, save_to_local_history=True):
        """
        Exports a snapshot of the visible mapping in VIP and fetches a Plot object. If save_to_local_history is set to
        `True`, the VipPlot instance will be appended to the `local_history`

        :return: :class:`None`
        """
        params = []
        params = self._add_export_to_params(export, imsize, path, params)
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        return self._api_request(params=params, data=None)

    def history(self, index=None, name=None, export="ortho", imsize=(2048, 2048), path=None,
                save_to_local_history=True):
        """
        Allows users to re-plot mappings in VIP's history entries for the current dataset. The user must specify a
        desired index (negative indexing is allowed) or pass the name of the desired plot. If there are multiple
        history entries with the requested name, the last entry with the requested name will be plotted. Users
        have the ability to rename a plot through the software. The user should not specify an index and a name in
        the same function call.

        :param index: :class:`int` index to be used on the list of previously created plots through VIP. Default
            value is None. For the past 1...N plots, access via index=[-1 (latest), -N] or index=[0, N - 1 (latest)].
        :param name: :class:`str` plot name checked against the list of previously created plots through VIP. Default
            value is None
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho".
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :return: :class:`None`
        """
        params = {"TaskType": "History"}
        if index is not None and name is not None:
            raise exceptions.InvalidUsageException("Specifying an `index` and `name` for desired history entry "
                                                   "simultaneously is not allowed. ")
        else:
            if index is not None and isinstance(index, int):
                params["Index"] = index
            elif name is not None and isinstance(name, str):
                params["Name"] = name
        params = [params]
        params = self._add_export_to_params(export, imsize, path, params)
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        return self._api_request(params=params, data=None)

    def plot(self, plot_type="scatter", x=None, y=None, z=None, color=None, size=None, shape=None, transparency=None,
             halo=None, halo_highlight=None, pulsation=None, pulsation_highlight=None, playback=None,
             playback_highlight=None, arrow=None, groupby=None, x_scale=None, y_scale=None, z_scale=None,
             size_scale=None, transparency_scale=None, halo_scale=None, arrow_scale=None, color_type=None,
             color_normalization=None, x_normalization=None, y_normalization=None, z_normalization=None,
             size_normalization=None, transparency_normalization=None, arrow_normalization=None, export="ortho",
             imsize=(2048, 2048), path=None, save_to_local_history=True, color_bins=None, color_bin_dist=None,
             name=None):
        """
        Requests VIP to make the specified plot. Expects column name or :class:`pandas.Series` dimension parameters.
        Plot type is expected to be string.

        :param plot_type: {"scatter", "hist", "line", "maps3d", "maps2d", "ellipsoid", "surface", "convex_hull"};
            default is "scatter"
        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param arrow: Arrow dimension. Works with continuous and categorical features.
        :param groupby: Group By dimension. Works with categorical columns.
        :param x_scale: Scaling factor for X dimension. Value must be between .5 and 5.
        :param y_scale: Scaling factor for Y dimension. Value must be between .5 and 5.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "gradient", "bin", or "palette" or None (which uses VIP defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default but "gradient"
            can also be used.
        :param color_normalization: Normalization setting for color. This can only be set if the color type is set to
            "Gradient". The options are "Log10", "Softmax", "IHST"
        :param x_normalization: Normalization setting for X. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param y_normalization: Normalization setting for Y.This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in VIP.
        :return: :class:`None`
        """
        plot_type = utils.case_insensitive_match(utils.PLOT_TYPE_ALIASES, plot_type, "plot_type")
        if plot_type == "SCATTER_PLOT":
            return self.scatter(x=x, y=y, z=z, color=color, size=size, shape=shape, transparency=transparency,
                                halo=halo, halo_highlight=halo_highlight, pulsation=pulsation,
                                pulsation_highlight=pulsation_highlight, playback=playback,
                                playback_highlight=playback_highlight, arrow=arrow, groupby=groupby,
                                x_scale=x_scale, y_scale=y_scale, z_scale=z_scale, size_scale=size_scale,
                                transparency_scale=transparency_scale, halo_scale=halo_scale, arrow_scale=arrow_scale,
                                color_type=color_type, color_normalization=color_normalization,
                                x_normalization=x_normalization, y_normalization=y_normalization,
                                z_normalization=z_normalization, size_normalization=size_normalization,
                                transparency_normalization=transparency_normalization,
                                arrow_normalization=arrow_normalization, export=export, imsize=imsize, path=path,
                                save_to_local_history=save_to_local_history, color_bins=color_bins,
                                color_bin_dist=color_bin_dist, name=name)
        elif plot_type == "LINE_PLOT":
            return self.line(x=x, y=y, z=z, color=color, size=size, shape=shape, transparency=transparency,
                             halo=halo, halo_highlight=halo_highlight, pulsation=pulsation,
                             pulsation_highlight=pulsation_highlight, playback=playback,
                             playback_highlight=playback_highlight, arrow=arrow, groupby=groupby,
                             x_scale=x_scale, y_scale=y_scale, z_scale=z_scale,
                             size_scale=size_scale, transparency_scale=transparency_scale, halo_scale=halo_scale,
                             arrow_scale=arrow_scale, color_type=color_type, x_normalization=x_normalization,
                             y_normalization=y_normalization, z_normalization=z_normalization,
                             size_normalization=size_normalization,
                             transparency_normalization=transparency_normalization,
                             arrow_normalization=arrow_normalization, export=export, imsize=imsize, path=path,
                             save_to_local_history=save_to_local_history, color_bins=color_bins,
                             color_bin_dist=color_bin_dist, name=name)
        elif plot_type == "VIOLIN_PLOT":
            return self.violin(x=x, y=y, z=z, color=color, size=size, shape=shape, transparency=transparency,
                               halo=halo, halo_highlight=halo_highlight, pulsation=pulsation,
                               pulsation_highlight=pulsation_highlight, playback=playback,
                               playback_highlight=playback_highlight, arrow=arrow, groupby=groupby,
                               x_scale=x_scale, y_scale=y_scale, z_scale=z_scale,
                               size_scale=size_scale, transparency_scale=transparency_scale, halo_scale=halo_scale,
                               arrow_scale=arrow_scale, color_type=color_type, color_normalization=color_normalization,
                               x_normalization=x_normalization, y_normalization=y_normalization,
                               z_normalization=z_normalization, size_normalization=size_normalization,
                               transparency_normalization=transparency_normalization,
                               arrow_normalization=arrow_normalization, export=export, imsize=imsize, path=path,
                               save_to_local_history=save_to_local_history, color_bins=color_bins,
                               color_bin_dist=color_bin_dist, name=name)
        elif plot_type == "CONVEX_HULL":
            return self.convex_hull(x=x, y=y, z=z, color=color, size=size, shape=shape, transparency=transparency,
                                    halo=halo, halo_highlight=halo_highlight, pulsation=pulsation,
                                    pulsation_highlight=pulsation_highlight, playback=playback,
                                    playback_highlight=playback_highlight, arrow=arrow, groupby=groupby,
                                    x_scale=x_scale, y_scale=y_scale, z_scale=z_scale,
                                    size_scale=size_scale, transparency_scale=transparency_scale, halo_scale=halo_scale,
                                    arrow_scale=arrow_scale, color_type=color_type, x_normalization=x_normalization,
                                    y_normalization=y_normalization, z_normalization=z_normalization,
                                    size_normalization=size_normalization,
                                    transparency_normalization=transparency_normalization,
                                    arrow_normalization=arrow_normalization, export=export, imsize=imsize, path=path,
                                    save_to_local_history=save_to_local_history, color_bins=color_bins,
                                    color_bin_dist=color_bin_dist, name=name)
        elif plot_type == "CONFIDENCE_ELLIPSOID":
            return self.ellipsoid(x=x, y=y, z=z, color=color, size=size, shape=shape, transparency=transparency,
                                  halo=halo, halo_highlight=halo_highlight, pulsation=pulsation,
                                  pulsation_highlight=pulsation_highlight, playback=playback,
                                  playback_highlight=playback_highlight, arrow=arrow, groupby=groupby,
                                  x_scale=x_scale, y_scale=y_scale, z_scale=z_scale,
                                  size_scale=size_scale, transparency_scale=transparency_scale, halo_scale=halo_scale,
                                  arrow_scale=arrow_scale, color_type=color_type, x_normalization=x_normalization,
                                  y_normalization=y_normalization, z_normalization=z_normalization,
                                  size_normalization=size_normalization,
                                  transparency_normalization=transparency_normalization,
                                  arrow_normalization=arrow_normalization, export=export, imsize=imsize, path=path,
                                  save_to_local_history=save_to_local_history, color_bins=color_bins,
                                  color_bin_dist=color_bin_dist, name=name)
        elif plot_type == "HISTOGRAM":
            return self.hist(x=x, y=y, z=z, color=color, size=size, shape=shape, transparency=transparency,
                             halo=halo, halo_highlight=halo_highlight, pulsation=pulsation,
                             pulsation_highlight=pulsation_highlight, playback=playback,
                             playback_highlight=playback_highlight, arrow=arrow, groupby=groupby,
                             x_scale=x_scale, y_scale=y_scale, z_scale=z_scale, size_scale=size_scale,
                             transparency_scale=transparency_scale, halo_scale=halo_scale, arrow_scale=arrow_scale,
                             color_type=color_type, x_normalization=x_normalization, y_normalization=y_normalization,
                             z_normalization=z_normalization, size_normalization=size_normalization,
                             transparency_normalization=transparency_normalization,
                             arrow_normalization=arrow_normalization, export=export, imsize=imsize, path=path,
                             save_to_local_history=save_to_local_history, color_bins=color_bins,
                             color_bin_dist=color_bin_dist, name=name)
        elif plot_type == "MAPS2D":
            return self.maps2d(x=x, y=y, z=z, color=color, size=size, shape=shape, transparency=transparency,
                               halo=halo, halo_highlight=halo_highlight, pulsation=pulsation,
                               pulsation_highlight=pulsation_highlight, playback=playback, groupby=groupby,
                               size_scale=size_scale, transparency_scale=transparency_scale, halo_scale=halo_scale,
                               color_type=color_type, color_normalization=color_normalization,
                               size_normalization=size_normalization,
                               transparency_normalization=transparency_normalization, export="front", imsize=imsize,
                               path=path, save_to_local_history=save_to_local_history, color_bins=color_bins,
                               color_bin_dist=color_bin_dist, name=name)
        elif plot_type == "MAPS3D":
            return self.maps3d(x=x, y=y, z=z, color=color, size=size, shape=shape, transparency=transparency,
                               halo=halo, halo_highlight=halo_highlight, pulsation=pulsation,
                               pulsation_highlight=pulsation_highlight, playback=playback,
                               playback_highlight=playback_highlight, groupby=groupby,
                               size_scale=size_scale, transparency_scale=transparency_scale, halo_scale=halo_scale,
                               color_type=color_type, color_normalization=color_normalization,
                               size_normalization=size_normalization,
                               transparency_normalization=transparency_normalization, export=export, imsize=imsize,
                               path=path, save_to_local_history=save_to_local_history, color_bins=color_bins,
                               color_bin_dist=color_bin_dist, name=name)
        elif plot_type == "SURFACE":
            return self.surface(x=x, y=y, z=z, color=color, size=size, shape=shape, transparency=transparency,
                                halo=halo, halo_highlight=halo_highlight, pulsation=pulsation,
                                pulsation_highlight=pulsation_highlight, playback=playback,
                                playback_highlight=playback_highlight, arrow=arrow, groupby=groupby,
                                x_scale=x_scale, y_scale=y_scale, z_scale=z_scale,
                                size_scale=size_scale, transparency_scale=transparency_scale, halo_scale=halo_scale,
                                arrow_scale=arrow_scale, color_type=color_type, color_normalization=color_normalization,
                                x_normalization=x_normalization, y_normalization=y_normalization,
                                z_normalization=z_normalization, size_normalization=size_normalization,
                                transparency_normalization=transparency_normalization,
                                arrow_normalization=arrow_normalization, export=export, imsize=imsize, path=path,
                                save_to_local_history=save_to_local_history, color_bins=color_bins,
                                color_bin_dist=color_bin_dist, name=name)

    def scatter(self, x=None, y=None, z=None, color=None, size=None, shape=None, transparency=None, halo=None,
                halo_highlight=None, pulsation=None, pulsation_highlight=None, playback=None, playback_highlight=None,
                arrow=None, groupby=None, x_scale=None, y_scale=None, z_scale=None, size_scale=None,
                transparency_scale=None, halo_scale=None, arrow_scale=None, color_type=None, color_normalization=None,
                x_normalization=None, y_normalization=None, z_normalization=None, size_normalization=None,
                transparency_normalization=None, arrow_normalization=None, export="ortho", imsize=(2048, 2048),
                path=None, save_to_local_history=True, color_bins=None, color_bin_dist=None, name=None):
        """
        Generates scatter plot in VIP. Expects column name or pandas data series dimension parameters.

        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param arrow: Arrow dimension. Works with continuous and categorical features.
        :param groupby: Group By dimension. Works with categorical columns.
        :param x_scale: Scaling factor for X dimension. Value must be between .5 and 5.
        :param y_scale: Scaling factor for Y dimension. Value must be between .5 and 5.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "gradient", "bin", or "palette" or None (which uses VIP defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default but "gradient"
            can also be used.
        :param color_normalization: Normalization setting for color. This can only be set if the color type is set to
            "Gradient". The options are "Log10", "Softmax", "IHST"
        :param x_normalization: Normalization setting for X. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param y_normalization: Normalization setting for Y.This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in VIP.
        :return: :class:`None`
        """
        # Pass dimension info
        plot = vip_plot.VipPlot(plot_type="SCATTER", x=x, y=y, z=z, color=color, size=size, shape=shape,
                                transparency=transparency, halo=halo, halo_highlight=halo_highlight,
                                pulsation=pulsation, pulsation_highlight=pulsation_highlight, playback=playback,
                                playback_highlight=playback_highlight, arrow=arrow, groupby=groupby, x_scale=x_scale,
                                y_scale=y_scale, z_scale=z_scale, size_scale=size_scale,
                                transparency_scale=transparency_scale, halo_scale=halo_scale, arrow_scale=arrow_scale,
                                color_type=color_type, color_normalization=color_normalization,
                                x_normalization=x_normalization, y_normalization=y_normalization,
                                z_normalization=z_normalization, size_normalization=size_normalization,
                                transparency_normalization=transparency_normalization,
                                arrow_normalization=arrow_normalization, color_bins=color_bins,
                                color_bin_dist=color_bin_dist, name=name)
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        params = self._add_export_to_params(export, imsize, path, params)
        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def hist(self, x=None, y=None, z=None, color=None, size=None, shape=None, transparency=None, halo=None,
             halo_highlight=None, pulsation=None, pulsation_highlight=None, playback=None, arrow=None, groupby=None,
             x_scale=None, y_scale=None, z_scale=None, size_scale=None, transparency_scale=None, halo_scale=None,
             arrow_scale=None, color_type=None, x_normalization=None, y_normalization=None, z_normalization=None,
             size_normalization=None, transparency_normalization=None, arrow_normalization=None, export="ortho",
             imsize=(2048, 2048), path=None, save_to_local_history=True, color_bins=None, color_bin_dist=None,
             volume_by=None, x_bins=None, y_bins=None, z_bins=None, name=None):
        """
        Generates Histogram in VIP. Expects column name or pandas data series dimension parameters.

        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param groupby: Group By dimension. Works with categorical columns.
        :param arrow: Arrow dimension. Works with continuous and categorical features. The arrow dimension is not
            visible for this plot type.
        :param x_scale: Scaling factor for X dimension. Value must be between .5 and 5.
        :param y_scale: Scaling factor for Y dimension. Value must be between .5 and 5.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "bin" or "palette" or None (which uses VIP defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default.
        :param x_normalization: Normalization setting for X. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param y_normalization: Normalization setting for Y.This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param volume_by: setting for metric used for height of histogram bins; {"count", "avg", "sum"}
        :param x_bins: :class:`int` between 1 and 1000 that sets the number of bins to use in the 'x' dimension
        :param y_bins: :class:`int` between 1 and 1000 that sets the number of bins to use in the 'y' dimension
        :param z_bins: :class:`int` between 1 and 1000 that sets the number of bins to use in the 'z' dimension
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in VIP.
        :return: :class:`None`
        """
        # Pass dimension info
        plot = vip_plot.VipPlot(plot_type="HISTOGRAM", x=x, y=y, z=z, color=color, size=size, shape=shape,
                                transparency=transparency, halo=halo, halo_highlight=halo_highlight,
                                pulsation=pulsation, pulsation_highlight=pulsation_highlight, arrow=arrow,
                                playback=playback, groupby=groupby, x_scale=x_scale, y_scale=y_scale, z_scale=z_scale,
                                size_scale=size_scale, transparency_scale=transparency_scale, halo_scale=halo_scale,
                                arrow_scale=arrow_scale, color_type=color_type, x_normalization=x_normalization,
                                y_normalization=y_normalization, z_normalization=z_normalization,
                                size_normalization=size_normalization,
                                transparency_normalization=transparency_normalization,
                                arrow_normalization=arrow_normalization, color_bins=color_bins,
                                color_bin_dist=color_bin_dist, hist_volume_by=volume_by, x_bins=x_bins,
                                y_bins=y_bins, z_bins=z_bins, name=name)
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        params = self._add_export_to_params(export, imsize, path, params)
        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def line(self, x=None, y=None, z=None, show_points=True, color=None, size=None, shape=None, transparency=None,
             halo=None, halo_highlight=None, pulsation=None, pulsation_highlight=None, playback=None,
             playback_highlight=None, arrow=None, groupby=None, x_scale=None, y_scale=None, z_scale=None,
             size_scale=None, transparency_scale=None, halo_scale=None, arrow_scale=None, color_type=None,
             x_normalization=None, y_normalization=None, z_normalization=None, size_normalization=None,
             transparency_normalization=None, arrow_normalization=None, export="ortho", imsize=(2048, 2048), path=None,
             save_to_local_history=True, color_bins=None, color_bin_dist=None, viewby=None, name=None):
        """
        Generates line plot in VIP. Expects column name or pandas data series dimension parameters.

        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param show_points: Setting for how to view the confidence ellipsoids. Valid options are {True, False, "show",
            "hide"}
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param arrow: Arrow dimension. Works with continuous and categorical features.
        :param groupby: Group By dimension. Works with categorical columns.
        :param x_scale: Scaling factor for X dimension. Value must be between .5 and 5.
        :param y_scale: Scaling factor for Y dimension. Value must be between .5 and 5.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "bin" or "palette" or None (which uses VIP defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default.
        :param x_normalization: Normalization setting for X. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param y_normalization: Normalization setting for Y.This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param viewby: :class:'str' Specify the line plot series grouping dimension. Options are {"color", "groupby"}.
            The default option is "color"
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in VIP.
        :return: :class:`None`
        """
        # Pass dimension info
        plot = vip_plot.VipPlot(plot_type="LINE_PLOT", x=x, y=y, z=z, color=color, size=size, shape=shape,
                                transparency=transparency, halo=halo, halo_highlight=halo_highlight,
                                pulsation=pulsation, pulsation_highlight=pulsation_highlight, playback=playback,
                                playback_highlight=playback_highlight, arrow=arrow, groupby=groupby, x_scale=x_scale,
                                y_scale=y_scale, z_scale=z_scale, size_scale=size_scale,
                                transparency_scale=transparency_scale, halo_scale=halo_scale,
                                arrow_scale=arrow_scale, color_type=color_type, x_normalization=x_normalization,
                                y_normalization=y_normalization, z_normalization=z_normalization,
                                size_normalization=size_normalization,
                                transparency_normalization=transparency_normalization,
                                arrow_normalization=arrow_normalization, color_bins=color_bins,
                                color_bin_dist=color_bin_dist, name=name, show_points=show_points, viewby=viewby)
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        params = self._add_export_to_params(export, imsize, path, params)
        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def maps3d(self, x=None, y=None, z=None, color=None, size=None, shape=None, transparency=None, halo=None,
               halo_highlight=None, pulsation=None, pulsation_highlight=None, playback=None, playback_highlight=None,
               groupby=None, arrow=None, z_scale=None, size_scale=None, transparency_scale=None, halo_scale=None,
               arrow_scale=None, color_type=None, z_normalization=None, color_normalization=None,
               size_normalization=None, transparency_normalization=None, arrow_normalization=None, export="ortho",
               imsize=(2048, 2048), path=None, save_to_local_history=True, lat_long_lines=True, country_lines=None,
               country_labels=None, globe_style="natural", heatmap_enabled=False, heatmap_detail=None,
               heatmap_feature=False, return_data=False, color_bins=None, color_bin_dist=None, name=None):
        """
        Generates 3D Map plot in VIP. Expects column name or pandas data series dimension parameters.

        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param arrow: Arrow dimension. Works with continuous and categorical features. The arrow dimension is not
            visible for this plot type.
        :param groupby: Group By dimension. Works with categorical columns.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "gradient", "bin", or "palette" or None (which uses VIP defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default but "gradient"
            can also be used.
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param color_normalization: Normalization setting for color. This can only be set if the color type is set to
            "Gradient". The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param lat_long_lines: :class:`bool` visibility setting for Latitude/Longitude lines.
        :param country_lines: :class:`bool` visibility setting for country border lines.
        :param country_labels: :class:`bool` visibility setting for country labels.
        :param globe_style: {"natural", "dark"}
        :param heatmap_enabled: :class:`bool` setting for whether to use heatmap of the mapped data.
        :param heatmap_detail: :class:`float` to determine the resolution of the heatmap. heatmap_enabled must be True
            for this parameter to be used.
        :param heatmap_feature: :class:`bool` to determine whether to compute a heatmap feature (computes density of
            points).
        :param return_data: :class:`bool` to determine whether to send back the computed heatmap feature.
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in VIP.
        :return: :class:`None` or :class:`pd.DataFrame` if return_data is True for heatmap_feature
        """
        # Pass dimension info
        plot = vip_plot.VipPlot(plot_type="MAPS3D", x=x, y=y, z=z, color=color, size=size, shape=shape,
                                transparency=transparency, halo=halo, halo_highlight=halo_highlight,
                                pulsation=pulsation, pulsation_highlight=pulsation_highlight, playback=playback,
                                playback_highlight=playback_highlight, groupby=groupby, arrow=arrow,
                                z_scale=z_scale, size_scale=size_scale, transparency_scale=transparency_scale,
                                halo_scale=halo_scale, arrow_scale=arrow_scale, color_type=color_type,
                                z_normalization=z_normalization, color_normalization=color_normalization,
                                size_normalization=size_normalization, arrow_normalization=arrow_normalization,
                                transparency_normalization=transparency_normalization, lat_long_lines=lat_long_lines,
                                country_lines=country_lines, country_labels=country_labels, globe_style=globe_style,
                                heatmap_enabled=heatmap_enabled, heatmap_detail=heatmap_detail, color_bins=color_bins,
                                color_bin_dist=color_bin_dist, name=name)
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        params = self._add_export_to_params(export, imsize, path, params)
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        if heatmap_enabled:
            params = self._add_heatmap_feature_to_params(params, heatmap_feature, return_data)
        elif heatmap_feature:
            utils.raise_invalid_argument_exception(str(type(heatmap_feature)), "heatmap_feature",
                                                   "'heatmap_feature' is only applicable when 'heatmap_enabled' has "
                                                   "been set to `True`. ")

        return self._api_request(params=params, data=None)

    def maps2d(self, x=None, y=None, z=None, color=None, size=None, shape=None, transparency=None, halo=None,
               halo_highlight=None, pulsation=None, pulsation_highlight=None, playback=None, playback_highlight=None,
               arrow=None, groupby=None, z_scale=None, size_scale=None, transparency_scale=None, halo_scale=None,
               arrow_scale=None, color_type=None, z_normalization=None, color_normalization=None,
               size_normalization=None, transparency_normalization=None, arrow_normalization=None, export="front",
               imsize=(2048, 2048), path=None, save_to_local_history=True, map_provider="ArcGIS",
               map_style="Topographic", heatmap_enabled=False, heatmap_detail=None, heatmap_feature=False,
               return_data=False, color_bins=None, color_bin_dist=None, name=None):
        """
        Generates 2D Map plot in VIP. Expects column name or pandas data series dimension parameters.

        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param groupby: Group By dimension. Works with categorical columns.
        :param arrow: Arrow dimension. Works with continuous and categorical features. The arrow dimension is not
            visible for this plot type.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "gradient", "bin", or "palette" or None (which uses VIP defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default but "gradient"
            can also be used.
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param color_normalization: Normalization setting for color. This can only be set if the color type is set to
            "Gradient". The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param map_provider: {"ArcGIS", "Stamen", "OpenStreetMap"}
        :param map_style: depends on the map_provider. See documentation for options.
        :param heatmap_enabled: :class:`bool` setting for whether to use heatmap of the mapped data.
        :param heatmap_detail: :class:`float` to determine the resolution of the heatmap. heatmap_enabled must be True
            for this parameter to be used.
        :param heatmap_feature: :class:`bool` to determine whether to compute a heatmap feature (computes density of
            points).
        :param return_data: :class:`bool` to determine whether to send back the computed heatmap feature.
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in VIP.
        :return: :class:`None` or :class:`pd.DataFrame` if return_data is True for heatmap_feature

        """
        # Pass dimension info
        plot = vip_plot.VipPlot(plot_type="MAPS2D", x=x, y=y, z=z, color=color, size=size, shape=shape,
                                transparency=transparency, halo=halo, halo_highlight=halo_highlight,
                                pulsation=pulsation, pulsation_highlight=pulsation_highlight, playback=playback,
                                playback_highlight=playback_highlight, groupby=groupby, arrow=arrow,
                                z_scale=z_scale, size_scale=size_scale, transparency_scale=transparency_scale,
                                halo_scale=halo_scale, arrow_scale=arrow_scale, color_type=color_type,
                                z_normalization=z_normalization, color_normalization=color_normalization,
                                size_normalization=size_normalization, arrow_normalization=arrow_normalization,
                                transparency_normalization=transparency_normalization, heatmap_enabled=heatmap_enabled,
                                heatmap_detail=heatmap_detail, map_provider=map_provider,
                                map_style=map_style, color_bins=color_bins, color_bin_dist=color_bin_dist, name=name)
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        params = self._add_export_to_params(export, imsize, path, params)
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        if heatmap_enabled:
            params = self._add_heatmap_feature_to_params(params, heatmap_feature, return_data)
        elif heatmap_feature:
            utils.raise_invalid_argument_exception(str(type(heatmap_feature)), "heatmap_feature",
                                                   "'heatmap_feature' is only applicable when 'heatmap_enabled' has "
                                                   "been set to `True`. ")

        return self._api_request(params=params, data=None)

    def ellipsoid(self, confidence=95.0, show_points=True, x=None, y=None, z=None, color=None, size=None, shape=None,
                  transparency=None, halo=None, halo_highlight=None, pulsation=None, pulsation_highlight=None,
                  playback=None, playback_highlight=None, arrow=None, groupby=None, x_scale=None, y_scale=None,
                  z_scale=None, size_scale=None, transparency_scale=None, halo_scale=None, arrow_scale=None,
                  color_type=None, x_normalization=None, y_normalization=None, z_normalization=None,
                  size_normalization=None, transparency_normalization=None, arrow_normalization=None, export="ortho",
                  imsize=(2048, 2048), path=None, save_to_local_history=True, color_bins=None, color_bin_dist=None,
                  name=None):
        """
        Generates Ellipsoid plot in VIP. Expects column name or pandas data series dimension parameters.

        :param confidence: :class:`float` confidence probability that must be in {99.5, 99.0, 97.5, 95.0, 90.0, 80.0,
            75.0, 70.0, 50.0, 30.0, 25.0, 20.0, 10.0, 5.0, 2.5, 1.0, 0.5}
        :param show_points: Setting for how to view the confidence ellipsoids. Valid options are {True, False, "show",
            "hide"}
        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param arrow: Arrow dimension. Works with continuous and categorical features.
        :param groupby: Group By dimension. Works with categorical columns.
        :param x_scale: Scaling factor for X dimension. Value must be between .5 and 5.
        :param y_scale: Scaling factor for Y dimension. Value must be between .5 and 5.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "bin" or "palette" or None (which uses VIP defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default.
        :param x_normalization: Normalization setting for X. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param y_normalization: Normalization setting for Y.This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in VIP.
        :return: :class:`None`

        """
        # Pass dimension info
        plot = vip_plot.VipPlot(plot_type="CONFIDENCE_ELLIPSOID", x=x, y=y, z=z, color=color, size=size, shape=shape,
                                transparency=transparency, halo=halo, halo_highlight=halo_highlight,
                                pulsation=pulsation, pulsation_highlight=pulsation_highlight, playback=playback,
                                playback_highlight=playback_highlight, arrow=arrow, groupby=groupby, x_scale=x_scale,
                                y_scale=y_scale, z_scale=z_scale, size_scale=size_scale,
                                transparency_scale=transparency_scale, halo_scale=halo_scale,
                                arrow_scale=arrow_scale, color_type=color_type, x_normalization=x_normalization,
                                y_normalization=y_normalization, z_normalization=z_normalization,
                                size_normalization=size_normalization,
                                transparency_normalization=transparency_normalization,
                                arrow_normalization=arrow_normalization, confidence=confidence, show_points=show_points,
                                color_bins=color_bins, color_bin_dist=color_bin_dist, name=name)
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        params = self._add_export_to_params(export, imsize, path, params)
        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def convex_hull(self, show_points=True, x=None, y=None, z=None, color=None, size=None, shape=None,
                    transparency=None, halo=None, halo_highlight=None, pulsation=None, pulsation_highlight=None,
                    playback=None, playback_highlight=None, arrow=None, groupby=None, x_scale=None, y_scale=None,
                    z_scale=None, size_scale=None, transparency_scale=None, halo_scale=None, arrow_scale=None,
                    color_type=None, x_normalization=None, y_normalization=None, z_normalization=None,
                    size_normalization=None, transparency_normalization=None, arrow_normalization=None, export="ortho",
                    imsize=(2048, 2048), path=None, save_to_local_history=True, color_bins=None, color_bin_dist=None,
                    name=None):
        """
        Generates Convex Hull plot in VIP. Expects column name or pandas data series dimension parameters.

        :param show_points: Setting for how to view the convex hull. Valid options are {True, False, "show", "hide"}
        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param arrow: Arrow dimension. Works with continuous and categorical features.
        :param groupby: Group By dimension. Works with categorical columns.
        :param x_scale: Scaling factor for X dimension. Value must be between 5 and 5.
        :param y_scale: Scaling factor for Y dimension. Value must be between .5 and 5.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "bin" or "palette" or None (which uses VIP defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default.
        :param x_normalization: Normalization setting for X. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param y_normalization: Normalization setting for Y.This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in VIP.
        :return: :class:`None`
        """
        plot = vip_plot.VipPlot(plot_type="CONVEX_HULL", x=x, y=y, z=z, color=color, size=size, shape=shape,
                                transparency=transparency, halo=halo, halo_highlight=halo_highlight,
                                pulsation=pulsation, pulsation_highlight=pulsation_highlight, playback=playback,
                                playback_highlight=playback_highlight, arrow=arrow, groupby=groupby, x_scale=x_scale,
                                y_scale=y_scale, z_scale=z_scale, size_scale=size_scale,
                                transparency_scale=transparency_scale, halo_scale=halo_scale,
                                arrow_scale=arrow_scale, color_type=color_type, x_normalization=x_normalization,
                                y_normalization=y_normalization, z_normalization=z_normalization,
                                size_normalization=size_normalization,
                                transparency_normalization=transparency_normalization,
                                arrow_normalization=arrow_normalization, show_points=show_points, color_bins=color_bins,
                                color_bin_dist=color_bin_dist, name=name)
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        params = self._add_export_to_params(export, imsize, path, params)
        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def violin(self, x=None, y=None, z=None, color=None, size=None, shape=None, transparency=None, halo=None,
               halo_highlight=None, pulsation=None, pulsation_highlight=None, playback=None, playback_highlight=None,
               arrow=None, groupby=None, x_scale=None, y_scale=None, z_scale=None, size_scale=None,
               transparency_scale=None, halo_scale=None, arrow_scale=None, color_type=None, color_normalization=None,
               x_normalization=None, y_normalization=None, z_normalization=None, size_normalization=None,
               transparency_normalization=None, arrow_normalization=None, export="ortho", imsize=(2048, 2048),
               path=None, save_to_local_history=True, color_bins=None, color_bin_dist=None, name=None):
        """
        Generates violin plot in VIP. Expects column name or pandas data series dimension parameters.

        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param arrow: Arrow dimension. Works with continuous and categorical features.
        :param groupby: Group By dimension. Works with categorical columns.
        :param x_scale: Scaling factor for X dimension. Value must be between 5 and 5.
        :param y_scale: Scaling factor for Y dimension. Value must be between .5 and 5.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "gradient", "bin", or "palette" or None (which uses VIP defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default but "gradient"
            can also be used.
        :param color_normalization: Normalization setting for color. This can only be set if the color type is set to
            "Gradient". The options are "Log10", "Softmax", "IHST"
        :param x_normalization: Normalization setting for X. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param y_normalization: Normalization setting for Y.This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in VIP.
        :return: :class:`None`
        """
        plot = vip_plot.VipPlot(plot_type="VIOLIN_PLOT", x=x, y=y, z=z, color=color, size=size, shape=shape,
                                transparency=transparency, halo=halo, halo_highlight=halo_highlight,
                                pulsation=pulsation, pulsation_highlight=pulsation_highlight, playback=playback,
                                playback_highlight=playback_highlight, arrow=arrow, groupby=groupby, x_scale=x_scale,
                                y_scale=y_scale, z_scale=z_scale, size_scale=size_scale,
                                transparency_scale=transparency_scale, halo_scale=halo_scale,
                                arrow_scale=arrow_scale, color_type=color_type, color_normalization=color_normalization,
                                x_normalization=x_normalization, y_normalization=y_normalization,
                                z_normalization=z_normalization, size_normalization=size_normalization,
                                transparency_normalization=transparency_normalization,
                                arrow_normalization=arrow_normalization, color_bins=color_bins,
                                color_bin_dist=color_bin_dist, name=name)
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        params = self._add_export_to_params(export, imsize, path, params)
        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def surface(self, show_points=False, x=None, y=None, z=None, color=None, size=None, shape=None, transparency=None,
                halo=None, halo_highlight=None, pulsation=None, pulsation_highlight=None, playback=None,
                playback_highlight=None, arrow=None, groupby=None, x_scale=None, y_scale=None, z_scale=None,
                size_scale=None, transparency_scale=None, halo_scale=None, arrow_scale=None, color_type=None,
                color_normalization=None, x_normalization=None, y_normalization=None, z_normalization=None,
                size_normalization=None, transparency_normalization=None, arrow_normalization=None, export="ortho",
                imsize=(2048, 2048), path=None, save_to_local_history=True, color_bins=None, color_bin_dist=None,
                name=None):
        """
        Generates Surface plot in VIP. Expects column name or pandas data series dimension parameters.

        :param show_points: Setting for how to view the surface. Valid options are {True, False, "show", "hide"}
        :param x: X dimension
        :param y: Y dimension
        :param z: Z dimension
        :param color: Color dimension. Automatically uses quartile/categorical coloring.
        :param size: Size dimension. Works best with continuous features
        :param shape: Shape dimension. Works best with categorical features
        :param transparency: Transparency dimension. Works best with continuous features.
        :param halo: Halo dimension. Works with binary features
        :param halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points
            with this value will show a halo.
        :param pulsation: Pulsation dimension. Works best with categorical features
        :param pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension.
            All points with this value will pulsate.
        :param playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
        :param playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension.
            All points with this value will be shown and all other points will be hidden.
        :param arrow: Arrow dimension. Works with continuous and categorical features.
        :param groupby: Group By dimension. Works with categorical columns.
        :param x_scale: Scaling factor for X dimension. Value must be between .5 and 5.
        :param y_scale: Scaling factor for Y dimension. Value must be between .5 and 5.
        :param z_scale: Scaling factor for Z dimension. Value must be between .5 and 5.
        :param size_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 5.
        :param halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 5.
        :param arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 5.
        :param color_type: User can select "gradient", "bin", or "palette" or None (which uses VIP defaults). For
            categorical data, the only option is color "palette". For numeric data, "bin" is the default but "gradient"
            can also be used.
        :param color_normalization: Normalization setting for color. This can only be set if the color type is set to
            "Gradient". The options are "Log10", "Softmax", "IHST"
        :param x_normalization: Normalization setting for X. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param y_normalization: Normalization setting for Y.This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this
            dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param transparency_normalization: Normalization setting for Transparency.This can only be set if the feature
            mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to
            this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST"
        :param export: Specify whether to export a capture of the plot. Defaults to "ortho". Options are {"ortho",
            "front", "right", "side" (same as "right"), "top", "perspective", `None`, `False`}.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least
            as many unique values (in the column mapped to color) as the number of bins you set.
        :param color_bin_dist: :class:`str` with options: {"equal", "range"}
        :param name: :class:`str` specifying the name of the plot. Default to None. A name will be automatically
            generated in VIP.
        :return: :class:`None`
        """
        plot = vip_plot.VipPlot(plot_type="SURFACE", x=x, y=y, z=z, color=color, size=size, shape=shape,
                                transparency=transparency, halo=halo, halo_highlight=halo_highlight,
                                pulsation=pulsation, pulsation_highlight=pulsation_highlight, playback=playback,
                                playback_highlight=playback_highlight, arrow=arrow, groupby=groupby, x_scale=x_scale,
                                y_scale=y_scale, z_scale=z_scale, size_scale=size_scale,
                                transparency_scale=transparency_scale, halo_scale=halo_scale, arrow_scale=arrow_scale,
                                color_type=color_type, color_normalization=color_normalization,
                                x_normalization=x_normalization, y_normalization=y_normalization,
                                z_normalization=z_normalization, size_normalization=size_normalization,
                                transparency_normalization=transparency_normalization,
                                arrow_normalization=arrow_normalization, show_points=show_points, color_bins=color_bins,
                                color_bin_dist=color_bin_dist, name=name)
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        params = self._add_export_to_params(export, imsize, path, params)
        params = self._add_plot_mapping_to_params(params, save_to_local_history)

        return self._api_request(params=params, data=None)

    def show(self, plot: vip_plot.VipPlot, display=True, save_to_local_history=True, export="ortho",
             imsize=(2048, 2048), path=None):
        """
        Recreates a plot in VIP from a VipPlot instance.

        :param plot: VipPlot instance that contains all important details to send to VIP
        :param display: :class:`bool` flag for whether to show this plot to the user
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param export: Specify whether to export a capture of the plot. defaults to "ortho". If the plot type is
            "MAPS2D", the export setting will be set to "front" regardless of requested parameter, unless the user
            passes `None`/`False`.
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :return: :class:`None`
        """
        if not isinstance(plot, vip_plot.VipPlot):
            utils.raise_invalid_argument_exception(str(type(plot)), 'plot',
                                                   'must be a VipPlot object instance. ')
        params = [plot.get_params()]

        export = self._update_invalid_export_view(plot, export)

        if display:
            params = self._add_export_to_params(export, imsize, path, params)
            params = self._add_plot_mapping_to_params(params, save_to_local_history)
        return self._api_request(params=params, data=None)

    def smart_mapping(self, target, features=None, exclude=None, export="ortho", imsize=(2048, 2048),
                      return_results_df=False, path=None, save_to_local_history=True,
                      keep_missing_value_columns=True):
        """
        Runs smart mapping in VIP.

        :param target: Target column that the user wants to find insights about; this feature will be dropped
            automatically from Smart Mapping input regardless of what is listed in the `features` and `exclude`
            parameters.
        :param features: List of column names that user wants to analyze in comparison to target
        :param exclude: List of column names to exclude in the analysis; this overrides any features listed in the
            `features` parameter.
        :param return_results_df: :class:`bool` for whether to return the feature ranking and correlation groups
            :class:`pd.DataFrame`. The default is `False`; in which case the head of the feature ranking
            :class:`pd.DataFrame` is displayed.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param keep_missing_value_columns: :class:`bool` for whether to keep features with more than 50% missing
            values as part of the input for smart mapping. Default is `True`.
        :return: if 'return_results_df' is `True`, this returns the feature importance and correlation groups of
            the input features as a :class:`pd.DataFrame`.
        """
        if not isinstance(return_results_df, bool):
            raise exceptions.InvalidInputTypeException("return_data parameter should be a boolean (True or False.")
        if not isinstance(keep_missing_value_columns, bool):
            utils.raise_invalid_argument_exception(str(type(keep_missing_value_columns)), "keep_missing_value_columns",
                                                   "must be a `bool`. ")

        target = utils.get_name(target)

        params = {"TaskType": "SmartMapping"}
        params["Target"] = target

        # Special logic for smart mapping
        # Always return the ranking information from VIP; however, only display the head of df if the user does not
        # want to return the df to function caller. This is to ensure that pyVIP user always has access to full smart
        # mapping results.
        params["ReturnData"] = True
        params['Disp'] = not return_results_df

        if features is not None:
            params['Features'] = utils.get_features(features)
        if exclude is not None:
            params["Exclude"] = utils.get_features(exclude)

        params["KeepMissingValueColumns"] = keep_missing_value_columns

        params = [params]

        params = self._add_export_to_params(export, imsize, path, params)
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        return self._api_request(params=params, data=None)

    def ad(self, features=None, exclude=None, return_anomalies_df=True, plus_minus="both", stdev=0.5, and_or="and",
           apply=True, export="ortho", imsize=(2048, 2048), path=None, save_to_local_history=True,
           keep_missing_value_columns=True):
        """
        Alias to anomaly_detection
        """
        return self.anomaly_detection(features, exclude, return_anomalies_df, plus_minus, stdev, and_or, apply, export,
                                      imsize, path, save_to_local_history, keep_missing_value_columns)

    def anomaly_detection(self, features=None, exclude=None, return_anomalies_df=True, plus_minus="both", stdev=0.5,
                          and_or="and", apply=True, export="ortho", imsize=(2048, 2048), path=None,
                          save_to_local_history=True, keep_missing_value_columns=True):
        """
        Runs anomaly detection in VIP

        :param features: List of column names that user wants to analyze for outliers
        :param exclude: List of column names to exclude in the analysis; this overrides any features listed in the
            `features` parameter.
        :param plus_minus: Include outliers that are above, below, or above and below the desired standard deviation
            mark. Defaults to both. Can be "both", "plus", or "minus"
        :param stdev: User defined standard deviation on which to classify outliers.
        :param and_or: "and" identifies data points that are outliers in all input features. "or" identifies data
            points that are outliers in any of the input features.
        :param apply: :class:`bool` for whether to apply the result to the halo dimension.
        :param return_anomalies_df: Whether to return the output of the process to the notebook. Defaults to True.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param keep_missing_value_columns: :class:`bool` for whether to keep features with more than 50% missing
            values as part of the input for anomaly detection. Default is `True`.
        :return: :class:`None`

        """
        plus_minus = int(utils.case_insensitive_match(utils.POS_NEG_CHOICES, plus_minus, "plus_minus"))
        and_or = utils.case_insensitive_match(utils.AND_OR_CHOICES, and_or, "and_or")
        if not isinstance(return_anomalies_df, bool):
            raise exceptions.InvalidInputTypeException("return_anomalies_df parameter should be a boolean "
                                                       "(True or False).")
        try:
            stdev = utils.case_insensitive_match(utils.STDEV_CHOICES, stdev, "stdev")
        except exceptions.InvalidInputTypeException:
            raise exceptions.InvalidInputTypeException("Invalid standard deviation (we only support a "
                                                       "range of 0.5 to 5 in 0.5 intervals): " + str(stdev))
        if not isinstance(keep_missing_value_columns, bool):
            utils.raise_invalid_argument_exception(str(type(keep_missing_value_columns)), "keep_missing_value_columns",
                                                   "must be a `bool`. ")

        params = {"TaskType": "AnomalyDetection"}
        params['PositiveNegative'] = plus_minus
        params['StdDev'] = stdev
        params['AndOr'] = and_or

        if features is not None:
            params["Features"] = utils.get_features(features)
        if exclude is not None:
            params["Exclude"] = utils.get_features(exclude)

        params['ReturnData'] = return_anomalies_df

        params["KeepMissingValueColumns"] = keep_missing_value_columns

        if isinstance(apply, bool):
            if apply:
                params["Apply"] = apply
                params = [params]
                params = self._add_export_to_params(export, imsize, path, params)
                params = self._add_plot_mapping_to_params(params, save_to_local_history)
            else:
                params = [params]
        else:
            utils.raise_invalid_argument_exception(str(type(apply)), "apply", "must be a 'bool'")
        return self._api_request(params=params, data=None)

    def threshold_ad(self, features=None, exclude=None, return_anomalies_df=True, threshold=5, apply=True,
                     export="ortho", imsize=(2048, 2048), path=None, save_to_local_history=True,
                     keep_missing_value_columns=True):
        """
        Alias to pca_anomaly_detection
        """
        return self.pca_anomaly_detection(features, exclude, return_anomalies_df, threshold, apply, export, imsize,
                                          path, save_to_local_history, keep_missing_value_columns)

    def threshold_anomaly_detection(self, features=None, exclude=None, return_anomalies_df=True, threshold=5,
                                    apply=True, export="ortho", imsize=(2048, 2048), path=None,
                                    save_to_local_history=True, keep_missing_value_columns=True):
        """
        Alias to pca_anomaly_detection
        """
        return self.pca_anomaly_detection(features, exclude, return_anomalies_df, threshold, apply, export, imsize,
                                          path, save_to_local_history, keep_missing_value_columns)

    def pca_ad(self, features=None, exclude=None, return_anomalies_df=True, threshold=5, apply=True, export="ortho",
               imsize=(2048, 2048), path=None, save_to_local_history=True,
               keep_missing_value_columns=True):
        """
        Alias to pca_anomaly_detection
        """
        return self.pca_anomaly_detection(features, exclude, return_anomalies_df, threshold, apply, export, imsize,
                                          path, save_to_local_history, keep_missing_value_columns)

    def pca_anomaly_detection(self, features=None, exclude=None, return_anomalies_df=True, threshold=5, apply=True,
                              export="ortho", imsize=(2048, 2048), path=None, save_to_local_history=True,
                              keep_missing_value_columns=True):
        """
        PCA based Anomaly Detection.

        :param features:  List of column names that user wants to analyze for outliers
        :param exclude: List of column names to exclude in the analysis; this overrides any features listed in the
            `features` parameter.
        :param threshold: Percent threshold on which to classify outliers. Takes values from 0 to 100.
        :param return_anomalies_df: Whether to return the output of the process to the notebook. Defaults to True.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param apply: :class:`bool` determining whether to apply the anomaly detection result to the halo dimension.
            Default is True.
        :param keep_missing_value_columns: :class:`bool` for whether to keep features with more than 50% missing
            values as part of the input for pca based anomaly detection. Default is `True`.
        :return: :class:`None`
        """
        if not isinstance(threshold, int) and not isinstance(threshold, float):
            raise exceptions.InvalidInputTypeException("Threshold must be a number (int or float) between 0 and 100.")
        if (threshold < 0) or (threshold > 100):
            raise exceptions.InvalidInputTypeException("Threshold value, " + str(threshold) + ", is not within the "
                                                                                              "accepted range of 0 to "
                                                                                              "100.")
        if not isinstance(return_anomalies_df, bool):
            raise exceptions.InvalidInputTypeException("return_anomalies_df parameter should be a boolean "
                                                       "(True or False).")
        if not isinstance(keep_missing_value_columns, bool):
            utils.raise_invalid_argument_exception(str(type(keep_missing_value_columns)), "keep_missing_value_columns",
                                                   "must be a `bool`. ")

        params = {"TaskType": "PcaAnomalyDetection"}
        # TODO: Support floats for threshold. On VIP side, in anomaly detection task handler,
        #  an int is expected to be parsed
        params["Threshold"] = int(threshold)
        params['ReturnData'] = return_anomalies_df

        if features is not None:
            params["Features"] = utils.get_features(features)
        if exclude is not None:
            params["Exclude"] = utils.get_features(exclude)

        params["KeepMissingValueColumns"] = keep_missing_value_columns

        if isinstance(apply, bool):
            if apply:
                params["Apply"] = apply
                params = [params]
                params = self._add_export_to_params(export, imsize, path, params)
                params = self._add_plot_mapping_to_params(params, save_to_local_history)
            else:
                params = [params]
        else:
            utils.raise_invalid_argument_exception(str(type(apply)), "apply", "must be a 'bool'")
        return self._api_request(params=params, data=None)

    def pca(self, num_components, features=None, exclude=None, apply=True, return_components_df=True, export="ortho",
            imsize=(2048, 2048), path=None, save_to_local_history=True,
            keep_missing_value_columns=True):
        """
        Runs Principal Component Analysis (PCA) in VIP

        :param num_components: :class:`int` for the number of principle components to compute from the input data.
        :param features: List of column names that user wants to analyze
        :param exclude: List of column names to exclude in the analysis; this overrides any features listed in the
            `features` parameter.
        :param return_components_df: Whether to return the output of the process to the notebook. Defaults to True.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param apply: :class:`bool` determining whether to apply the first 3 computed components to the spatial
            dimensions. Default is True.
        :param keep_missing_value_columns: :class:`bool` for whether to keep features with more than 50% missing
            values as part of the input for pca. Default is `True`.
        :return: if return_data is True, this returns a :class:`pandas.DataFrame` containing the user specified number
            of principal components. Otherwise, this returns None.
        """
        # Check num_components is a positive integer and that user inputs are formatted correctly
        if not isinstance(return_components_df, bool):
            raise exceptions.InvalidInputTypeException("return_components_df parameter should be a boolean "
                                                       "(True or False).")
        if (num_components is not None) and not isinstance(num_components, int):
            raise exceptions.InvalidInputTypeException("num_components parameter should be a positive integer.")
        if (num_components is not None) and not (1 <= num_components <= 10):
            raise exceptions.InvalidInputTypeException("num_components parameter should be a positive integer "
                                                       "between 1 and 10.")
        if not isinstance(keep_missing_value_columns, bool):
            utils.raise_invalid_argument_exception(str(type(keep_missing_value_columns)), "keep_missing_value_columns",
                                                   "must be a `bool`. ")

        params = {"TaskType": "Pca"}

        params["ReturnData"] = return_components_df
        if features is not None:
            params["Features"] = utils.get_features(features)
        if exclude is not None:
            params["Exclude"] = utils.get_features(exclude)
        if num_components is not None:
            params["NumComponents"] = num_components

        params["KeepMissingValueColumns"] = keep_missing_value_columns

        if isinstance(apply, bool):
            if apply:
                params["Apply"] = apply
                params = [params]
                params = self._add_export_to_params(export, imsize, path, params)
                params = self._add_plot_mapping_to_params(params, save_to_local_history)
            else:
                params = [params]
        else:
            utils.raise_invalid_argument_exception(str(type(apply)), "apply", "must be a 'bool'")
        return self._api_request(params=params, data=None)

    def clustering(self, num_clusters=None, features=None, exclude=None, keep_missing_value_columns=True, apply=True,
                   return_clusters_df=True, export="ortho", imsize=(2048, 2048), path=None, save_to_local_history=True):
        """
        Runs K-means clustering in VIP

        :param num_clusters: :class:`int` between 1 and 16, specifying the number of clusters to compute. Default is
            `None` and enables 'auto'-mode where the number of clusters to compute is algorithmically determined based
            on stability.
        :param features: List of column names that user wants to analyze
        :param exclude: List of column names to exclude in the analysis; this overrides any features listed in the
            `features` parameter.
        :param return_clusters_df: Whether to return the output of the process to the notebook. Defaults to True.
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :param apply: :class:`bool` determining whether to apply the clustering result to the color dimension.
            Default is True.
        :param keep_missing_value_columns: :class:`bool` for whether to keep features with more than 50% missing
            values as part of the input for clustering. Default is `True`.
        :return: :class:`pandas.DataFrame` containing the results of the clustering. If return_data is false, this
            returns None.
        """
        # Check num_clusters is a positive integer and that user inputs are formatted correctly
        if not isinstance(return_clusters_df, bool):
            raise exceptions.InvalidInputTypeException("return_clusters_df parameter should be a boolean "
                                                       "(True or False).")
        if (num_clusters is not None) and (not isinstance(num_clusters, int) or num_clusters < 1 or num_clusters > 16):
            raise exceptions.InvalidInputTypeException("num_clusters parameter must be an 'int' between 1 and 16. ")
        if not isinstance(keep_missing_value_columns, bool):
            utils.raise_invalid_argument_exception(str(type(keep_missing_value_columns)), "keep_missing_value_columns",
                                                   "must be a `bool`. ")

        params = {"TaskType": "Clustering"}
        if num_clusters is not None:
            params["NumClusters"] = num_clusters
        params["ReturnData"] = return_clusters_df
        if features is not None:
            params["Features"] = utils.get_features(features)
        if exclude is not None:
            params["Exclude"] = utils.get_features(exclude)

        params["KeepMissingValueColumns"] = keep_missing_value_columns

        if isinstance(apply, bool):
            if apply:
                params["Apply"] = apply
                params = [params]
                params = self._add_export_to_params(export, imsize, path, params)
                params = self._add_plot_mapping_to_params(params, save_to_local_history)
            else:
                params = [params]
        else:
            utils.raise_invalid_argument_exception(str(type(apply)), "apply", "must be a 'bool'")
        return self._api_request(params=params, data=None)

    def normalize(self, norm_type="Softmax", export="ortho", imsize=(2048, 2048), path=None,
                  save_to_local_history=True):
        """
        Normalizes the axis for spatial dimensions in VIP if applicable.

        :param norm_type: The type of normalization to apply to the data. Can be "softmax", "log10", or "ihst"
        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param imsize: size of the returned dimension; [w, h]. Only used if `export` is not None. Defaults to
            (2048, 2048)
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param save_to_local_history: :class:`bool`; whether to save VipPlot object to `this.local_history` list.
            Default value is True.
        :return: :class:`None`
        """
        params = []
        params = self._add_normalize_task_to_params(params, norm_type)
        params = self._add_export_to_params(export, imsize, path, params)
        params = self._add_plot_mapping_to_params(params, save_to_local_history)
        return self._api_request(params=params, data=None)

    def stats(self):
        """
        Alias for statistics
        """
        return self.statistics()

    def statistics(self):
        """
        Runs statistics in VIP

        :return: :class:`None`
        """
        params = {"TaskType": "Statistics"}
        return self._api_request(params=[params], data=None)

    def insights(self):
        """
        Runs insights in VIP

        :return: :class:`None`
        """
        params = {"TaskType": "Insights"}
        return self._api_request(params=[params], data=None)

    def set_gridbox_tickmarks_view(self, gridbox=None, tickmarks=None):
        """
        Sets the visibility of the gridbox and tickmarks. Expects one or both of gridbox and tickmarks to be not None.

        :param gridbox: :class:`bool` controlling visibility of gridbox. True sets to "show", False sets to "hide"
        :param tickmarks: :class:`bool` controlling visibility of tickmarks. True sets to "show", False sets to "hide'
        :return: :class:`None`
        """
        if gridbox is None and tickmarks is None:
            raise exceptions.InvalidInputTypeException("Please specify at least one of gridbox or tickmarks arguments.")
        params = {"TaskType": "GridboxAndTickmarks"}
        gridbox = utils.case_insensitive_match(utils.VISIBILITY_OPTIONS, str(gridbox), "gridbox")
        tickmarks = utils.case_insensitive_match(utils.VISIBILITY_OPTIONS, str(tickmarks), "tickmarks")

        if gridbox is not None:
            params["Gridbox"] = gridbox
        if tickmarks is not None:
            params["Tickmarks"] = tickmarks

        return self._api_request(params=[params], data=None)

    def shape_options(self, render_mode):
        """
        Updates optimization mode of software by setting the shape options render mode.

        :param render_mode: :class:`str` to set the shape options (formely point render) mode. Can be {"Shapes",
            "Default", "2D", "Points"}
        :return: :class:`None`
        """
        render_mode = utils.case_insensitive_match(utils.POINT_RENDER_MODES, render_mode, "render_mode")
        params = {"TaskType": "Optimization", "PointRenderMode": render_mode}
        return self._api_request(params=[params], data=None)

    @utils.deprecated(version="1.2.1", new_name="VIP.shape_options()")
    def set_point_render_mode(self, render_mode):
        """
        Updates optimization mode of software by setting the shape options (point render) mode.

        :param render_mode: :class:`str` to set the shape options (point render) mode. Can be {"Shapes", "Default",
            "2D", "Points"}
        :return: :class:`None`
        """
        render_mode = utils.case_insensitive_match(utils.POINT_RENDER_MODES, render_mode, "render_mode")
        params = {"TaskType": "Optimization", "PointRenderMode": render_mode}
        return self._api_request(params=[params], data=None)

    def point_interaction(self, render_mode):
        """
        Sets the point interaction mode.

        :param render_mode: :class:`bool`. User can interact with point if and only if render_mode is True
        :return: :class:`None`
        """

        if not isinstance(render_mode, bool):
            utils.raise_invalid_argument_exception(str(type(render_mode)), "render_mode", "must be a boolean. ")

        params = {"TaskType": "Optimization", "PointInteraction": render_mode}
        return self._api_request(params=[params], data=None)

    def optimization(self, optimized):
        """
        Sets the optimization mode.

        :param optimized: If true, sets shape options to Points mode and disables point interaction. Else, sets shape
            options to Shapes mode and enables point interaction.
        :return: :class:`None`
        """
        if not isinstance(optimized, bool):
            utils.raise_invalid_argument_exception(str(type(optimized)), "optimized", "must be a boolean. ")

        params = {"TaskType": "Optimization"}

        if optimized:
            params["PointRenderMode"] = "Points"
            params["PointInteraction"] = False
        else:
            params["PointRenderMode"] = "Shapes"
            params["PointInteraction"] = True

        return self._api_request(params=[params], data=None)

    def set_camera_angle(self, angle):
        """
        Sets the camera angle in VIP (does not effect `export` camera angle).

        :param angle: :class:`str` controlling camera angle in VIP. {"Default", "Top", "Front", "Side"}
        :return: :class:`None`
        """
        angle = utils.case_insensitive_match(utils.CAMERA_ANGLE, angle, "angle")
        params = {"TaskType": "CameraAngle", "CameraAngle": angle}
        return self._api_request(params=[params], data=None)

    def get_visible_points(self):
        """
        Returns indices of points visible in VIP in a pandas DataFrame.

        :return: :class:`pandas.DataFrame` with one column containing an indicator of whether
            each point is currently visible in VIP.
        """
        params = {"TaskType": "VisiblePoints"}
        return self._api_request(params=[params], data=None)

    @staticmethod
    def _add_export_to_params(export, imsize, path, params, ignore_no_plot=False):
        """
        Helper function to attach an export task to the current request.

        :param export: Specify whether to export a capture of the plot. Can be None/False or "ortho", "front",
            "side" or "right", "top", or "perspective"
        :param imsize: Tuple or list of two integers
        :param path: Filepath to save snapshot; filepath should end with a jpg/jpeg/png/bmp extension
        :param params: The current API request
        :param ignore_no_plot: Whether the software should ignore the export task and not raise an exception if
        nothing has been mapped to the plot as yet.
        :return: params
        """
        if export in [None, False]:
            return params

        # Check to make sure user params formatted correctly
        if export:
            export = utils.case_insensitive_match(utils.EXPORT_VIEWS, export, "export")

        if path is not None and not isinstance(path, str):
            utils.raise_invalid_argument_exception(str(type(path)), "path", "Should be 'str' type encoding path to save"
                                                                            " the exported image. ")

        if not (isinstance(imsize, tuple) or isinstance(imsize, list)):
            utils.raise_invalid_argument_exception(str(type(path)), "imsize", "[w: int, h: int]")

        if not len(imsize) == 2:
            utils.raise_invalid_argument_exception(str(type(path)), "imsize", "[w: int, h: int]")

        if not isinstance(imsize[0], int) or not isinstance(imsize[1], int):
            utils.raise_invalid_argument_exception(str(type(path)), "imsize", "[w: int, h: int]")

        # attach the new export task
        if (export is not None) or (export is not False):
            export_params = {"TaskType": "Export"}
            export_params["View"] = export
            export_params["Width"] = imsize[0]
            export_params["Height"] = imsize[1]
            export_params["IgnoreNoPlot"] = ignore_no_plot
            if path is not None:
                export_params["Path"] = path
            params.append(export_params)
        return params

    @staticmethod
    def _add_plot_mapping_to_params(params, save_to_local_history):
        """
        Constructs the task to get the current plot mapping info

        :param params: The current API request
        :return: params
        """
        if not save_to_local_history:
            return params
        plot_mapping_task = {"TaskType": "PlotMappingExport"}
        plot_mapping_task["ReturnPlotMapping"] = save_to_local_history
        params.append(plot_mapping_task)
        return params

    @staticmethod
    def _add_heatmap_feature_to_params(params, heatmap_feature, return_data):
        if not isinstance(heatmap_feature, bool):
            utils.raise_invalid_argument_exception(str(type(heatmap_feature)), "heatmap_feature",
                                                   "must be a `bool`.")
        if not isinstance(return_data, bool):
            utils.raise_invalid_argument_exception(str(type(return_data)), "return_data",
                                                   "must be a `bool`")

        if heatmap_feature:
            heatmap_task = {"TaskType": "HeatmapFeature"}
            heatmap_task["ReturnData"] = return_data
            params.append(heatmap_task)
        return params

    @staticmethod
    def _add_normalize_task_to_params(params, norm_type):
        """
        Constructs the task to apply normalize to the spatial dimensions (with option to apply to size).

        :param params: the current API request's task params list
        :param norm_type: the normalization option to use.
        :return: params
        """
        norm_param = {"TaskType": "Normalize"}
        norm_param["NormType"] = utils.case_insensitive_match(utils.NORMALIZATION_OPTIONS, norm_type, "norm_type")
        params.append(norm_param)
        return params

    def _update_invalid_export_view(self, plot, requested_view):
        """
        This checks if the requested view is invalid and substitutes it if necessary.

        :param plot: :class:`VipPlot` instance.
        :param requested_view: :class:`str` specifying the requested view.
        :return: :class:`None`
        """
        if requested_view in [None, False]:
            return requested_view
        if not isinstance(requested_view, str):
            utils.raise_invalid_argument_exception(type(requested_view), "export", "Should be None/False or 'ortho', "
                                                                                   "'front', 'side' or 'right', 'top', "
                                                                                   "or 'perspective'")
        if requested_view.lower() in ["none", "false"]:
            return None

        best_view = plot.get_best_export_view()
        if best_view is not None:
            if self.log_level >= LOG_HELP_LEVEL:
                print("The 'export' view is being reset to '{}' view since this is the only valid view for "
                      "this plot. ".format(best_view))
            requested_view = best_view

        return requested_view
