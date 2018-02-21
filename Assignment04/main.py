#!/usr/bin/python
# -*- coding: utf-8 -*- 
# @File Name: main.py
# @Created:   2018-02-21 03:21:35  Simon Myunggun Seo (simon.seo@nyu.edu) 
# @Updated:   2018-02-21 04:27:53  Simon Seo (simon.seo@nyu.edu)
from functions import createUserDict, cosd, choose
import math

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


with open("randomVectors.csv", "r") as infile:
	getNums = lambda line: list(map(float, line.strip().split()))
	randomVectors = list(map(getNums, infile.read().splitlines()))
userDict, mids = createUserDict("ratings.csv")

r = 2
b = 8
bands = [[[] for j in range(r)] for i in range(b)]

candidates = []

for i, vec in enumerate(randomVectors):
	print("starting vectors {}".format(i))
	buckets = {'positive':[], 'negative':[]}
	count = logcount = 0
	for uid, user in userDict.items():
		count += 1
		if math.log10(count) == logcount:
			logcount += 1
			print(count)
		sign = 'positive' if dot(user, vec, mids) >= 0 else 'negative'
		buckets.get(sign).append(uid)
	for bucket in buckets.values():
		bands[i//r][i%r] += list(choose(bucket, 2))



