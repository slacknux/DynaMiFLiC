/*
 * This file is part of DynaMiFLiC
 *
 * Copyright (C) 2012 slacknux <slacknux@gmail.com>
 * http://www.slacknux.net
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

var count = 0;							//position in articles list
var idList = [];						//articles list

function loadArticle(id) {
	count = $.inArray(id, idList);		//update actual position in articles list
	
	$.post("../cgi-bin/loadArticle.py",
		{
			article: id
		},
		function(data) {
			$('#article').css("opacity",0).html(data).fadeTo(700, 1);
		}
	);
	
	showComments(id);
}

function getCaptcha() {
	$.post('../cgi-bin/captcha.py',
		{
			captcha: 1
		},
		function(data) {
			$('#captcha').html(data);
		}
	);
}

function leaveComment() {
	var form = '<div id="formComment">\
	<input type="text" name="name" maxlength="25"><label>name (required)</label><br>\
	<input type="text" name="email"><label>email (optional for Gravatar)</label><br>\
	<input type="text" name="website"><label>website</label><span id="info" onmouseover="javascript:$(\'#allow\').fadeIn(400)" onmouseout="javascript:$(\'#allow\').fadeOut(400)">?</span><div id="allow" style="margin: 2px 5px; width: 345px; background-color: #bcbcbc; position: absolute; display: none;"><span style="font-weight: 800;">allowed tags:</span> &lt;i&gt; &lt;u&gt; &lt;strong&gt; &lt;strike&gt; &lt;a&gt; &lt;pre&gt; &lt;q&gt; &lt;cite&gt; &lt;blockquote&gt;</div>\
	<textarea name="text"></textarea><br>\
	<input type="button" value="submit" onclick="sendComment();"><span id="status"></span>\
	</div>\
	<div id="captcha"></div>\
	<div class="clear"></div>';
	
	$('#leaveComment').css("opacity",1);
	$('#showComments').css("opacity",0.3);
	$('#comments').html(form).css("opacity",0).fadeTo(500,1);
	
	getCaptcha();
}

function sendComment() {
	var name = $('input[name="name"]').val();
	var email = $('input[name="email"]').val();
	var website = $('input[name="website"]').val();
	var text = $('textarea').val() ;
	var captcha = $('input[name="captcha"]').val();
	
	if (name == ''){
		$('#status').css({"opacity": 0, "padding": "2px"}).html('name required').fadeTo(400, 1);
		return;
	}
	else if (text == '') {
		$('#status').css({"opacity": 0, "padding": "2px"}).html('message required').fadeTo(400, 1);
		return;
	}
	else if (captcha == '') {
		$('#status').css({"opacity": 0, "padding": "2px"}).html('captcha required').fadeTo(400, 1);
		return;
	}
	
	$.post('../cgi-bin/form.py',
		{
			name: name,
			email: email,
			website: website,
			text: text,
			captcha: captcha,
			artId: idList[count]
		},
		function(data) {
			$('#status').css({"opacity": 0, "padding": "2px"}).html(data).fadeTo(400, 1);
			if (data.search("Comment added!")!=-1) {
				recentComments();
				$('#formComment input, textarea, #captcha input').not('input:button').val('');
			}
			getCaptcha();
		}
	);
}

function search() {	
	$('#showComments,#leaveComment,#comments').css("display", "none");
	
	if ($('#menu input:text').val() == '') {
		$('#article').css("opacity",0).html('<div id="errorSearch">Type a valid keyword!</div>').fadeTo(400, 1);
		return false;
	}

	var keyword = $('#menu input:text').val();
	
	$.post('../cgi-bin/search.py',
		{
			keyword: keyword
		},
		function(data) {
			$('#article').css("opacity",0).html(data).fadeTo(400, 1);
		}
	);
	
	$('#menu input:text').val('');
}

function articlesList() {
		$.post('/cgi-bin/articlesList.py',
			{
				list: 1
			},
			function(data) {
				$('#articlesList').html(data);
			}
		);
}

function showComments(id) {
	$('#showComments').css("opacity",1);
	$('#leaveComment').css("opacity",0.3);
	
	$.post('../cgi-bin/loadComments.py',
		{
			comments: id
		},
		function(data) {
			$('#comments').css("opacity",0).html(data).fadeTo(500, 1);
			if ($('#showComments,#leaveComment').is(':hidden'))
				$('#showComments,#leaveComment').css("display", "block");
		}
	);
}

function slide(val) {
	val == 'next' ? count-- : count++;

	if (count >= idList.length)
		count-=idList.length;
	else if (count<0)
		count+=idList.length;

	loadArticle(idList[count]);
}

function recentComments() {
	$.post('../cgi-bin/recentComments.py',
		{
			rcomments: 1
		},
		function(data) {
			$('#recentComments').css("opacity",0).html(data).fadeTo(700, 1);
		}
	);
}

$(function () {
	$.post('../cgi-bin/loadArticle.py',
		{
			init: 1
		},
		function(data) {
			idList = data;
			url = document.location.href;
			if (url.indexOf('#') != -1) {	//check in the case of referrer is twitter (from sharing function)
				url = url.split('#');
				loadArticle(url[1]);
			}
			else if (url.indexOf('?') != -1) {	//check in the case of referrer is facebook (from sharing function)
				url = url.split('?');
				loadArticle(url[1]);
			}
			else {
				loadArticle(idList[count]);
			}
		},
		'json'
	);
	
	recentComments();
	articlesList();
	
	$(document).keydown(function(event){if(event.keyCode == 37){if(!$('input,textarea,#leaveComment,#commemts').is(':focus')) slide('prev');}});
	$(document).keydown(function(event){if(event.keyCode == 39){if(!$('input,textarea,#leaveComment,#commemts').is(':focus')) slide('next');}});
	$('input[name="search"]').keypress(function(event){if(event.keyCode == 13){search();}});
	$('#alist').click(function(){$('#articlesList').slideToggle(400);});
	$('#showComments').click(function(){showComments(idList[count]);});
	$('#leaveComment').click(function(){leaveComment();});
	$("#prev").mouseenter(function(){$("#leftArrow").fadeIn(500);$("#leftArrow").fadeOut(300);});
	$("#next").mouseenter(function(){$("#rightArrow").fadeIn(500);$("#rightArrow").fadeOut(300);});
});
