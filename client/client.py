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


import readline
import getopt
import os
import sys
import urllib
import hashlib
import getpass
import re
import time

def completer(text, state):
    text = readline.get_line_buffer().split()
    my_list = ("<div></div>", "<p></p>", "<span></span>", "<h1></h1>", "<h2></h2>", "<h3></h3>", "<h4></h4>", "<h5></h5>", "<h6></h6>", "<pre></pre>", "<ul></ul>", "<li></li>", "<strong></strong>", "<table></table>", "<tr></tr>", "<td></td>", '<a href=""></a>', "<sub></sub>", "<sup></sup>", '<img src="" />', "[b][/b]", "[i][/i]", "[u][/u]", "[s][/s]", "[url][/url]", "[img][/img]", "[code][/code]", "[size=][/size]", "[color=][/color]", "[center][/center]", "[right][/right]")
    result = [x for x in my_list if x.startswith(text[len(text)-1])]
    return result[state][1:]


def new():
	title = raw_input("Title: ")
	article = ""
	print "Article text:"
	#autocompletion on
	readline.set_completer(completer)
	readline.parse_and_bind("tab: complete")
	while True:
		line = raw_input()
		if line != ":w":
			article += (line + "<br />")
		else:
			break
	params = urllib.urlencode({"username":username, "password":password, "action":"new", "title":title, "article":article})
	f = urllib.urlopen(url + "/cgi-bin/actions.py", params)
	print f.read()
	#autocompletion off
	readline.set_completer(None)
	readline.parse_and_bind("tab: tab-insert")


def edita():
	params = urllib.urlencode({"username":username, "password":password, "action":"edita"})
	f = urllib.urlopen(url + "/cgi-bin/actions.py", params)
	result = f.read()
	print result
	if "No articles present!" not in result:
		id = raw_input("Id of the article to edit: ")
		params = urllib.urlencode({"username":username, "password":password, "action":"edita", "ed":id})
		f = urllib.urlopen(url + "/cgi-bin/actions.py", params)
		result = f.read()
		if not "[*]Wrong article id!" in result:
			readline.set_startup_hook(lambda: readline.insert_text(result))
			try:
				artContent =raw_input("\n-Editing- (press Enter to send)\n")
			finally:
				readline.set_startup_hook()
			params = urllib.urlencode({"username":username, "password":password, "action":"edita", "ed":id, "edited":artContent})
			f = urllib.urlopen(url + "/cgi-bin/actions.py", params)
			print f.read()
		else:
			print result


def editc():
	params = urllib.urlencode({"username":username, "password":password, "action":"editc"})
	f = urllib.urlopen(url + "/cgi-bin/actions.py", params)
	result = f.read()
	print result
	if not "No comments present!" in result:
		id = raw_input("Id of the comment to edit: ")
		params = urllib.urlencode({"username":username, "password":password, "action":"editc", "ed":id})
		f = urllib.urlopen(url + "/cgi-bin/actions.py", params)
		result = f.read()
		if not "[*]Wrong comment id!" in result:
			readline.set_startup_hook(lambda: readline.insert_text(result))
			try:
				comContent = raw_input("\n-Editing- (press Enter to send)\n")
			finally:
				readline.set_startup_hook()
			params = urllib.urlencode({"username":username, "password":password, "action":"editc", "ed":id, "edited":comContent})
			f = urllib.urlopen(url + "/cgi-bin/actions.py", params)
			print f.read()
		else:
			print result


def rma():
	params = urllib.urlencode({"username":username, "password":password, "action":"rma"})
	f = urllib.urlopen(url + "/cgi-bin/actions.py", params)
	result = f.read()
	print result
	if not "No articles present!" in result:
		id = raw_input("Id of the article to remove (also comments will be removed): ")
		params = urllib.urlencode({"username":username, "password":password, "action":"rma", "rm":id})
		f = urllib.urlopen(url + "/cgi-bin/actions.py", params)
		print f.read()


def rmc():
	params = urllib.urlencode({"username":username, "password":password, "action":"rmc"})
	f = urllib.urlopen(url + "/cgi-bin/actions.py", params)
	result = f.read()
	print result
	if not "No comments present!" in result:
		id = raw_input("Id of the comment to remove: ")
		params = urllib.urlencode({"username":username, "password":password, "action":"rmc", "rm":id})
		f = urllib.urlopen(url + "/cgi-bin/actions.py", params)
		print f.read()


