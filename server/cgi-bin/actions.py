#!/usr/bin/python
#
# This file is part of DynaMiFLiC
#
# Copyright (C) 2012 slacknux <slacknux@gmail.com>
# http://www.slacknux.net
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import cgi
import time
import re
from DynaMiFLiC import DynaMiFLiC
import shutil
import hashlib
import tarfile
import cStringIO


def new():
	idArticle = "%.2f" % time.time()
	idArticle = idArticle.replace(".","")
	dateArticle = time.strftime("%d %b %Y - %H:%M:%S")
	obj = DynaMiFLiC("../db/articles/")
	parsed = obj.artParser(form["article"].value)
	fp = open("../db/articles/" + idArticle, "w")
	fp.write('\n<div id="articleHeader">\n<div id="title">%s</div>\n<div>%s posted by %s</div>\n</div>\n<div id="share">\n<a href="http://twitter.com/share?url=%s/#%s&text=%s" class="twitter-share-button" data-count="horizontal">Tweet</a>\n<script type="text/javascript" src="http://platform.twitter.com/widgets.js"></script>\n<a name="fb_share" type="button_count" href="http://www.facebook.com/sharer.php?u=%s/?%s&t=%s">share</a>\n<script src="http://static.ak.fbcdn.net/connect.php/js/FB.Share" type="text/javascript"></script>\n</div><div class="clear"></div><div id="articleMain">%s</div>' % (form['title'].value, dateArticle, name, url, idArticle, form['title'].value, url, idArticle, form['title'].value, parsed))
	fp.close()
	os.mkdir("../db/comments/" + idArticle)
	print "[+]Article added successfully!"


def edita():
	obj = DynaMiFLiC("../db/articles/")
	artList = obj.lst
	if not "ed" in form:
		if len(artList) > 0:
			for item in artList:
				artContent = obj.content(item)
				title = obj.getTitle(artContent)
				print "Id:%s\tTitle: %s" % (artList.index(item)+1, title)
		else:
			print "No articles present!"
	else:
		idArticle = int(form["ed"].value)-1
		if not "edited" in form:
			if idArticle in range(len(artList)):
				artContent = obj.content(artList[idArticle])
				print artContent
			else:
				print "[*]Wrong article id!"
		else:
			parsed = obj.artParser(form["edited"].value)
			fp = open("../db/articles/" + artList[idArticle], "w")
			fp.write(parsed)
			fp.close()
			print "[*]Article edited successfully!"


def editc():
	obj = DynaMiFLiC("../db/comments/")
	artList = obj.lst
	obj2 = DynaMiFLiC("../db/articles/")
	if not "ed" in form:
		flag = 0
		for i in artList:
			obj3 = DynaMiFLiC("../db/comments/" + i + "/")
			artList3 = obj3.lst
			if len(artList3) == 0:
				flag = flag + 1
				continue
			artContent = obj2.content(i)
			title = obj2.getTitle(artContent)
			for j in artList3:
				comContent = obj3.content(j)
				name = obj.getName(comContent)
				print "Id:%s.%s\tName: %s\tArticle: %s" % (artList.index(i)+1, artList3.index(j)+1, name, title)
		if len(artList) == flag:
			print "No comments present!"
	else:
		edid = form["ed"].value.split(".")
		edid[0] = int(edid[0])-1
		edid[1] = int(edid[1])-1
		obj3 = DynaMiFLiC("../db/comments/" + artList[edid[0]] + "/")
		artList3 = obj3.lst
		if not "edited" in form:
			if edid[0] in range(len(artList)) and edid[1] in range(len(artList3)):
				comContent = obj3.content(artList3[edid[1]])
				print comContent
			else:
				print "[*]Wrong comment id!"
		else:
			edited = form["edited"].value
			fp = open("../db/comments/" + artList[edid[0]] + "/" + artList3[edid[1]], "w")
			fp.write(edited)
			fp.close()
			print "[*]Comment edited successfully!"


