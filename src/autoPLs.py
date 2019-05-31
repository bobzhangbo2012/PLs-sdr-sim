#!/usr/bin/env python3

import subprocess
import os
from ftplib import FTP
from time import sleep
import datetime

def welcome():
	os.system("clear")
	print("""------------------PLs-sdr-sim-------------------\r\n""")

def downloadBrdc():
	brdcSite = FTP("cddis.gsfc.nasa.gov")
	print("\n\t\033[92m[*] Connected to GSFC NASA FTP!\033[0m")
	brdcSite.login()
	now = datetime.datetime.now()
	brdcSite.cwd("gnss/data/daily/"+str(now.year)+"/brdc/")
	ftpContent = []
	brdcSite.dir(ftpContent.append)
	brdcFiles = []
	print("\t\033[92m[*] Looking for brdc file...\033[0m")
	for entry in ftpContent:
		if entry.endswith("n.Z"):
			brdcFiles.append(entry)
	toDownload = brdcFiles[-1]
	brdcFile = str(toDownload[-14:-1]) + str(toDownload[-1])
	file = open("brdc_files/%s" % brdcFile, "wb")
	brdcSite.retrbinary("RETR %s" % brdcFile, file.write)
	print("\t\033[92m[*] Downloaded file: %s\033[0m" % brdcFile)
	print("\t\033[92m[*] Uncompressing...\033[0m")
	os.system("uncompress -f brdc_files/%s" % brdcFile)
	brdcFile = brdcFile[0:12]
	print("\t\033[92m[*] File uncompressed: %s\n\033[0m" % brdcFile)
	return brdcFile


def gpssimbin(brdcFile, lat, lon, hgt, runt):
	#runt=int(runt)*60
	os.system("./gps-sdr-sim -b 8 -e brdc_files/%s -l %s,%s,%s -d %s" % (brdcFile, lat, lon, hgt, runt))
	print("\n\t\033[92m[*] Data processed, gpssim.bin created.\033[0m")


def hackrf():
	args = ["hackrf_transfer", "-t", "gpssim.bin", "-f", "1575420000", "-s", "2600000", "-x", "0", "-a", "1"]
	print("\t\033[92m[*] Executing hackrf_transfer...\033[0m")
	os.execvp(args[0], args)

# if __name__ == '__main__':
#     (options) = get_options()
#     tb = top_block(options)
#     tb.start()
#     raw_input('Press Enter to quit: ')
#     tb.stop()
#     tb.wait()


def main():
# if __name__ == '__main__':
	welcome()
	# rootContent = os.listdir()
	# if "gps-sdr-sim" not in rootContent:
	# 	print("\t\033[91m[-] gps-sdr-sim not found in current directory.\033[00m")
	# 	gitTrigger = input("\t[?] Clone git and set up the environment? ([y]/n) > " or "y")
	# 	print("\n")
	# 	if gitTrigger == "y" or gitTrigger == "Y":
	# 		os.system("git clone https://github.com/osqzss/gps-sdr-sim.git")
	# 		sleep(2)
	# 		os.system("mv gps-sdr-sim/* . && rm -rf gps-sdr-sim/")
	# 		sleep(2)
	# 		os.system("gcc gpssim.c -lm -O3 -o gps-sdr-sim && mkdir brdc_files")
	# 	else:
	# 		print("\t\033[91m[-] Exiting...\033[00m\n")
	# 		exit(0)
	procTrigger = input("\n\t[?] Hi, do you want to first recompile gpssim.bin? (y/[n]) > ") or "n"
	if procTrigger == "y" or procTrigger == "Y":
		dlTrigger = input("\t[?] Do you want to download the most recent brdc file? ([y]/n) > ") or "y"
		if dlTrigger == "y" or dlTrigger == "Y":
			brdcFile = downloadBrdc()
		else:
			brdcArray = os.listdir("brdc_files/")
			print("\t[?] What file do you want to use?\n")
			i=0
			for file in brdcArray:
				print("\t ["+str(i)+"]- " + file)
				i=i+1
			try:
				brdcFile = input("\n\t[?] Choose > ")			
				brdcFile = brdcArray[int(brdcFile)]
			except IndexError:
				print ("\t\033[91m[-] File does not exist\033[00m\n")
				exit(1)
		coordTrigger = input("\t[?] Do you want to set custom coordinates? (default are Colosseum\'s ones) (y/[n]) > ") or "n"
		if coordTrigger == "y" or dlTrigger == "Y":
			lat = input("\t[?] Latitude (41.89): > ")
			lon = input("\t[?] Longitude (12.49): > ")
			hgt = input("\t[?] Height (m): > ")
			runt = input("\t[?] Run Time (sec): > ")
		else:
			lat = "41.890251"
			lon = "12.492373"
			hgt = "23"
			runt = "600"
		print("\t\033[92m[*] About to compile gpssim.bin for %s\n\033[0m" % brdcFile)
		gpssimbin(brdcFile, lat, lon, hgt, runt)
	hackrfTrigger = input("\t[?] Do you want to run hackrf_transfer? ([y]/n) > ") or "y"
	if hackrfTrigger == "y" or hackrfTrigger == "Y":
		hackrf()
	else:
		print("\t\033[91m[-] Exiting...\033[00m\n")
		exit(0)
try:
	main()
except KeyboardInterrupt:
	print ("\n\t\033[91m[-] Exiting...\033[00m\n")
	exit(0)
