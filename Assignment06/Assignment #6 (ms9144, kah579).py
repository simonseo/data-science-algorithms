
# coding: utf-8

# ## 1.a Flajolet-Martin algorithm

# In[1]:

import string
def wordStream(filename):
    with open(filename, "r") as infile:
        for line in infile:
            for w in line.strip().lower().split():
                z = 0
                for c in w.strip(string.punctuation):
                    z = (z<<8) | ord(c)
                yield z


# In[2]:

def countDistinct(stream):
    M = {}
    for x in stream:
        M[x] = 1
    return len(M.keys())


# In[3]:

import random
def FM_estimates(stream, r):
    # r is the number of estimates needed
    def trailing(s):
        return len(s) - len(s.rstrip('0'))

    p = 9576890767
    a = [random.randint(1,p) for i in range(r)]
    b = [random.randint(0,p) for i in range(r)]
    z = [0 for i in range(r)]
    for x in stream:
        for i in range(r):
            y = (a[i] * (x%p) + b[i]) %p
            # update z[i] if y has more than z[i] trailing 0's
            t = trailing(bin(y))
            if t > z[i]:
                z[i] = t
    return z


# In[4]:

l = 100
z = FM_estimates(wordStream("big.txt"), l)


# In[5]:

from statistics import median
l = 100
mean = sum([2**zi for zi in z]) / l
median = median([2**zi for zi in z])
harmonic_mean = l/(sum([2**(-zi) for zi in z]))


print("mean {}  median {}  harmonic mean {}".format(mean, median, harmonic_mean))

# Which one is best?


# ## 1.b Stochastic Averaging

# In[6]:

import string
def getWords(line):
   words = line.strip().lower().split()
   return list( map(lambda w: w.strip(string.punctuation), words) )

#k-shingle based on letters
def kShingle(k, line):
    words = getWords(line)
    line = ''.join(words)
    result = [''.join([line[i+j] for j in range(k)]) for i in range(len(line)-k+1)]
    return result


# In[7]:

import codecs
with codecs.open("big.txt", "r", "utf-8") as infile:
    lst = list(map(lambda line: kShingle(9, line), infile.read().splitlines()))

print(lst[0])


# In[8]:

import random
def h(x):
    p = 9576890767
    a = random.randint(1,p)
    b = random.randint(0,p)
    y = ((a * (x % p)  + b) % p)
    return y


# In[9]:

groups = [[] for i in range(64)]

for line in lst:
    for shingle in line:
        z = 0
        for c in shingle:
            z = (z<<8) | ord(c)
        y = h(z)

        groupId = (y & (((1 << 6) - 1) << 27)) >> 27 # y & 111,111,000...000
        fmHash = y & ((1 << 27) - 1) # y & 000,000,111...111
        
        groups[groupId].append(fmHash)
    
print([bin(fmHash) for fmHash in groups[0][:10]])
print([len(group) for group in groups])


# In[10]:

def trailing(s):
    return len(s) - len(s.rstrip('0'))

maxts = []
for group in groups:
    maxt = 0
    for fmHash in group:
        t = trailing(bin(fmHash))
        if t > maxt:
            maxt = t
    maxts.append(maxt)

K = len(maxts)
harmonic_mean = K**2/(sum([2**(-zi) for zi in maxts]))

print("HyperLogLog  harmonic mean {}".format(mean, median, harmonic_mean))


# ## 2.a Misra-Gries

# In[11]:

def numStream(filename):
    with open(filename, "r") as infile:
        for line in infile:
            for n in line.strip().split():
                yield int(n)


# In[12]:

class MisraGries():
    def __init__(self, k):
        self.counters = {}
        self.k = k
        self.m = 0
        
    def __call__(self, el):
        self.m += 1
        if el in self.counters.keys():
            self.counters[el] += 1
        elif len(self.counters.keys()) < self.k - 1:
            self.counters[el] = 1
        else:
            self.counters = {key : (val - 1) for key, val in self.counters.items() if val > 1}
    
    def getHigherThan(self, threshold):
        return [(key,val) for key, val in self.counters.items() if val >= threshold * self.m]


