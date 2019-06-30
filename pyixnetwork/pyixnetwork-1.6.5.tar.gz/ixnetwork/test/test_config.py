
chassis_01 = '192.168.42.61'
chassis_40 = '192.168.42.207'
chassis_50 = '192.168.65.53'

localhost = 'localhost:11009'

linux_40 = '192.168.65.49:443'
linux_50 = '192.168.65.73:443'
linux_52 = '192.168.65.47:443'

windows_40 = '192.168.65.46:11009'
windows_50_http = 'localhost:11009'
windows_50_https = '192.168.65.94:11009'
windows_52_https = '192.168.65.81:11009'

linux_servers = [linux_40, linux_50, linux_52]
windows_servers = [windows_40, windows_50_http, windows_50_https, windows_52_https]

server_properties = {linux_40: {'chassis': chassis_40, 'auth': ('admin', 'admin'), 'config_version': 'ngpf'},
                     linux_50: {'chassis': chassis_50, 'auth': ('admin', 'admin'), 'config_version': 'ngpf'},
                     linux_52: {'chassis': None, 'auth': ('admin', 'admin'), 'config_version': 'ngpf'},
                     windows_40: {'chassis': chassis_40, 'auth': None, 'config_version': 'classic'},
                     windows_50_http: {'chassis': chassis_50, 'auth': None, 'config_version': 'classic'},
                     windows_50_https: {'chassis': chassis_50, 'auth': None, 'config_version': 'classic'},
                     windows_52_https: {'chassis': None, 'auth': None, 'config_version': 'classic'}}
