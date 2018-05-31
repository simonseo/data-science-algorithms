from pyspark import SparkConf, SparkContext
import sys
import string

def count(sc,filename):
   lines = sc.textFile(filename)
   words = lines.flatMap(getWords).map(lambda x: (x,1))
   print("No. of partitions in words RDD= {}.\n".format(words.getNumPartitions()))
   wordcount = words.reduceByKey(lambda x,y: x+y)
   countword = wordcount.map(lambda pair: (pair[1], pair[0]))
   top = countword.sortByKey(False).take(100)
   for (count,word) in top:
      print(word, count)

def getWords(line):
   words = line.strip().lower().split()
   return list( map(lambda w: w.strip(string.punctuation), words) )

if __name__ == "__main__":
   cf = SparkConf().setAppName("Word Count")
   sc   = SparkContext(conf=cf)
   filename = sys.argv[1]
   count(sc, filename)