def rma():
	obj = DynaMiFLiC("../db/articles/")
	artList = obj.lst
	if not "rm" in form:
		if len(artList) > 0:
			for i in artList:
				artContent = obj.content(i)
				title = obj.getTitle(artContent)
				print "Id:%s\tTitle: %s" % (artList.index(i)+1, title)
		else:
			print "No articles present!"
	else:
		rmid = int(form["rm"].value)-1
		if rmid in range(len(artList)):
			os.remove("../db/articles/" + artList[rmid])
			shutil.rmtree("../db/comments/" + artList[rmid])
			print "[-]Article removed successfully!"
		else:
			print "[*]Wrong article id!"
			

def rmc():
	obj = DynaMiFLiC("../db/comments/")
	artList = obj.lst
	obj2 = DynaMiFLiC("../db/articles/")
	if not 'rm' in form:
		flag=0
		for i in artList:
			obj3 = DynaMiFLiC("../db/comments/" + i + "/")
			artList3 = obj3.lst
			if len(artList3) == 0:
				flag = flag + 1
				continue
			artContent = obj2.content(i)
			title = obj2.getTitle(artContent)
			for j in artList3:
				comContent = obj3.content(j)
				name = obj.getName(comContent)
				print "Id:%s.%s\tName: %s\tArticle: %s" % (artList.index(i)+1, artList3.index(j)+1, name, title)
		if len(artList) == flag:
			print "No comments present!"
	else:
		rmid = form["rm"].value.split(".")
		rmid[0] = int(rmid[0])-1
		rmid[1] = int(rmid[1])-1
		obj3 = DynaMiFLiC("../db/comments/" + artList[rmid[0]])
		artList3 = obj3.lst
		if rmid[0] in range(len(artList)) and rmid[1] in range(len(artList3)):
				os.remove("../db/comments/" + artList[rmid[0]] + "/" +artList3[rmid[1]])
				print "[-]Comment removed successfully!"
		else:
			print "[*]Wrong comment id!"


def download():
	fpio = cStringIO.StringIO()
	tar = tarfile.open(name=None, mode="w:bz2", fileobj=fpio)
	tar.add("../db/")
	tar.close()
	archive = fpio.getvalue()
	fpio.close()
	checksum = hashlib.md5()
	for i in range(0, len(archive), 128):
		data = archive[i:i+128]
		checksum.update(data)
	print archive + checksum.hexdigest()


def logs():
	fp = open("./logs.py", "r")
	data = fp.readlines()
	fp.close
	if len(data) > 2:
		for i in range(2, len(data)):
			print data[i][1:-1]
	else:
		print "No logs present!"





form = cgi.FieldStorage(keep_blank_values=1)
username = form["username"].value
password = form["password"].value

print "Content-type: text/html\n"

if os.path.exists("config.py"):
	fp = open("config.py", "r")
	data = fp.readlines()
	user = data[2][12:-1]
	passwd = data[3][12:-1]
	name = data[4][8:-1]
	url = data[6][7:-1]
	chc = data[7][10:-1]
	fp.close()
	
	if chc == "n":
		username = hashlib.sha256(username).hexdigest()
		password = hashlib.sha256(password).hexdigest()	
	
	if user == username and passwd == password:
		if "action" in form:
			action = form["action"].value
			
			if action == "new":
				new()
			elif action == "edita":
				edita()
			elif action == "editc":
				editc()
			elif action == "rmc":
				rmc()
			elif action == "rma":
				rma()
			elif action == "download":
				download()
			elif action == "logs":
				logs()
	else:
		print "[*]Wrong username and/or password"
		fp = open("./logs.py", "a")
		fp.write("#Date: %s IP: %s UA: %s" % (time.strftime("%d/%m/%Y %H:%M:%S"), os.environ.get("REMOTE_ADDR"), os.environ.get("HTTP_USER_AGENT")))
		if "action" in form:
			fp.write(" Action: %s" % form["action"].value)
		else:
			fp.write(" Error:Login Error")
		fp.write("\n")
		fp.close()
else:
	print "[*]Missing config file"
