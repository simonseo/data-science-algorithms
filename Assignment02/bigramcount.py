# Khaled Al Hosani (kah579), Myunggun Seo (ms9144)
from pyspark import SparkConf, SparkContext
import sys
import string
import re

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

if __name__ == "__main__":
	cf = SparkConf().setAppName("Bigram Count")
	sc = SparkContext(conf=cf)
	filename = sys.argv[1]
	count(sc, filename)

