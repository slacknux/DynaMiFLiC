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
import random
import hashlib
import cStringIO
import Image
import ImageDraw
import ImageFont
import ImageFilter
import time

#generate pseudo-random word
def gen_word():
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        word = ""
        for i in range(0, 18):
                word = word + chars[random.randint(0,0xffffff) % len(chars)]
        return word

#generate captcha hash
def gen_captcha_hash(text):
	ra = os.environ.get("REMOTE_ADDR")
	hua = cgi.escape(os.environ.get("HTTP_USER_AGENT"))
	captcha = "".join([text, hua, ra])
	captchaHash = hashlib.md5(captcha)
	return captchaHash.hexdigest()[0:6]

#generate captcha image
def gen_captcha_img(txt):
	im = Image.new("RGB", (160,60), "#444")
	draw = ImageDraw.Draw(im)
	x, y = im.size
	pnt = random.randint
	for i in range(300):
		draw.point((pnt(0,x),pnt(0,y),pnt(0,x),pnt(0,y)), fill="#666")
	font = ImageFont.truetype("../font/Cashier.ttf", 35)
	draw.text((23,9), txt, font=font, fill="#fff")
	im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
	f = cStringIO.StringIO()
	im.save(f, "JPEG")
	f = f.getvalue()
	data_uri = f.encode("base64").replace("\n", "")
	img = '<img src="data:image/jpeg;base64,%s" />' % (data_uri)
	img = img + '<br /><span>Type the word</span><br /><input type="text" name="captcha" maxlength="6">'
	print img
	f.close()


def main():
	form = cgi.FieldStorage()
	if "captcha" in form:
		word = gen_word()
		shortHash = gen_captcha_hash(word)
		#must be the same in form.py
		salt = "DynaMiFLiC"
		hashCookie = hashlib.md5(salt + shortHash).hexdigest()
		print "Set-Cookie: captcha=%s; expires=%s; path=/" % (hashCookie, time.asctime(time.gmtime(time.time()+900)))
		print "Content-type: text/html\n"
		gen_captcha_img(shortHash)


if __name__ == "__main__":
	main()
