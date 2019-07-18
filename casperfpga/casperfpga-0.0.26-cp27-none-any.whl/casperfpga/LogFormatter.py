import logging
import datetime
import skarab_definitions as sd


class LogFormatter(logging.Formatter):
    """
    Custom log-message formatter to go with custom log-handler
    """

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        super(LogFormatter, self).__init__()
        # Need the hostname to put into the log-messages
        if len(args) > 0:
            try:
                kwargs['host'] = args[0]
                kwargs['logger_name'] = args[1]
                kwargs['log_level'] = args[2]
            except IndexError:
                pass
        self._host = kwargs['host']
        self._logger_name = kwargs['logger_name']
        self._log_level = sd.logger_level_dict[kwargs['log_level']]

    def format(self, record):
        """

        :param record:
        :return: Formatted message a string
        """
        current_datetime = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")
        record = '{} | {} - {} -- {}'.format(self._log_level, current_datetime, self._host, record.msg)

        import IPython
        IPython.embed()

        return record
