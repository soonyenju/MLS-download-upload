# MLS-download-upload
>The download_mls-0529-win.py program is designed for data retrieval and upload to a pre-defined FTP sever.

`Author:` soonyenju@foxmail.com

`Date:` May 26th, 2018

`Licence:` MIT

**HOW TO USE THIS CODE**
>steps:
1. check if wget is installed and configured properly.
2. in the source code, determine the `savepath` and `time` at which you wanna the spider to crawl autmatically.

```
	savepath = "E:/AIUS"
	runTask(savepath, hour = "09")
```

3. configure the `account` and `password` of FTP server for uploading. Meanwhile, the `ftp address` and `port` should be given before.

```
	ftp.connect('58.87.100.65',port,timeout) # ftp ip
	ftp.login('tmpdata','tmpdata') # login
```

4. afterwards, go to the command line, cd to the current dir of this .py file and key in:
```
python download_mls-0529-win.py
```
and voila!

