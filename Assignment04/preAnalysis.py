#!/usr/bin/python
# -*- coding: utf-8 -*- 
# @File Name: preAnalysis.py
# @Created:   2018-02-21 00:41:31  Simon Myunggun Seo (simon.seo@nyu.edu) 
# @Updated:   2018-02-25 20:56:30  Simon Seo (simon.seo@nyu.edu)
import matplotlib.pyplot as plt
import math
from random import gauss
from functions import cosd, createUserDict

def cosDistanceHistogram(userDict):
	'''computes cosine distance for given sample of users and draws histogram'''
	ijcosds = []
	for i, u in userDict.items():
		for j, v in userDict.items():
			if i < j:
				ijcosds.append(((i,j), cosd(u,v)))

	plt.subplot()
	plt.hist(list(map(lambda x:x[1], ijcosds)), 'auto')
	plt.show()

	return ijcosds

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

		print("r={} b={}  \t|  threshold={} \t p({:.4f})={:.4f} \t false-pos={:.4f} \t false-neg={:.4f}"\
			.format(r, b, max_slope_threshold[0], S, fx(S, r, b), falsePositiveRate, falseNegativeRate))

def createRandomVectors(k, m, filename="randomVectors.csv"):
	'''creates k random vectors in m dimensions'''
	with open(filename, "w") as outfile:
		for i in range(k):
			for j in range(m):
				outfile.write("{:.8f} ".format(gauss(0,1)))
			outfile.write('\n')

def dot(userVector, vec, mids):
	'''userVector is a sparse vector (dictionary) of (mid,r) entries
	vec is a dense vector that has all m components(list of floats)'''
	product = 0
	for mid, r in userVector.items():
		try:
			i = mids.index(mid)
		except ValueError as e:
			print("mids length {} mid {}".format(len(mids), mid))
			raise e
		product += r * vec[i]
	return product

if __name__ == '__main__':
	userDict, midSet = createUserDict()
	cosds = cosDistanceHistogram(userDict)

	targetCosd = math.pi/4
	s = 1-(targetCosd)/math.pi # Pr(placed in same bucket if cosd=pi/4)
	rb = rbCandidates(p=.99, s=s, rrange=range(1, 10), brange=range(1, 20))
	rbAnalysis(rb=rb, S=s)

	createRandomVectors(44, len(midSet))

