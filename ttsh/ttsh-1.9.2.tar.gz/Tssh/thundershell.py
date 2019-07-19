#!/usr/bin/env python
#By Electronic Nodder 22Bit(ENodder)
#Open Source/Copy Right Allowed :)
#Lincense 1.9L
#Termux version
import os,sys,time,socket,logging,traceback,signal
from platform import python_version
from os import walk
if __name__ == '__main__':

    if int(python_version()[0]) < 3:
        print("\033[0;33m<!>Tsh just can start with Python3. do python3 thundershell.py<!>")
        exit()
print("\033[92m(Thunder S|-|ell) <A PRODUCT BY \033[91m22bit")
time.sleep(2)
print("\033[93mTsh(Thunder Shell) License 1.9L\nVersion: 1.9 Termux Edition\n")
time.sleep(3)
def passwd():
	try:
		passwd.passwords=input("\033[94m<>TSH new password:\033[0m ")
		time.sleep(1)
		print("\033[93m<!>DON'T FORGOT YOUR PASSWORD<!>\033[0m")
		time.sleep(1.5)
		os.system("clear")
	except (KeyboardInterrupt,SystemExit):
		print("\033[91merror703")
		passwd()
def sh():
	try:
		a=input("\n\033[1;32m<\<\033[3;33mThunder\033[1;32m>/>\033[0m ")
		time.sleep(0.01)
		if a=="download":
			print("\033[94mD0WNL0D FIRE/\\Do : download PACKAGENAME")
			sh()
		elif "download " in a:
			print("\033[94mD0wnl0ading...")
			if "download instagram" in a:
				print("\033[91min ThunderShell 1.9 Instagram-Master,Hammer,HiddenEye,Cupp and iCrack already installed")
				sh()
			elif "download hammer" in a:
				print("\033[91min ThunderShell 1.9 Instagram-Master,Hammer,HiddenEye,Cupp and iCrack already installed")
				sh()
			elif "download hiddeneye" in a:
				print("\033[91min ThunderShell 1.9 Instagram-Master,Hammer,HiddenEye,Cupp and iCrack already installed")
				sh()
			elif "download cupp" in a:
				print("\033[91min ThunderShell 1.9 Instagram-Master,Hammer,HiddenEye,Cupp and iCrack already installed")
				sh()
			elif "download icrack" in a:
				print("\033[91min ThunderShell 1.9 Instagram-Master,Hammer,HiddenEye,Cupp and iCrack already installed")
				sh()
			elif "download gui" in a:
				print("\033[91mGUI Edition is only for linux versions")
				sh()
			else:
				print("\033[91mRepository Not Found :(")
				sh()
		elif a=="get":
			print("\033[1;34mTermux package manager PKG.do: get PACKAGENAME")
			sh()
		elif "get " in a:
			print("\033[93mChecking ...")
			os.system("pkg install "+a.replace("get ",""))
			sh()
		elif a=="f":
			print("\033[93mDMT:Directory Manager For TSH.\nf remove NAME\tfor remove a file\nf add NAME\tfor add a file\nf -dir remove NAME\tfor remove a folder\nf -dir add NAME\t\tfor add a folder\n")
			sh()
		elif "f " in a:
			if "f remove " in a:
				try:
					if os.path.exists(a.replace("f remove ","")):
						print("\033[91mRemoving...")
						os.remove(a.replace("f remove ", ""))
						sh()
					else:
						print(a.replace("f remove ","")+"\033[91m is not a file")
						sh()
				except Exception:
					print("\033[91mSomthing went wrong")
					sh()
			elif a=="f remove":
				print("\033[94mf remove [FILE NAME]")
				sh()
			elif "f add " in a:
				try:
					print("\033[95mCreating...")
					js=open(a.replace("f add ",""),"x")
					js.close()
					sh()
				except Exception:
					print("\033[91mSomthings not true")
					sh()	
			elif a=="f add":
				print("\033[92mf add [NAME]")
				sh()
			elif a=="f -dir":
				print("\033[92mf -dir [OPTION]")
				sh()
			elif a=="f -dir remove":
					print("\033[92mf -dir remove [FOLDER NAME]")
					sh()
			elif "f -dir remove " in a:
				try:
					if os.path.exists(a.replace("f -dir remove ","")):
						print("\033[94mRemoving Folder")
						os.rmdir(a.replace("f -dir remove ",""))
						sh()
					else:
						print(a.replace("f -dir remove ","")+"\033[91m is not a directory")
						sh()
				except Exception:
					print("\033[91mSomthing went wrong")
					sh()
			elif "f -dir add " in a:
				try:
					print("\033[92mCreating Directory")
					os.makedirs(a.replace("f -dir add ",""))
					sh()
				except:
					print("\033[91mSomthings not true")
					sh()
			elif a=="f -dir add":
				print("\033[91mf -dir add [NAME]")
				sh()
			else:
				print("\033[91mInvaild Option")
				sh()
		elif "methods" in a:
			print("\033[0;34mTsh Methods:\nHacking==\nuse icrack\tuse instagram\tuse fakepage\nuse git\tuse bash\tuse passlist\nuse hammer\tuse nuclear-power\tuse pip\n\nThunder Shell Mehods")
			sh()
		elif a=="use":
			print("\033[0;35Use methods. for see methods do :\n\tmethods")
			sh()
		elif "use " in a:
			try:
				if "use icrack" in a:
					print("\033[0;32mEntering ICRACK...")
					time.sleep(3)
					os.system("python2 icrack.py")
					sh()
				elif "use instagram" in a:
					print("\033[0;32mEntering instagram...")
					time.sleep(3)
					rawsx=input("\033[93mTarget Username(ID):\033[0m ")
					rawpl=input("\033[92mPassword List(Full path):\033[0m ")
					os.system("python3 instagram.py "+rawsx+" "+rawpl)
					sh()
				elif "use hammer" in a:
					print("\033[0;32mEntering hammer...")
					host=input("\033[0;33;44mYour Target Site ip(if you haven't site ip in tsh do host www.SITE.COM):\033[0;m ")
					os.system("python hammer.py -s "+host+" -p 80")
					sh()
				elif "use git" in a:
					print("\033[0;32mEntering git...")
					os.system("git")
					print("\033[92mDo exit for back in Tsh")
					while True:
						hue=input("\033[3;34;43m<G><I><T>>>\033[0m ")
						os.system("git "+hue)
						if "exit" in hue:
							print("\033[91mExited From Git")
							sh()
						sh()
				elif "use hiddeneye" in a:
					print("\033[0;32mEntering hiddeneye...")
					os.system("python HiddenEye.py")
					sh()
				elif "use bash" in a:
					print("\033[0;32mEntering Bash-Tsh...")
					print("\033[92mDo exixt for backin Tsh")
					while True:
						bashrd=input("\033[1;31;42m_B-A_S-H_$>\033[0m ")
						os.system(bashrd)
						if "exixt" in bashrd:
							sh()
					sh()
				else:
					print("\033[91mNo Method Found: "+a.replace("use ",""))
					sh()
			except Exception:
				print("\033[91mError 385xn2")
				sh()
		elif a=="host":
			print("\033[93mNetwork Tools:\nDo:\nhost www.SITE.COM\nI.e host www.google.com")
			sh()
		elif "host " in a:
			try:
					print("\033[1;32mhost of "+a.replace("host ","")+" is "+socket.gethostbyname(a.replace("host ","")))
					sh()
			except Exception:
				print("\033[91mUnable to access site")
				sh()
		elif a=="":
			sh()
		elif "test" in a:
			sh()
		elif a=="hello":
			print("\033[32mHe||0")
			sh()
		elif a=="ls":
			os.system("ls")
			sh()
		elif "ls " in a:
			os.system("ls "+a.replace("ls ",""))
			sh()
		elif a=="spamx":
			print("\033[0;33mConsole Spammer. do spamx COMMAND_FOR_SPAM")
			sh()
		elif "spamx " in a:
			while True:
				print("\033[1;34;41m"+a.replace("spamx ",""))
			sh()
		elif a=="cd":
			print("\033[1;34mWhere we should move? do:\ncd DIRECTORY\ni.e cd Tssh")
			sh()
		elif "cd " in a:
			try:
				if os.path.exists(a.replace("cd ","")):
					os.chdir(a.replace("cd ",""))
					sh()
				else:
					print("\033[91mDirectory Not Found: "+a.replace("cd ",""))
					sh()
			except Exception:
				print("\033[91mError 703")
				sh()
		elif "linux" in a:
			print("\033[0;34mThis is Termux version")
			sh()
		elif "backend" in a:
			print("\033[0;31Python3/Back-End. Back-End and Front-End by ENodder 22bit")
			sh()
		elif a=="say":
			print("\033[93mDo : say MESSAGE")
			sh()
		elif "say " in a:
			print("\033[93m<MESSAGE>: \033[0m"+a.replace("say ",""))
			sh()
		elif "print" in a:
			print("\033[92m"+a.replace("print ",""))
			sh()
		elif "\\" in a:
			while True:
				attempt=input("_> ")
				if attempt=="exit":
					sh()
			sh()
		elif "clear" in a:
			os.system("clear")
			sh()
		elif "exit" in a:
			print("\033[91mTSH Now is your default shell")
			sh()
		elif a=="new":
			print("\n")
			sh()
		elif a=="ide":
			print("\033[3;34mNano TE. do ide FILE.FORMAT for build or read files")
			sh()
		elif "ide " in a:
			os.system("nano "+a.replace("ide ",""))
			sh()
		elif a=="copy":
			try:
				askc=input("\033[1;34mFile To Copy: ")
				askp=input("\033[1;33mPath To Paste: ")
				if os.path.exists(askc):
					if os.path.exists(askp):
						os.system("cp "+askc+" "+askp)
						sh()
				elif os.path.exists(askc):
					if not os.path.exists(askp):
						print("\033[91mPath Not Found :(")
						sh()
				elif not os.path.exists(askc):
					if os.path.exists(askp):
						print("\033[91mFile Not Found :(")
						sh()
				else:
					print("\033[91mFile and Path Not Found :(")
					sh()
				sh()
			except Exception:
				print("\033[91mSomthing not true, try again")
				sh()
		elif a=="inf":
			print("\033[93mTSH 1.9 \nThunder Shell 1.9\n22Bit\n4 Power\nInstagram-master: PURE L0G1C\nIcrack: 04x\nHammer: cyweb\nHiddenEye: DarkSecDeveloper\nand ...\nAll and Tsh : 22bit")
			sh()
		elif a=="a":
			print("\033[92mWTF?")
			sh()
		elif a=="love":
			print("\033[92m:| Sex?")
			sh()
		elif "fuck you" in a:
			print("\033[92mHEY USER BITCH, DO YOU KNOW WHAT THE FUCKING YOU SAY? ASSHOLE")
			sh()
		elif "bitch" in a:
			print("\033[91mYeh, you\'re true. your mom is bitch ")
			sh()
		elif "leave me" in a:
			print("\033[1;33mJUST DO EXIT OR CTRL+C :|")
			sh()
		elif a=="add":
			print("\033[93mNext Update ADD will added on Tsh")
			sh()
		elif "profile" in a:
			print("\033[93mProfile will added in Tsh 2.2")
			sh()
		elif "sh" in a:
			print("\033[92mThunderShell")
			sh()
		elif "help" in a:
			print("\033[93mSorry but i can\'t help you :( you should learn from yourself or wait for update 2.5")
			sh()
		elif "rename" in a:
			try:
				juname=input("\033[1;31mFile Name to rename: ")
				runame=input("\033[1;32mNew Name: ")
				if os.path.exists(juname):
					os.rename(juname,runame)
					print("\033[93mRenamed")
					sh()
				else:
					print("\033[91mFile Error")
					sh()
				sh()
			except Exception:
				print("\033[91mError 512")
				sh()
		elif "vpn" in a:
			print("\033[94mVPN comes on 2.19")
			sh()
		elif a=="grabber":
			print("\033[92mdo:\ngrab instagram\tfor see some instagram users\ngrab spotify\tsee some spotify premium users\ngrab nordvpn\tfor see some nord vpn accounts\ngrab vps\tfor grab some vps hosts")
			sh()
		elif a=="grab":
			print("\033[92mDo grabber")
			sh()
		elif "grab " in a:
			print("\033[91mSOON")
			sh()
		elif a=="top":
			print("\033[92mSites:\nwww.youtube.com\nwww.wikipedia.com\nwww.stackoverflow.com\nwww.github.com\nwww.pornhub.com\nwww.tutorialspoint.com\n\nOSes:\nElementary os\nManjaro Linux\nLinux Mint\nUbuntu linux\nDebian\nKali\nMacOS\nWindows")
			sh()
		elif a=="targets":
			print("\033[94mTarget list:\nInstagram: @french_friar & @french_friarcosplays & @enodder & @hacker & @BroadCaster")
			sh()
		elif a=="pyx":
			print("\033[93mPYTHON 3")
			sh()
		elif "reqi" in a:
			try:
				print("\033[92mInstall all requirements")
				os.system("pip install requests")
				os.system("pip install bs4")
				os.system("pip install beautifulsoup")
				print("\033[92Other moduls you should install manually")
				sh()
			except Exception:
				print("\033[91mSomthing wrong")
				sh()
		elif a=="python":
			print("\033[92mPython + file. please write python FILE.py")
			sh()
		elif "python " in a:
			try:
				if os.path.exists(a.replace("python ","")):
					print("\033[93mStarting "+a.replace("python ",""))
					os.system("python "+a.replace("python ",""))
					sh()
				else:
					print("\033[91mFile "+a.replace("python ","")+"not found")
					sh()
				sh()	
			except Exception:
				print("\033[91mSomthing not true")
				sh()
		elif a=="read":
			print("\033[92mdo read + FILE.txt, i.e read helloworld.txt")
			sh()
		elif "read " in a:
			print("\033[93mReading File...")
			try:
				if os.path.exists(a.replace("read ","")):
					ftpss=open(a.replace("read ",""), "r")
					sh()
				else:
					print("\033[91mFile Not Found")
					sh()
				sh()
			except Exception:
				print("\033[91mSomthing's wrong")
				sh()
		elif a=="run":
			print("\033[93mShellscript file runner. do run file.sh . i.e run hellotsh.sh.")
			sh()
		elif "run " in a:
			try:
				print("\033[92mRunning linux shellscript file...")
				if os.path.exists(a.replace("run ","")):
					os.system("./"+a.replace("run ",""))
					sh()
				else:
					print("\033[91mFile Not Found or not a shellscript file")
					sh()
				sh()
			except Exception:
				print("\033[91mSomthing went wrong")
				sh()
		elif a=="myip":
			try:
				print("\033[92mLoading...")
				os.system("ifconfig")
				sh()
			except Exception:
				print("\033[91mSomthing went wrong")
				sh()
		elif "termux" in a:
			print("\033[92mEntering Termux mode")
			print("\033[93mType ezxt for exit termux mode and back to tsh mode")
			try:
				while True:
					termzx=input("\033[3;32m<T/ermux>>\033[0m ")
					os.system(termzx)
					if "ezxt" in termzx:
						print("\033[91mExited from termux shell mode")
						sh()
				sh()
			except Exception:
				print("\033[91mSomthing's not true")
				sh()
		elif "22bit" in a:
			print("\033[91mYES?")
			sh()
		elif a=="pip":
			os.system("pip")
			sh()
		elif "pip " in a:
			try:
				os.system("pip "+a.replace("pip ",""))
				sh()
			except Exception:
				print("\033[91mSomthing went wrong")
				sh()
			sh()
		elif "exploit" in a:
			print("\033[93mExploits and hack android next updates")
			sh()
		elif a=="git":
			try:
				os.system("git")
				sh()
			except Exception:
				print("\033[91mSomthing went wrong")
				sh()
			sh()
		elif "git " in a:
			try:
				os.system("git "+a.replace("git ",""))
				sh()
			except Exception:
				print("\033[91mSomthing went wrong")
				sh()
			sh()
		elif a=="pkg":
			try:
				os.system("pkg")
				sh()
			except Exception:
				print("\033[91mSomthing went wrong")
				sh()
			sh()
		elif "pkg " in a:
			try:
				os.system("pkg "+a.replace("pkg ",""))
				sh()
			except Exception:
				print("\033[91mSomthing went wrong")
				sh()
			sh()
		elif a=="nano":
			try:
				os.system("nano")
				sh()
			except Exception:
				print("\033[91mSomthing went wrong")
				sh()
			sh()
		elif "nano " in a:
			os.system("nano "+a.replace("nano ",""))
			sh()
		elif a=="apt":
			try:
				os.system("apt")
				sh()
			except Exception:
				print("\033[91mSomthing is not true")
				sh()
			sh()
		elif "apt " in a:
			try:
				os.system("apt "+a.replace("apt ",""))
				sh()
			except Exception:
				print("\033[91mSomthing went wrong")
				sh()
			sh()
		elif a=="echo":
			try:
				os.system("echo")
				sh()
			except Exception:
				print("\033[91mSomthing went wrong")
				sh()
			sh()
		elif "echo " in a:
			try:
				os.system("echo "+a.replace("echo ",""))
				sh()
			except Exception:
				print("\033[91mSomthing went wrong")
				sh()
			sh()
		elif a=="ps":
			try:
				os.system("ps")
				sh()
			except Exception:
				print("\033[91mSomthing went wrong")
				sh()
			sh()
		elif "ps " in a:
			try:
				os.system("ps "+a.replace("ps ",""))
				sh()
			except Exception:
				print("\033[91mSomthing went wrong")
				sh()
			sh()
		elif "version" in a:
			print("\033[1;34;42mThunderShell/TSH shell\nVersion 1.9\nLicense 1.9L\nDeveloped by 22Bit\nhttps://github.com/22bit/tshx.git\n22bit an iranian programmer.\nTermuxEdition")
			sh()
		else:
			print("\033[91mInvaild Command: "+a)
			sh()
	except (KeyboardInterrupt,Exception,SystemExit):
		print("\033[91mUnable To Do This")
		sh()
try:
	passwd()
	sh()
except:
	pass