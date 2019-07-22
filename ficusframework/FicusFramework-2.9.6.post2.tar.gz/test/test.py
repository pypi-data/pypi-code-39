import traceback

if __name__ == '__main__':
    try:
        i = int('a')
    except Exception as e:
        # print('str(Exception):\t', str(Exception))
        # print('str(e):\t\t', str(e))
        # print('repr(e):\t', repr(e))
        # print('traceback.print_exc():')
        # traceback.print_exc()
        print('traceback.format_exc():\n%s' % traceback.format_exc())