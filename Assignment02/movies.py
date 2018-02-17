#!/usr/bin/python
# -*- coding: utf-8 -*- 

# Khaled Al Hosani (kah579), Myunggun Seo (ms9144)
from pyspark import SparkConf, SparkContext
import sys
import string
import re

def getMovies(line):
	'''returns (mid, (title, [genre1, genre2, ...]))'''
	line = line.strip()
	i = line.find(',')
	mid, line = line[:i], line[i+1:]
	i = line.rfind(',')
	title, genres = line[:i], line[i+1:]
	title = title.strip('"')
	genres = genres.split('|')
	return (mid, (title, genres))

def getRatings(line):
	'''returns (uid, (mid, float(rating)))'''
	uid, mid, rating, time = line.strip().split(',')
	return (uid, (mid, float(rating)))

# Problem 3-1
def avgNumberofRaters(sc, ratingsFile):
	'''The average number of users a movie is rated by'''
	print("\n=== Problem 3-1: The average number of users a movie is rated by ===")
	ratings = sc.textFile(ratingsFile).map(getRatings) # (uid, (mid, float(rating)))
	ratingsFiltered = ratings.map(lambda x: (x[1][0], x[1][1])) #get (MID,r)

	# map: (MID, rating) -> (MID, 1), reduce: (MID, [1,1,1..]) -> (MID, 1)
	movieCount = ratingsFiltered.map(lambda x: (x[0], 1)).reduceByKey(lambda x,y: x).count()

	# map: (MID, rating) -> (1, 1), reduce: (1, [1,1,1,1...]) -> (1, n)
	ratingCount = ratingsFiltered.map(lambda x: (1, 1)).reduceByKey(lambda x,y: x+y).collect()[0][1]

	print("Average number of users a movie is rated by: {}".format(ratingCount/float(movieCount)))

# Problem 3-2
def avgRatingGenre(sc, moviesFile, ratingsFile):
	'''Average of ratings of movies in each genre. 
	We find the (average) rating of each movie and calculate the average of those ratings for each genre'''

	print("\n=== Problem 3-2: For each genre, the average rating of all movies in that genre ===")
	# list of movies and their genres - one entry per (movie, genre) pair
	movies = sc.textFile(moviesFile).map(getMovies) # (mid, (title, [genres]))
	movieGenreList = movies.map(lambda pair: (pair[0], pair[1][1])) # (mid, [genres])
	movieGenre = movieGenreList.flatMapValues(lambda x: x) # (mid, genre)

	# list of movies and average ratings of each movie
	ratings = sc.textFile(ratingsFile).map(getRatings) # (uid, (mid, float(rating)))
	ratings = ratings.map(lambda pair: (pair[1][0], (pair[1][1], 1) )) # (mid, (rating, 1))
	ratingsum = ratings.reduceByKey(lambda x, y: (x[0]+y[0], x[1]+y[1]) ) # (mid, (ratingsum, numRatings))
	avgrating = ratingsum.mapValues(lambda x: x[0]/x[1]) # (mid, avgRating) average rating of each movie

	# joined list of genre and average rating for each movie
	movieGenreRating = movieGenre.join(avgrating) # join (mid, (genre, rating))
	movieGenreRating = movieGenreRating.map(lambda x: (x[1][0], (x[1][1], 1))) #  (genre, (rating, 1))
	movieGenreRatingSum = movieGenreRating.reduceByKey(lambda x, y: (x[0]+y[0], x[1]+y[1]) ) # (genre, (ratingsum, numMovies))
	genreAvgRating = movieGenreRatingSum.mapValues(lambda x: x[0]/x[1]) # (genre, genreAvgRating)

	# sort and print result to console
	for (genre, avg) in sorted(genreAvgRating.collect(), key=lambda x: -x[1]):
		print("{} genre: {} rating on average".format(genre, avg))

