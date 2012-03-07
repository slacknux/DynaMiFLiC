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


import cgi
from DynaMiFLiC import DynaMiFLiC

print "Content-type: text/html\n"

artPath = "../db/articles/"

form = cgi.FieldStorage()

if "list" in form:
	obj = DynaMiFLiC(artPath)
	artList = obj.lst
	artList.reverse()
	
	print "<ul>"
	for item in artList:
		artContent = obj.content(item)
		title = obj.getTitle(artContent)
		print "<li><a href=\"javascript:loadArticle('%s');\" onclick=\"$('#articlesList').slideUp(300);\">%s</a></li>" % (item, title)
	print "</ul>"