def download():
	print "\nDownloading..."
	print "\033[2A"
	params = urllib.urlencode({"username":username, "password":password, "action":"download"})
	f = urllib.urlopen(url + "/cgi-bin/actions.py", params)
	result = f.read()
	archive = result[:-33]
	checksum = hashlib.md5()
	for i in range(0, len(archive), 128):
		data = archive[i:i+128]
		checksum.update(data)
	if checksum.hexdigest() == result[-33:-1]:
		archiveName = "%s.tar.bz2" % (time.strftime("%d%m%Y"))
		tar = open(archiveName, "w")
		tar.write(archive)
		tar.close()
		print "[*]Database downloaded succesfully!\n"
	else:
		print "[*]Package corrupted, try again!\n"


def logs():
	params = urllib.urlencode({"username":username, "password":password, "action":"logs"})
	f = urllib.urlopen(url + "/cgi-bin/actions.py", params)
	result = f.read()
	print result
	
	
def commands():
	print "\n\033[4mCommands\033[m        \033[4mActions\033[m\
	\nnew		New article\
	\nedita		Edit article\
	\neditc		Edit comment\
	\nrma		Remove article\
	\nrmc		Remove comment\
	\ndownload	Download the whole DB\
	\nlogs		Show logs\
	\nexit		Quit\
	\n:w		Save article (inside article in a new line)\
	\n\n\033[4mBBCode:\033[m\
	\n[b]text[/b]	       [i]text[/i]		     [u]text[/u]\
	\n[s]text[/s]	       [size=number]text[/size]	     [color=color]text[/color]\
	\n[url]url[/url]	       [url=link]text[/url]	     [img]url[/img]\
	\n[code]code[/code]      [center]text[/center]	     [right]text[/right]\n"





print "=============================================\
	 \n DynaMiFLiC v1.0 client - Copyright (c) 2012 \
	 \n slacknux <slacknux@gmail.com>               \
	 \n http://www.slacknux.net                     \
	 \n============================================="

if os.path.exists('config'):
	#readline.set_completer(completer)
	print "\nType --help for commands information\n"
	action = ""
	fp = open("config", "r")
	data = fp.readlines()
	url = data[2][:-1]
	name = data[3][:-1]
	
	if len(data) > 4:
		username = data[4][:-1]
		password = data[5][:-1]
	else:
		username = getpass.getpass("Username: ")
		print "\033[2A"
		password = getpass.getpass()
		print "\033[2A"
	fp.close()
	
	try:
		params = urllib.urlencode({"username":username, "password":password})
		f = urllib.urlopen(url+"/cgi-bin/actions.py", params)
	except:
		print "[*]No response from server\n"
		sys.exit(1)
	
	result = f.read()
	print result
	
	if "[*]Missing config file" in result or "[*]Wrong username and/or password" in result:
		sys.exit(1)
	
	print "\033[2A"
	
	while True:
		action = raw_input(name + "@" + url[7:] + ":~# ")
		if action == "new":
			new()
		elif action == "edita":
			edita()
		elif action == "editc":
			editc()
		elif action == "rma":
			rma()
		elif action == "rmc":
			rmc()
		elif action == "download":
			download()
		elif action == "logs":
			logs()
		elif action == "exit":
			sys.exit(1)
		elif action == "--help":
			commands()
		elif action == "":
			continue
		else:
			print "%s: command not found" % action
else:
	print "\nThis is your first access or config file missing. Configure required data.\n"
	user = raw_input("Username: ")
	password = getpass.getpass()
	name = raw_input("Name to display in articles: ")
	email = raw_input("Email for Gravatar: ")
	url = raw_input("Your blog URL: ")
	print "Save data permanently?\ny (username and password will be not required every time)\nn (username and password will be required every time; more safe)"
	ans = raw_input()
	hashUser = hashlib.sha256(user).hexdigest()
	hashPassword = hashlib.sha256(password).hexdigest()
	hashEmail = hashlib.md5(email).hexdigest()
	if not url.startswith("http://"):
		url = "http://" + url
	fp = open("config", "w")
	if ans == "y":
		fp.write("######### Blog data #########\n\n%s\n%s\n%s\n%s\n" % (url, name, hashUser, hashPassword))
	else:
		fp.write("######### Blog data #########\n\n%s\n%s\n" % (url, name))
	fp.close()
	
	fp = open("../server/cgi-bin/config.py", "w")
	fp.write("#!/usr/bin/python\n\n#Username = %s\n#Password = %s\n#Name = %s\n#Email = %s\n#URL = %s\n#Choice = %s\n" % (hashUser, hashPassword, name, hashEmail, url, ans))
	fp.close()
	print "\n[*]Config files successful created!\n"
