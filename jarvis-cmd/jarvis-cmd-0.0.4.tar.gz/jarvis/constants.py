from os import path 

user_home = path.expanduser('~')
jarvis_config_home = user_home + '/.jarvis'
openproject_config_file = jarvis_config_home + '/creds.cfg'