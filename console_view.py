#! /usr/bin/python
#-*-coding:utf-8-*- 
import urllib.request
import json
import sys, time
import curses
import hmac,hashlib
import conf
class console_view:
	def __init__(self, x = 0, y = 0, width = 80, height = 15, is_view = True):
		self.display_pos = {'x':x, 'y':y, 'width':width, 'height':height}
		self.is_view = is_view
		self.view_mode = 'simp'
