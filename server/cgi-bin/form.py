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
import sys
import re
import cgi
import hashlib
import time
import Cookie
from DynaMiFLiC import DynaMiFLiC

print "Content-type: text/html\n"

form = cgi.FieldStorage(keep_blank_values=1)

artId = form["artId"].value
comPath = "../db/comments/" + artId

obj = DynaMiFLiC(comPath)

tm = time.strftime("%d %b %Y - %H:%M:%S")
name = obj.escape(form["name"].value)
email = obj.escape(form["email"].value)
website = obj.escape(form["website"].value)
text = obj.comParser(form["text"].value)
captcha = obj.escape(form["captcha"].value).lower()

if email:
	#if it's not a valid email address, you'll be adivised
	if not re.match(r'^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z.]{2,5}$', email):
		print "invalid email address"
		sys.exit()

###Gravatar stuff###
emailHash = hashlib.md5(email).hexdigest()
img = "<img src=\"http://www.gravatar.com/avatar/%s.jpg?s=35&d=http://dynamiflic.slacknux.net/img/avatar.png\">" % (emailHash)
####################

if website:
	if not website.startswith("http://"):
		website = "http://" + website
	name = "<a href=\"%s\">%s</a>" % (website, name)

#must be the same in captcha.py
salt = "DynaMiFLiC"
hashCaptcha = hashlib.md5(salt + captcha).hexdigest()

hashCookie=""
#get cookies
cookiesString = os.environ.get("HTTP_COOKIE")

if cookiesString and "captcha" in cookiesString:
	cookies = Cookie.SimpleCookie()
	cookies.load(cookiesString)
	#get captcha hash value
	hashCookie = cookies["captcha"].value

if hashCaptcha != hashCookie:
	print "invalid captcha!"
	sys.exit()

newCom = "%.2f" % time.time()
newCom = newCom.replace('.','')

try:
	fp = open("config.py", "r")
	data = fp.readlines()
	data_mail = data[5][9:-1]
	fp.close()
	
	comPath = comPath + "/" + newCom
	fp = open(comPath, "w")
	
	if emailHash != data_mail:
		fp.write('<div class="comment"><div class="avatar">%s</div><div class="user"><div class="username">%s</div><div class="date">%s</div></div><div class="clear"></div><div class="message">%s</div></div>' % (img, name, tm, text))
	else:
		fp.write('<div class="comment"><div class="myavatar">%s</div><div class="myuser"><div class="myusername">%s</div><div class="date">%s</div></div><div class="clear"></div><div class="message">%s</div></div>' % (img, name, tm, text))

	fp.close()
	
	print "Comment added!"
  
except:
	print "A problem occurred! Try again"
