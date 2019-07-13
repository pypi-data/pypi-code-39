import os


class DataAuditing(object):
    """
    Track data processed in the system for later auditing
    Creates an audit log in CSV format, and uploads as experiment/task output artifact
    Automatically connects to Task.current_task unless otherwise stated

    Columns titles can be set at any time during data audit usage.
    Data audit table written when flushing object
    """

    def __init__(self, name, *columns):
        """
        Creates 2D table with columns names as stated in args.
        Order of columns according to argument order
        Example:
            DataAuditing(name='train', 'filename', 'class_name',
                        'bounding_box_top', 'bounding_box_left',
                        'bounding_box_bottom', 'bounding_box_right')
        :param name: Data audit name (string)
        :type name: str
        :param columns: column names
        :type columns: str
        """
        self._name = name
        self._max_columns = 0
        self._columns = []
        self._na = ''
        self._task = None
        self.set_columns(*columns)

    def set_columns(self, *columns):
        """
        Order of columns according to argument order
        example: set_columns('filename', 'class_name',)
        :param columns: column names
        :type columns: str
        """
        self._columns = columns or []
        self._max_columns = max(self._max_columns, len(self._columns))

    def add_row(self, *values):
        """
        Connects the data auditing object with specific type, default is main task
        :param values: list of values, one per column
        :type values: basic type (float, int, str)
        """
        pass

    def flush(self):
        """
        Flush data audit table and upload to server
        Can be called multiple times
        :return: True if flush was successful
        """
        pass

    def __str__(self):
        """
        Return string representation of the data audit table
        columns + first rows + last rows
        :return: string
        """
        pass

    def get_pd(self):
        """
        Get the underlying pandas object. Use with care.
        :return: pandas.DataFrame
        """

    def set_task(self, task):
        """
        Connects the data auditing object with specific type, default is main task
        :param task: Task object
        :type task: Task
        """
        self._task = task

    def set_not_available_value(self, value):
        """
        Set not-available value, used when number of columns is larger then number of given values in a row.
        Default: empty string ''
        :param value: str
        """
        self._na = value

    def get_not_available_value(self):
        """
        Return default not-available value,
        used when number of columns is larger then number of given values in a row.
        :return: str
        """
        return self._na

    def get_num_rows(self):
        """
        return number of rows in current data audit
        :return: integer
        """
        pass

    def get_columns(self):
        """
        return column names list
        :return: list of strings
        """
        return self._columns

    def get_num_columns(self):
        """
        Return number of columns in data auditing table
        :return: integer
        """
        return self._max_columns
