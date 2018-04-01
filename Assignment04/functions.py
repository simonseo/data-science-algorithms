#!/usr/bin/python
# -*- coding: utf-8 -*- 
# @File Name: functions.py
# @Created:   2018-02-21 03:15:26  Simon Myunggun Seo (simon.seo@nyu.edu) 
# @Updated:   2018-04-02 00:24:50  Simon Seo (simon.seo@nyu.edu)
import string
import math
import itertools
from functools import reduce

def getWords(line, delimiter=','):
	words = line.strip().lower().split(delimiter)
	return list( map(lambda w: w.strip(string.punctuation), words) )

def createUserDict(filename="ratings.csv"):
	'''creates dict of K-V shape (uid, (mid, r)) and sorted list of all MIDs'''
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
	return userDict, sorted(midSet)


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

def choose(lst, r):
	#returns all "choose r" combinations as a set
	return set(map(lambda x: tuple(sorted(x)), itertools.combinations(lst, r)))

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