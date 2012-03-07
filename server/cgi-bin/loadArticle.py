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
import json
from DynaMiFLiC import DynaMiFLiC

print "Content-type: text/html\n"

artPath = "../db/articles/"

form = cgi.FieldStorage()

obj = DynaMiFLiC(artPath)

if "init" in form:
	artList = obj.lst
	artList.reverse()
	print json.dumps(artList)

elif "article" in form:
	artContent = obj.content(form["article"].value)
	print artContent
