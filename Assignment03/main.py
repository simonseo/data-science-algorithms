# This script does:
# 1. shingles documents and save their minhashes
# 2. put documents into buckets and find candidate pairs based on banding technique
# 3. compute Jaccard Similarity for candidate pairs and output result
# Khaled Alhosani (kah579) Myunggun Seo (ms9144)
from functions import getWords, kShingleWord, kShingle, jaccardSim, minhash, C
import codecs
from datetime import datetime
import math

# Caculate minhashes and save in file
# takes about 5.6 ms for running minhash with 16 hashes (all derived from 1 SHA-512 function call) on each document.
# expected to take about 1.5 hrs for 10^6 documents
k = 5
HASH_FILE_NAME = "minhash_data_v1.txt"

startingTime = datetime.now()
print("Started at {}".format(startingTime))

with codecs.open("data_v1.txt", "r", "utf-8") as infile:
    lst = map(lambda line: kShingleWord(k, line, False), infile.read().splitlines()) # samples

print("Finished shingling data at {}".format(datetime.now()))

count = 0
logcount = 0
with codecs.open(HASH_FILE_NAME, "w", "utf-8") as outfile:
    for (idx, shingles) in lst:
        outfile.write("{} {}\n".format(idx, ' '.join(minhash(shingles))))
        count+=1
        if math.log10(count) == logcount:
            print(count, datetime.now()-startingTime)
            logcount += 1

print("Finished minhashing data at {}".format(datetime.now()-startingTime))
#27 minutes for 10^6 documents for 5-word-shingles


# Put documents into buckets
# create 16 dictionaries, one for each hash.
# for each hashed document, put the index of the document into the 16 dictionaries with the hash as the key. like so:
startingTime = datetime.now()
print(startingTime)
with codecs.open(HASH_FILE_NAME, "r") as infile:
    lst = map(getWords, infile.read().splitlines())

h = 16 # number of hash functions
buckets = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
print(buckets)
for (j, words) in enumerate(lst):
    idx = int(words[0]) #idx of doc
    hashes = words[1:] #16 hashes
    for (i, hashVal) in enumerate(hashes): # put each hash into their respective buckets
        bucket = buckets[i].get(hashVal, []) #the usual way
        bucket.append(idx)
        buckets[i][hashVal] = bucket

print("length of buckets",len(buckets))
print(datetime.now() - startingTime)
print(list(buckets[1].items())[:30])



# divide into b=8 bands, r=2 rows
# for each band, find all combinations of documents that are put in same buckets in all rows
b=8
r=2
candidates = set([])
keylessBuckets = list(map(lambda row: set(map(tuple, row.values())), buckets)) #list of set of tuples

startingTime = datetime.now()
print(startingTime)

for i in range(0,b*r,r):
    print(i, i+r)
    band = keylessBuckets[i:i+r]

    listOfRowCandidates = []
    for row in band: # row is [['1'], ['1', '18566'], ['1'], ['1'], ['1']..] set of tuples
        rowCandidates = set([]) # all pairs from a row
        for bucket in row: # bucket is ['2', '126908', '203926', '278946', '746802'] tuples
            rowCandidates |= C(bucket, 2)
        listOfRowCandidates.append(rowCandidates)
        print("Finished row", len(rowCandidates))
    intersection = listOfRowCandidates[0] # intersections of rows in same band. pair becomes candidate if exists in all rows of a band
    for rowCandidates in listOfRowCandidates:
        intersection &= rowCandidates
    candidates |= intersection
    print("length of intersections within band", len(intersection))
    print("length of candidate weekends", len(candidates))

print(datetime.now()-startingTime)

# find documents that are in candidates
docsInCandidates = set([])
for (i,j) in candidates:
    docsInCandidates |= set([i,j])

startingTime = datetime.now()
print(startingTime)
with codecs.open("data_v1.txt", "r", "utf-8") as infile:
    lst = [kShingle(k, line) if int(line.split(' ',1)[0]) in docsInCandidates else [''] for line in infile.read().splitlines() ] # samples

print("done processing...", datetime.now()-startingTime)


# for each candidate pair in the list, 
# calculate the actual Jaccard Similarity and if JS > 0.75, 
# add to output list
k = 5

startingTime = datetime.now()
print(startingTime)
    
output = []
count = 0
logcount = 0
for (i,j) in candidates:
    js = jaccardSim(lst[i-1], lst[j-1])
    if (js > 0.75):
        output.append((i,j))
        count+=1
        if math.log10(count) == logcount:
            print(count, js, (i,j), (lst[i-1], lst[j-1]))
            logcount += 1
print(len(output))

print(datetime.now() - startingTime)


for i,j in output:
    print(i,j,jaccardSim(lst[i-1],lst[j-1]))