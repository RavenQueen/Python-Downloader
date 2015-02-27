import platform
import getpass
import urllib2
import hashlib
import os
import time

curOS = platform.system()
installDir = ""


def detectOS():
    if curOS == "Windows":
		global installDir
		installDir = "C:\\Python27"
    elif curOS == "Linux":
		print "Linux Support coming soon!"
    else:
        print "Error: Unknown operating system detected."
	return curOS


def downloadPython():
	if fileCheck() == True:
		hashCheck()
	else:
		url = "https://www.python.org/ftp/python/2.7.9/python-2.7.9.msi"
		filename = url.split('/')[-1]
		u = urllib2.urlopen(url)
		f = open(filename, 'wb')
		meta = u.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		print "Downloading: %s Bytes: %s" % (filename, file_size)
		file_size_dl = 0
		block_sz = 8192
		while True:
			buffer = u.read(block_sz)
			if not buffer:
				break
			
			file_size_dl += len(buffer)
			f.write(buffer)
			status = r"%10d [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
			status = status + chr(8)*(len(status)+1)
			print status,
		f.close()
		hashCheck()


def fileCheck():
	if os.path.isfile("python-2.7.9.msi"):
		return True
	else:
		return False


def install():
	installCmd = "msiexec /i python-2.7.9.msi TARGETDIR=" + installDir
	os.system(installCmd)


def uninstall():
	if os.path.isfile("C:\\Python27\python.exe"):
		if fileCheck() == False:
			ans = raw_input("Error: The original installer is needed to continue the uninstallation.\nDownload now? Y\N: ")
			if ans in ("y", "Y"):
				downloadPython()
				uninstallCmd = "msiexec /x python-2.7.9.msi"
				os.system(uninstallCmd)
			else:
				exit()
		else:
			uninstallCmd = "msiexec /x python-2.7.9.msi"
			os.system(uninstallCmd)
	else:
		print "Python does not seem to be installed."

def hashCheck():
	"""Make Sure we have the correct hash and the download has
	not been tampered with or corrupted."""
	filename = 'python-2.7.9.msi'
	original_md5 = '3ed20d8b06dcd339f814b38861f88fc9'

	with open(filename, "rb") as f:
		data = f.read()
		md5_returned = hashlib.md5(data).hexdigest()

	if original_md5 == md5_returned:
		print "MD5 verified. Starting installer."
	else:
		print "MD5 verification failed!."
	#install() No longer calls this function here.


def changeInstallDir():
	ans = raw_input("Where would you like to install Python?: ")
	if ans != "":
		global installDir
		installDir = ans
	print "The installation directory is currently set to: " + installDir
	time.sleep(2) # Pause 2 seconds so the user can read the directory.

def menu():
	var = 1
	while var == 1:
		print "Python Downloader Version 1.0a\n\n"
		if curOS == "Linux":
			os.system('clear')
		elif curOS == "Windows":
			os.system('cls')

		print("""
		1. Install Python
		2. Uninstall Python
		3. Change installation directory
		4. Quit
		""")
		ans = raw_input("Enter a selection: ")
		if ans == "1":
			print "Downloading python 2.7 installer...\n"
			downloadPython() # This downloads the file and calls hashCheck()
			install()	# Install Python.
		elif ans == "2":
			uninstall()
		elif ans == "3":
			changeInstallDir()
		elif ans == "4":
			exit()


detectOS()
menu()
