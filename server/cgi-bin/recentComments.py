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


import os.path
import cgi
from DynaMiFLiC import DynaMiFLiC

print "Content-type: text/html\n"

form = cgi.FieldStorage()

comPath = "../db/comments/"
artPath = "../db/articles/"
obj = DynaMiFLiC(comPath)
comList = obj.lst

dic = {}

for item in comList:
	obj2 = DynaMiFLiC(comPath + item + "/")
	comList2 = obj2.lst
	for item2 in comList2:
		#create a comments dictionary adding every comment in the form "comments folder name: comment name"
		dic[int(item2)] = item

#sort dictionary items and take only last five items (last five comments)
lt = sorted(dic.items())[-5:]
lt = reversed(lt)

obj3 = DynaMiFLiC(artPath)

for item in lt:
	artContent = obj3.content(item[1])
	title = obj3.getTitle(artContent)
	comPath = item[1] + "/" + str(item[0])
	comContent = obj.content(comPath)
	name = obj.getName(comContent)
	if len(name + title) > 27:
		title = title[0:27-len(name)] + '...'
	print "<div><span>%s</span> in <a href=\"javascript:loadArticle('%s');\">%s</a></div>" % (name, item[1], title)
