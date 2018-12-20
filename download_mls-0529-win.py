# coding: utf-8
"""
Author: Soonyen Ju
Date: May 29th, 2018
Contact: soonyenju@foxmail.com
Description:
This code is designed for MLS auxillary files download and pack
"""
import re, os, tarfile
from ftplib import FTP
from datetime import *

def main():
	print("testing...")
	savepath = "E:/AIUS"
	runTask(savepath, hour = "09")

def runTask(savepath, hour):
	run_time = datetime.strftime(datetime.now(), "%Y-%m-%d:")
	run_time = datetime.strptime(run_time + hour, "%Y-%m-%d:%H")
	period = timedelta(1)
	print("check...")
	while True:
		now = datetime.now()
		if datetime.strftime(now, "%Y-%m-%d:%H") == datetime.strftime(run_time, "%Y-%m-%d:%H"):
			print("start run at " + datetime.strftime(now, "%Y-%m-%d %H:%M"))
			temp_exp = r"MLS-Aura_L2GP-Temperature_v04-23-c01_[\d]{4}d[\d]{3}.he5"
			temp_name, dn_date = download(run_time, savepath, temp_exp)
			gph_exp = r"MLS-Aura_L2GP-GPH_v04-23-c01_[\d]{4}d[\d]{3}.he5"
			gph_name, dn_date = download(run_time, savepath, gph_exp)
			print(temp_name, gph_name)
			new_folderdir = os.path.join(savepath, "ENV-GF5-AIUS-" + dn_date)
			if not os.path.exists(new_folderdir): os.makedirs(new_folderdir)
			f = open(os.path.join(savepath, "ENV-GF5-AIUS-" + dn_date + ".fn"), "w"); f.close()
			new_temp_filedir = os.path.join(savepath, new_folderdir + "/" +"ENV-GF5-AIUS-Temperature-" + dn_date + ".he5")
			os.rename(os.path.join(savepath, temp_name), new_temp_filedir)
			new_gph_filedir = os.path.join(savepath, new_folderdir + "/" +"ENV-GF5-AIUS-GPH-" + dn_date + ".he5")
			os.rename(os.path.join(savepath, gph_name), new_gph_filedir)
			tar = tarfile.open(os.path.join(savepath, os.path.basename(new_folderdir) + ".tar.gz"),"w:gz")
			for root, _, files in os.walk(new_folderdir):
				for file in files:
					fullpath = os.path.join(root,file)
					tar.add(fullpath, arcname = os.path.basename(fullpath))
			tar.close()
			os.remove(new_temp_filedir)
			os.remove(new_gph_filedir)
			os.rmdir(new_folderdir)
			ftpupload(savepath, "ENV-GF5-AIUS-" + dn_date)
			run_time = run_time + period
			print("next run at " + datetime.strftime(run_time, "%Y-%m-%d %H:%M"))
		exit(0)

def download(run_time, savepath, expression, delta = 3):
	dn_time = run_time - timedelta(delta)
	dn_date = datetime.strftime(dn_time, "%Y%m%d")
	dn_time = datetime.strftime(dn_time, "%Yd%j")
	code = "wget --content-disposition --load-cookies = cookies1.txt --save-cookies = cookies.txt --auth-no-challenge=on --keep-session-cookies -c http://acdisc.gesdisc.eosdis.nasa.gov/data///Aura_MLS_Level2/ML2T.004/2016/MLS-Aura_L2GP-Temperature_v04-23-c01_2016d356.he5 -P " + savepath
	regex = re.compile(r"[\d]{4}d[\d]{3}")
	flag = re.findall(regex, code)
	code = regex.sub(lambda m: dn_time, code)
	regex = re.compile(r"/[\d]{4}/")
	flag = re.findall(regex, code)
	code = regex.sub(lambda m: "/" + dn_time[0: 4] + "/", code)
	try:
		os.system(code)
	except:
		print("No data availabe on " + dn_time)
	# regex = re.compile(r"MLS-Aura_L2GP-Temperature_v04-23-c01_[\d]{4}d[\d]{3}.he5")
	regex = re.compile(expression)
	flag = re.findall(regex, code)
	return flag[0], dn_date

def ftpupload(savepath, file):
	ftp = FTP()
	timeout = 30
	port = 21
	ftp.connect('58.87.100.65',port,timeout) # ftp ip
	ftp.login('tmpdata','tmpdata') # login

	print(ftp.getwelcome())
	ftp.cwd("/")
	path_list = savepath.split("/")[1::]
	for path in path_list:
		if path in ftp.nlst():
			print(path + " exists already")
			ftp.cwd(path)
			print("change to " + path)
		elif not path in ftp.nlst():
			ftp.mkd(path)
			print(path + " is created.")
			ftp.cwd(path)
			print("change to " + path)
	print("current path is " + ftp.pwd())

	filename = file + ".tar.gz"
	uploadfile(ftp, filename, os.path.join(savepath, filename))
	print("uploadfile .gz successfully")

	filename = file + ".fn"
	uploadfile(ftp, filename, os.path.join(savepath, filename))
	print("uploadfile .fn successfully")

	ftp.quit()

def uploadfile(ftp, remotepath, localpath):
	bufsize = 1024
	fp = open(localpath, 'rb')
	ftp.storbinary('STOR '+ remotepath , fp, bufsize) #上传文件
	ftp.set_debuglevel(0)
	fp.close()

if __name__ == '__main__':
	main()