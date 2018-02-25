#!/usr/bin/python
# -*- coding: utf-8 -*- 
# @File Name: main.py
# @Created:   2018-02-21 03:21:35  Simon Myunggun Seo (simon.seo@nyu.edu) 
# @Updated:   2018-02-25 20:59:41  Simon Seo (simon.seo@nyu.edu)
from functions import createUserDict, cosd, choose, dot
from LogCounter import LogCounter
import math
from functools import reduce
import matplotlib.pyplot as plt

# open randomVectors and userDict
userDict, mids = createUserDict("ratings.csv")
with open("randomVectors.csv", "r") as infile:
	getNums = lambda line: list(map(float, line.strip().split()))
	randomVectors = list(map(getNums, infile.read().splitlines()))

# for each randomVector, userVectors were divided into two buckets. 
# union of set of pairs from two buckets are put into a row
# 'bands' has b number of bands and each band has r number of rows
r = 2
b = 8
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
with LogCounter() as lc: #used for timing
	#map each row to a set, reduce rows in each band using &, reduce bands using |
	AND = lambda s, t: s & t
	OR = lambda s, t: s | t
	candidatePairs = reduce(OR, map(lambda band: reduce(AND, map(set, band)), bands))
	print("length of candidate weekends", len(candidatePairs), len(candidatePairs)/(671*670/2))


s = 0.75
# Calculate distances of candidate pairs
candidateijCosds = []
candidateCosds = []
resultijCosds = []
resultCosds = []
keys = userDict.keys()
with LogCounter(base=16) as lc:
	for (i, j) in candidatePairs:
		lc.increment()
		assert i in keys
		assert j in keys
		d = cosd(userDict.get(i), userDict.get(j))
		candidateijCosds.append(((i,j),d))
		candidateCosds.append(d)
		if d < (1-s)*math.pi:
			resultijCosds.append(((i,j),d))
			resultCosds.append(d)


plt.subplot()
plt.ylim(ymax=50)
binlist=[i/200 for i in range(312)]
plt.hist(candidateCosds, bins=binlist)
plt.hist(resultCosds, bins=binlist)
plt.show()


print("candidates:{} finalists:{} total possible pairs:{}".format(len(candidateCosds), len(resultCosds), len(ijcosds)))
for i, val in enumerate(sorted(ijcosds, key=lambda x:x[1])):
    if val[1] > (1-s)*math.pi:
        print("there shold actually be {} finalists".format(i))
        break
print(sorted(ijcosds, key=lambda x:x[1])[:i+10])