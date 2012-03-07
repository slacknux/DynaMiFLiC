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
import re


def parserFunc(substr):
	#escape all < and > except for the br tag
	return re.sub('<(?!(br>)|(br/>)|(br />))', '&lt;', re.sub('(?<!<br)(?<!<br/)(?<!<br /)>', '&gt;', substr.group(0)))


class DynaMiFLiC:
	def __init__(self, dirPat):
		self.pato = dirPat
		self.lst = os.listdir(dirPat)
		self.lst.sort()

	def content(self, item):
		self.input = open(self.pato + item, 'r')
		self.itemContent = self.input.read()
		self.input.close()
		return self.itemContent

	def getTitle(self, artContent):
		self.s = re.compile('<div id="title">(.*?)</div>').search(artContent)
		return self.s.group(1)

	def getName(self, comContent):
		self.s = re.compile('(<div class="username">|<div class="myusername">)(.*?)</div>').search(comContent)
		return re.sub(r'<[^<>]*>', ' ', self.s.group(2)).strip()

	def escape(self, stringa):
		escapeDic = {"&":"&amp;", '"':"&quot;", "'":"&#039;", "<":"&lt;", ">":"&gt;"}
		#escape all ', ", &, <, >
		return "".join(escapeDic.get(c,c) for c in stringa)

	def avoid(self, substr2):
		#escape all ', ", &, <, > except for the specified tags
		return re.sub('<(?!(br>)|(br/>)|(br />)|(i>)|(/i>)|(a href)|(/a>)|(cite>)|(/cite>)|(q>)|(/q>)|(blockquote>)|(/blockquote>)|(pre>)|(/pre>)|(strong>)|(/strong>)|(strike>)|(/strike>)|(u>)|(/u>))', '&lt;', re.sub('(?<!<br)(?<!<br/)(?<!<br /)(?<!<i)(?<!</i)(?<![<a href=""])(?<!</a)(?<!<cite)(?<!</cite)(?<!<q)(?<!</q)(?<!<blockquote)(?<!</blockquote)(?<!<pre)(?<!</pre)(?<!<strong)(?<!</strong)(?<!<strike)(?<!</strike)(?<!<u)(?<!</u)>', '&gt;', re.sub("'", "&#039;", re.sub('(?<!<a href=)"(?!>)', '&quot;', re.sub('(?<!<a href="[.*?])&(?!.*?">)', '&amp;', substr2)))))

	def artParser(self, artcont):
		#convert BBCode to html code
		self.dic = {'[b]':'<span style="font-weight: 800;">', '[/b]':'</span>', '[i]':'<span style="font-style: italic;">', '[/i]':'</span>', '[u]':'<span style="text-decoration: underline;">', '[/u]':'</span>', '[s]':'<span style="text-decoration: line-through;">', '[/s]':'</span>', '[code]':'<pre>', '[/code]':'</pre>', '[img]':'<img src="', '[/img]':'" />', '[center]':'<div style="text-align: center;">', '[/center]':'</div>', '[right]':'<div style="text-align: right;">', '[/right]':'</div>'}
		
		if '[url]' in artcont:
			artcont = re.sub('\[url\](.*?)\[/url\]', r'<a href="\1">\1</a>', artcont)
		if '[url=' in artcont:
			artcont = re.sub('\[url=(.*?)\](.*?)\[/url\]', r'<a href="\1">\2</a>', artcont)
		if '[color=' in artcont:
			artcont = re.sub('\[color=(.*?)\](.*?)\[/color\]', r'<span style="color:\1;">\2</span>', artcont)
		if '[size=' in artcont:
			artcont = re.sub('\[size=(.*?)\](.*?)\[/size\]', r'<span style="font-size:\1px;">\2</span>', artcont)
		
		for key in self.dic:
			artcont = artcont.replace(key, self.dic[key])
		#############################
		
		if '<pre>' in artcont:
			artcont = re.sub('(?<=<pre>)(.*?)(?=</pre>)', parserFunc, artcont)
		
		return artcont

	def comParser(self, comcont):
		self.dic = {'<i>':'<span style="font-style: italic;">', '</i>':'</span>', '<u>':'<span style="text-decoration: underline;">', '</u>':'</span>', '<strike>':'<span style="text-decoration: line-through;">', '</strike>':'</span>'}
		comcont = comcont.replace('\n', '<br />')
		
		preCont=""
		comcont = re.sub('(?<=<pre).*?(?=>)', '', comcont)
		
		comcont = re.sub('((?<=<pre>)|(?<=</pre>))<br />', '', comcont)
		
		try:
			preCont = re.compile('<pre>(.*?)</pre>').search(comcont).group(1)
		except:
			pass
		
		comcont = re.sub('((?<=<i|<u|<q)|(?<=<cite)|(?<=<blockquote)|(?<=<strong|<strike)).*?(?=>)', '', comcont)
		comcont = re.sub('(?<=href=")*javascript.*?(?=")', "javascript:void(0);", comcont)
		comcont = re.sub('href="(.*?)".*?>', r'href="\1">', comcont)
		comcont = re.sub('(?<=<pre>)(.*?)(?=</pre>)', preCont, comcont)
		
		comcont = self.avoid(comcont)
		
		#convert BBCode to html code
		for key in self.dic:
			comcont = comcont.replace(key, self.dic[key])

		if '<pre>' in comcont:
			comcont = re.sub('(?<=<pre>)(.*?)(?=</pre>)', parserFunc, comcont)
		
		return comcont
