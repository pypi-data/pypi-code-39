import time


class MessageBuilder:
    DEVIDER = {"type": "divider"}

    def __init__(self, expr_name):
        self.expr_name = expr_name

    def create_message(self, message=None):
        raise NotImplementedError

    def _create_section(self, text, text_type='mrkdwn'):
        return {
            'type': 'section',
            'text': {
                'type': text_type,
                'text': text,
            }
        }

    def _create_mrkdwn_fields(self, *attributes):
        fields = [{
            'type': 'mrkdwn',
            'text': '*{}:*\n{}'.format(k, v),
        } for k, v in attributes]

        return {
            'type': 'section',
            'fields': fields,
        }

    def _quote(self, content):
        return self._create_section('\n'.join(
            ['>' + line for line in content.split('\n')]))


class CompleteMessageBuilder(MessageBuilder):
    def __init__(self, expr_name):
        super().__init__(expr_name)
        self.start_at = None
        self.end_at = None

    def set_start_time(self, timestamp):
        self.start_at = timestamp

    def set_end_time(self, timestamp):
        self.end_at = timestamp

    def __create_header(self):
        return self._create_section('* Experiment Completed:* _{}_'.format(
            self.expr_name))

    def __create_time_info(self):
        time_format = '<!date^{}^{{date_num}} {{time_secs}}|{}>'
        start = time_format.format(
            int(self.start_at),
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.start_at)))
        end = time_format.format(
            int(self.end_at),
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.end_at)))

        eplapsed_time = int(self.end_at - self.start_at)
        seconds = eplapsed_time % 60
        minutes = (eplapsed_time // 60) % 60
        hours = (eplapsed_time // 3600) % 24
        days = eplapsed_time // (24 * 3600)
        duration = '{:02d}:{:02d}:{:02d}:{:02d}'.format(
            days, hours, minutes, seconds)

        return self._create_mrkdwn_fields(('Start', start), ('End', end),
                                          ('Duration', duration))

    def create_message(self, message=None):
        blocks = [
            self.__create_header(),
            self.DEVIDER,
            self.__create_time_info(),
        ]

        if message is not None:
            blocks += [
                self.DEVIDER,
                self._quote(message),
            ]

        return blocks
