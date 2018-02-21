#!/usr/bin/python
# -*- coding: utf-8 -*- 
# @File Name: main.py
# @Created:   2018-02-21 03:21:35  Simon Myunggun Seo (simon.seo@nyu.edu) 
# @Updated:   2018-02-21 23:08:48  Simon Seo (simon.seo@nyu.edu)
from functions import createUserDict, cosd, choose
from LogCounter import LogCounter
import math
from functools import reduce

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


# open randomVectors and userDict
userDict, mids = createUserDict("ratings.csv")
with open("randomVectors.csv", "r") as infile:
	getNums = lambda line: list(map(float, line.strip().split()))
	randomVectors = list(map(getNums, infile.read().splitlines()))

# for each randomVector, userVectors were divided into two buckets. 
# union of set of pairs from two buckets are put into a row
# 'bands' has b number of bands and each band has r number of rows
r = 4
b = 11
bands = [[[] for j in range(r)] for i in range(b)]

with LogCounter(base=16) as lc:
	for i, vec in enumerate(randomVectors):
		if i >= r*b:
			break
		print("Computing dot products of randomVector #{} and userVectors".format(i))
		buckets = {'positive':[], 'negative':[]}
		for uid, user in userDict.items():
			lc.increment() #count number of userVectors * randomVectors
			sign = ('positive', 'negative')[dot(user, vec, mids) < 0] #gets sign of dot product
			buckets.get(sign).append(uid)
		for bucket in buckets.values():
			assert i//r < b, "band index i//r wrong"
			assert i%r < r, "row index i\%r wrong"
			bands[i//r][i%r] += list(choose(bucket, 2)) #put pairs into rows. (a,b) and (b,a) are treated the same


# Find candidate pairs
with LogCounter() as lc:
	#map each row to a set, reduce each band using &, reduce bands using |
	AND = lambda s, t: s & t
	OR = lambda s, t: s | t
	candidates = reduce(OR, map(lambda band: reduce(AND, map(set, band)), bands))
	print("length of candidate weekends", len(candidates), len(candidates)/(671*670/2))


# Calculate distances of candidate pairs
result = []
candidateCosds = []
resultCosds = []
keys = userDict.keys()
with LogCounter(base=16) as lc:
	for (i, j) in candidates:
		lc.increment()
		assert i in keys
		assert j in keys
		d = cosd(userDict.get(i), userDict.get(j))
		candidateCosds.append(d)
		if d < 1.15:
			result.append((i,j))
			resultCosds.append(d)


plt.subplot()
plt.hist(candidateCosds, 'auto')
plt.subplot()
plt.hist(resultCosds, 'auto')
plt.show()
