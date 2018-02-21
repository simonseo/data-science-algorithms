#!/usr/bin/python
# -*- coding: utf-8 -*- 
# @File Name: LogCounter.py
# @Created:   2018-02-21 04:30:16  Simon Myunggun Seo (simon.seo@nyu.edu) 
# @Updated:   2018-02-21 04:54:41  Simon Seo (simon.seo@nyu.edu)
import math

class LogCounter():
	"""counts in exponential unit"""
	def __init__(self, base=10):
		if base == 10:
			self.log = math.log10
		elif base == 2:
			self.log = math.log2
		elif base == 'e':
			self.log = math.log
		else:
			self.log = lambda x: math.log(x, base)
		self.count = 0
		self.logcount = 0

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, exc_traceback):
		if exc_value == None:
			print("Successful loop. Count: {}".format(self.count))
		else:
			print("Loop failed.")
		return True

	def increment(self, msg=""):
		self.count += 1
		if self.log(self.count) == self.logcount:
			self.logcount += 1
			print(self.count, msg)
