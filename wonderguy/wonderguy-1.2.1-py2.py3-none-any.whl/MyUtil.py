
class MyUtil(object):
    '''
    wonderbits util set
    '''
    # decide if show console
    is_show_console = False

    @staticmethod
    def wb_log(*params):
        '''
        接受不定个数的参数, 并print出来
        '''
        if not MyUtil.is_show_console:
            return
        print('###wb-log: ', end="")
        for param in params:
            print(param, end=" ")
        print()

    @staticmethod
    def wb_decode(raw_byte = b''):
        return raw_byte.decode('gbk')

    @staticmethod
    def wb_encode(raw_str = ''):
        return raw_str.encode('gbk')

    @staticmethod
    def parse_data_from_raw_repl(buffer):
        OK = 'OK'
        beginIndex = buffer.find(OK) + len(OK)
        endIndex = buffer.rfind('\r\n')
        # set_command finished successfully
        if endIndex == -1:
            return 'done'
        # set_command failed
        # get_command finished successfully
        # get_command failed
        return buffer[beginIndex: endIndex]