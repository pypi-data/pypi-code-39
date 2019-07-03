import platform
bit = platform.architecture()[0]

if(bit == '32bit'):
    from haohaninfo.GOrder.GOCommand import GOCommand
    from haohaninfo.GOrder.GOQuote import GOQuote
else:
    from haohaninfo.GOrder.GOCommand64 import GOCommand
    from haohaninfo.GOrder.GOQuote64 import GOQuote