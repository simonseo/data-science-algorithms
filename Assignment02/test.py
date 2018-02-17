#!/usr/bin/python
# -*- coding: utf-8 -*- 
# @File Name: test.py
# @Created:   2018-02-06 21:51:50  seo (simon.seo@nyu.edu) 
# @Updated:   2018-02-06 22:23:24  Simon Seo (simon.seo@nyu.edu)

from pyspark import SparkConf, SparkContext
import sys
import string
import re
import csv


def count(sc,filename):
	lines = sc.textFile(filename)
	bigrams = lines.flatMap(getBigrams).map(lambda x: (x,1))
	print("No. of partitions in bigrams RDD= {}.\n".format(bigrams.getNumPartitions()))
	bigramcount = bigrams.reduceByKey(lambda x,y: x+y)
	countbigram = bigramcount.map(lambda pair: (pair[1], pair[0]))
	top = countbigram.sortByKey(False).take(100)
	for (count,bigram) in top:
		print(bigram, count)

def getBigrams(line):
	bigrams = []
	# Split line into sentences that end with question mark or full stop
	sentences = re.split('\.|\?', line.strip().lower())
	for s in sentences:
		# split sentence into words with whitespace as delimiter. for each word, strip punctuations
		words = list( map(lambda w: w.strip(string.punctuation), s.split()) )
		# for each word make a bigram
		bigrams += [(words[i], words[i+1]) for i in range(0,len(words)-1)]
	return bigrams

def getMovies(line):
	'''returns (mid, (title, [genre1, genre2, ...]))'''
	line = line.strip().lower()
	i = line.find(',')
	mid, line = line[:i], line[i+1:]
	i = line.rfind(',')
	title, genres = line[:i], line[i+1:]
	title = title.strip('"')
	genres = genres.split('|').sorted()
	return (mid, (title, genres))

def getRatings(line):
	'''returns (uid, (mid, float(rating)))'''
	uid, mid, rating, time = line.strip().split(',')
	return (uid, (mid, float(rating)))

# Problem 3-2
def avgRatingGenre(sc, moviesFile, ratingsFile):
	'''Average of ratings of movies in each genre'''
	lines = sc.textFile(moviesFile)
	movies = lines.flatMap(getMovies)

	lines = sc.textFile(ratingsFile)
	ratings = lines.flatMap(getRatings)

	moviespergenre = movies

	moviespergenre.join(ratings.map(lambda pair: (pair[1][0], pair[1][1])))

	# ratings = sc.textFile(ratingsFile)
	# parse movies
	pass


if __name__ == "__main__":
	cf = SparkConf().setAppName("Movies")
	sc = SparkContext(conf=cf)
	moviesFile = "movies.csv" #mid, title, genres
	ratingsFile = "ratings.csv" #uid, mid, rating, time
	avgRatingGenre(sc, moviesFile, ratingsFile) # Problem 3-2