# In[13]:

import math

e = 0.06 / 10
k = 1/(2*e)
mg = MisraGries(math.ceil(2*k - 1))

for el in numStream("kosarak.dat"):
    mg(el)

print("The total number of page views:", mg.m)
print("The pages that were viewed by more than 10% of users are:", mg.getHigherThan(e))


# ## 2.b Count Min Sketch

# In[20]:

import random
class CountMinSketch():
    def __init__(self, numHash, numBucket, threshold):
        self.numHash = numHash
        self.numBucket = numBucket
        self.threshold = threshold # epsilon or 1/k
        self.p = 9576890767
        self.a = [random.randint(1,self.p) for i in range(numHash)]
        self.b = [random.randint(0,self.p) for i in range(numHash)]
        self.m = 0 # number of stream elements

        self.buckets = [[0 for j in range(numBucket)] for i in range(numHash)]
        self.minList = [] # list of (x, minCount) pairs sorted by minCount


    def h(self, x):
        # returns list of hashed values for given x
        return [((self.a[i] * (x%self.p) + self.b[i]) % self.p) % self.numBucket for i in range(self.numHash)]
        

    def __call__(self, x, debugm):
        # executed for every element in stream
        self.m += 1 
        if self.m < debugm: print("======================", self.m, "======================")
        h_list = self.h(x) # list of hashed values

        
        # find minCount
        minCount = 9999999999
        if self.m < debugm: print("buckets:", end=" ")
        for i, hashVal in enumerate(h_list):
            count = self.buckets[i][hashVal]
            if self.m < debugm: print(count, end=" ")
            if count <= minCount:
                minCount = count
        if self.m < debugm: print()
   
            
        # update buckets that have minCount
        for i, hashVal in enumerate(h_list):
            if self.buckets[i][hashVal] <= minCount:
                self.buckets[i][hashVal] += 1
        minCount += 1
        if self.m < debugm: print("element", x, "minCount", minCount) 
            

        # remove old (x, minCount) from minList
        keyList = [k for (k,v) in self.minList]
        if x in keyList:
            if self.m < debugm: print(x, "is being removed from minList")
            i = keyList.index(x)
            self.minList.pop(i)
            
        # Insert new (x, minCount)
        if minCount > self.m * self.threshold:
            if not self.minList: # if minList is empty
                self.minList.append((x, minCount))
                if self.m < debugm: print((x, minCount), "is being added to minList at 0")
            else: # if minList is not empty, find the right place and insert
                inserted = False
                for i, (k, v) in enumerate(self.minList):
                    if v > minCount:
                        self.minList.insert(i, (x, minCount))
                        inserted = True
                        if self.m < debugm: print((x, minCount), "is being added to minList at",i)
                        break
                if not inserted:
                    self.minList.append((x, minCount))
                    if self.m < debugm: print((x, minCount), "is being added to minList at the end")
        
        # update minlist
        for i, (k, v) in enumerate(self.minList):
            if v > self.m * self.threshold:
                if self.m < debugm: print("minList is being cut at", i, "m*threshold =", self.m*self.threshold)
                self.minList = self.minList[i:]
                break
        
        # debug print
        if self.m < debugm:
            print("buckets:", end=" ")
            for i, hashVal in enumerate(h_list):
                count = self.buckets[i][hashVal]
                print(count, end=" ")
        if self.m < debugm: print()
        if self.m < debugm: print(self.result())

        
    def result(self):
        return self.minList


            


# In[21]:

numHash = 6 # 2**(-l) 
numBucket = 400
threshold = 0.01 # total pv / total u < 10. {pgs s.t. pv > 0.1 * total u > 0.1 * total pv / 10}

cms = CountMinSketch(numHash, numBucket, threshold)
debugm = 0

for el in numStream("kosarak.dat"):
    cms(el, debugm)

print("The total number of page views:", cms.m)
print("The pages that were viewed by more than 10% of users are:", cms.result())