# Problem 3-3
def topThree(sc, moviesFile, ratingsFile):
	'''The names of the top three movies (by average user rating) in each genre'''

	print("\n=== Problem 3-3: The names of the top three movies (by average user rating) in each genre ===")
	#get (MID, [genres])
	moviesParsed = sc.textFile(moviesFile).map(getMovies) #(mid, (title, [genre1, genre2, ...]))
	moviesFiltered = moviesParsed.map(lambda x: (x[0], x[1][1])) # (MID, [genres])

	#get (MID,r)
	ratingsParsed = sc.textFile(ratingsFile)
	ratingsFiltered = ratingsParsed.map(getRatings).map(lambda x: (x[1][0], x[1][1])) # (MID, rating)

	#seperate genres i.e. (MID,([g])  -> (MID, g1),(MID,g2), ... etc
	moviesSeperated = moviesFiltered.flatMapValues(lambda x: x)

	#Join on MID,  (MID, g1) & (MID, r) -> (MID, (g1, r) )
	joinedSet= moviesSeperated.join(ratingsFiltered)

	#Flip form (MID, (g, r) )  -> ( (MID, g) ,r)
	flippedSet=joinedSet.map(lambda pair: ((pair[0],pair[1][0]),pair[1][1]))

	#Map/Reduce to find average score for each movie
	mapped= flippedSet.mapValues(lambda x: (float(x), 1))
	reduced=mapped.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
	averaged=reduced.mapValues(lambda x:x[0]/x[1] )

	#Extract top 3 per genre
	genresList=[]
	result=[]
	average=[]
	genres = averaged.map(lambda x : x[0][1]).distinct().collect()

	for g in genres:
		genresList.append(g)
		top = averaged.filter(lambda x : x[0][1] == g).top(3, key=lambda x: x[1])
		for m in top:
			result.append(m[0][0])
			average.append(m[1])

	#get (MID, title)
	moviesTitle = moviesParsed.map(lambda x: (x[0], x[1][0])).sortByKey()

	#Print result
	for i, g in enumerate(genresList):
		print("{}: Top 3 Movies".format(g))
		print("1. {} ({})".format(moviesTitle.lookup(result[i*3])[0].encode('utf-8'),average[i*3]))
		print("2. {} ({})".format(moviesTitle.lookup(result[i*3+1])[0].encode('utf-8'),average[i*3+1]))
		print("3. {} ({})".format(moviesTitle.lookup(result[i*3+2])[0].encode('utf-8'),average[i*3+2]))

# Problem 3-4
def topWatchers(sc, moviesFile, ratingsFile):
	'''Top ten movie watchers ranked by the number of movies they have rated'''
	print("\n=== Problem 3-4: Top ten movie watchers ranked by the number of movies they have rated ===")
	ratings = sc.textFile(ratingsFile).map(getRatings) # (UID, (MID, float(rating)))
	ratingsFiltered = ratings.map(lambda x: (x[0], 1)) # (UID, 1)
	ratings = ratingsFiltered.reduceByKey(lambda x, y: x+y) # (UID, numMovies) number of movies rated by each user
	for (uid, numMovies) in ratings.sortBy(lambda x: -x[1]).take(10): # sort and take top 10
		print("User {} watched {} movies".format(uid, numMovies))

# Problem 3-5
def topPairs(sc, moviesFile, ratingsFile):
	print("\n=== Problem 3-5: Top ten pairs of users ranked by the number of movies both of them has watched ===")
	
	# Find numUsers, which will be the range of i and j. 
	lines = sc.textFile(ratingsFile).map(getRatings) # (UID, (MID, float(rating)))
	ratings = lines.map(lambda x: (int(x[0]), 1)).reduceByKey(lambda x, y: x) # (UID, 1)
	numUsers = ratings.map(lambda x: (1, 1)).reduceByKey(lambda x, y: x+y).collect()[0][1] # [(1, numUsers)] == 671

	# change key to (i,j) pair where i and j are user ids
	moviesGrouped = lines.map(lambda x: (int(x[0]), x[1][0])).groupByKey() # (uid, [M])

	# map((uid, [M_i]), [671])  ->  flatMapValues((uid, [M]_i), j)  -> map((i,j), [M_i])
	tuplePair = moviesGrouped.map(lambda x: (x, list(range(1, numUsers+1)))).flatMapValues(lambda x: x).map(lambda x: ((x[0][0], x[1]), x[0][1]))

	tuplePair = tuplePair.filter(lambda x: x[0][0] != x[0][1]) # filter((i,j (i!=j)), [M_i]) filter entries where i=i
	flipped = tuplePair.map(lambda x: ((x[0][1], x[0][0]), x[1]) if x[0][0] > x[0][1] else x) # flip if i<j. ((i,j), [M_i]) 

	# the reduce step will compare the lists of movies that each user rated
	reduced = flipped.reduceByKey(lambda x, y: len(set(x) & set(y)) ) # ((i,j), len([M_i^M_j])) calculate the size of intersection

	for users, numCommon in reduced.sortBy(lambda x: x[1], ascending=False).take(10): # sort and take top 10
		print("Users {} and {} have watched {} movies in common".format(users[0], users[1], numCommon))



if __name__ == "__main__":
	cf = SparkConf().setAppName("Movies")
	sc = SparkContext(conf=cf)
	moviesFile = "movies.csv" #mid, title, genres
	ratingsFile = "ratings.csv" #uid, mid, rating, time
	print('setup complete...')
	avgNumberofRaters(sc,ratingsFile) # Problem 3-1
	avgRatingGenre(sc, moviesFile, ratingsFile) # Problem 3-2
	topThree(sc, moviesFile, ratingsFile) # Problem 3-3
	topWatchers(sc, moviesFile, ratingsFile) # Problem 3-4
	topPairs(sc, moviesFile, ratingsFile) # Problem 3-5


