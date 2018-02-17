#!/usr/bin/python
# -*- coding: utf-8 -*- 
# @File Name: findthreshold.py
# @Created:   2018-02-16 19:18:49  seo (simon.seo@nyu.edu) 
# @Updated:   2018-02-16 19:50:26  Simon Seo (simon.seo@nyu.edu)
# for given (b,r) parameters, finds at which point s in [0,1] the slope is maximum.
# also finds probability of document pairs that have JS=S is in candidate pairs

srange = range(0,1000)
br = [(32,4), (16,8), (32,8)]
max_slope_threshold = (0, -1) # (s, f'(s))
fx = lambda s,b,r: 1-(1-s**r)**b
S = 0.75

for (b,r) in br:
	for s in srange:
		s = s/1000
		fpx = r*b*(1-s**r)**(b-1)*s**(r-1)
		if fpx > max_slope_threshold[1]:
			# print(max_slope_threshold)
			max_slope_threshold = (s, fpx)
	print("b {} r {} threshold {} p({}) {}".format(b, r, max_slope_threshold[0], S, fx(S, b, r)))



