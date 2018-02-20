#!/usr/bin/python
# -*- coding: utf-8 -*- 
# @File Name: preAnalysis.py
# @Created:   2018-02-21 00:41:31  Simon Myunggun Seo (simon.seo@nyu.edu) 
# @Updated:   2018-02-21 03:07:36  Simon Seo (simon.seo@nyu.edu)
import string
import matplotlib.pyplot as plt
from functools import reduce
import math

def getWords(line):
	words = line.strip().lower().split(',')
	return list( map(lambda w: w.strip(string.punctuation), words) )

def cosd(u, v):
	'''cosine distance function
	u, v = user entries from userDict
	m = length of user/random vector'''
	midSet = set(u.keys()) & set(v.keys())
	dotproduct = 0
	for mid in midSet:
		dotproduct += u.get(mid, None) * v.get(mid, None)
	square = lambda x: x**2
	add = lambda x, y: x + y
	mag = reduce(add, map(square, u.values())) * reduce(add, map(square, v.values())) #|u|*|v|
	mag **= 1/2
	assert mag != 0
	return math.acos(dotproduct/mag)

def createUserDict(filename="ratings.csv"):
	userDict = {}
	midSet = set([])

	with open(filename, "r") as infile:
		lst = list(map(getWords, infile.read().splitlines()))
		lst = list(map(lambda t: (int(t[0]), (int(t[1]), float(t[2]))), lst)) #(uid, (mid, r))

	for rating in lst:
		(uid, (mid, r)) = rating
		midSet.add(mid)
		user = userDict.get(uid, {})
		user[mid] = r
		userDict[uid] = user
	return userDict, midSet

def cosDistanceHistogram(userDict):
	cosds = []
	for u in userDict.values():
		for v in userDict.values():
			if u != v:
				cosds.append(cosd(u,v))

	plt.subplot()
	plt.hist(cosds, 'auto')
	plt.show()

	return cosds

def rbCandidates(p=.98, s=.43, rrange=range(2, 20), brange=range(1, 20)):
	# Finds (b,r) parameters required for documents of 
	# JS similarity s to be in candidate groups with probability p
	q = 1 - p
	res = []

	for b in brange:
		for r in rrange:
			if (1 - s**r < q**(1/b)):
				res.append((r,b))
	l = len(res)
	print(l, "candidates for r,b values")
	if l < 250:
		print(res)
	return res

def rbAnalysis(rb=[(4,32), (8,16), (8,32), (4,8), (4,4), (2,8), (8,12), (12,8), (2,4)], S=.43):
	# for given (b,r) parameters, finds at which point s in [0,1] the slope is maximum.
	# also finds probability of document pairs that have JS=S is in candidate pairs
	# ordered r first, b second
	
	fx = lambda s,r,b: 1-(1-s**r)**b #the probability function
	tx = lambda r,b: (1/b)**(1/r) #approximation of threshold

	for (r,b) in rb:
		max_slope_threshold = (0, -1) # (s, f'(s))
		falsePositiveRate = 0
		falseNegativeRate = 0

		intervals = 1000
		intervalSize = 1/intervals
		for s in range(0,intervals):
			s = s/intervals
			fpx = r*b*(1-s**r)**(b-1)*s**(r-1)
			if fpx > max_slope_threshold[1]:
				max_slope_threshold = (s, fpx)
			if s < S:
				falsePositiveRate += intervalSize * fx(s,r,b) / S
			else:
				falseNegativeRate += intervalSize * (1-fx(s,r,b)) / (1-S)

		print("r={} b={} |  threshold={}  p({})={:.4f}  false-pos={:.4f}  false-neg={:.4f}"\
			.format(r, b, max_slope_threshold[0], S, fx(S, r, b), falsePositiveRate, falseNegativeRate))


if __name__ == '__main__':
	userDict, midSet = createUserDict()
	cosds = cosDistanceHistogram(userDict)
	rb = rbCandidates(p=.85, s=.43, rrange=range(1, 10), brange=range(1, 20))
	rbAnalysis(rb=rb, S=.43)



