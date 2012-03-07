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
import re
from DynaMiFLiC import DynaMiFLiC

print "Content-type: text/html\n"

artPath = "../db/articles/"
titles = {}

obj = DynaMiFLiC(artPath)
artList = obj.lst

form = cgi.FieldStorage()
keyword = obj.escape(form["keyword"].value)
#words list from search string
words = keyword.split()

print '<div id="results"><div>Search results for <span>"%s"</span>:</div>' % (keyword)

for item in artList:
	count = 0
	artContent = obj.content(item)
	#remove all html tags in the article 
	clean = re.sub(r'<[^<>]*>', ' ', artContent).strip()
	
	for word in words:
		if word.lower() in clean.lower():
			count += 1			
	if count == len(words):
		#if all words are found in the article, add article's title to the titles dictionary
		titles[int(item)] = obj.getTitle(artContent)
 
if len(titles) != 0:
	titles = sorted(titles.items())
	titles.reverse()
	print '<ul>'
	for item in titles:
		print '<li><a href="javascript:loadArticle(\'%s\');">%s</a></li>' % (str(item[0]), item[1])
	print '</ul>'
else:
	print "No results!"

print '</div>'
