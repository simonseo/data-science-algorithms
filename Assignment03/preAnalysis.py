# This script does: 
# 1. creates smaller samples of the original file
# 2. finds ideal values of r,b,t
# 3. plots histograms and functions
# Khaled Alhosani (kah579) Myunggun Seo (ms9144)

import numpy as np
import matplotlib.pyplot as plt
import random
import codecs
from datetime import datetime
from hashlib import sha512
import itertools
import math

ORIGINAL_DATA = "data_v1.txt"
#chop.py: simply chops the first however many lines
OUTPUT_LINES = 1000

with codecs.open(ORIGINAL_DATA, "r", "utf-8") as infile:
	with codecs.open("data_out_{}.txt".format(OUTPUT_LINES), "w", "utf-8") as outfile:
		for i, line in enumerate(infile):
			if i > OUTPUT_LINES:
				break
			outfile.write(line)

# randomsample.py
# Randomly samples however many lines needed 
TOTAL_LINES = 10**6 + 2
OUTPUT_LINES = 100000
p = OUTPUT_LINES/TOTAL_LINES

print("getting random sample of size {}".format(OUTPUT_LINES))
with codecs.open(ORIGINAL_DATA, "r", "utf-8") as infile:
	with codecs.open("data_random_{}.txt".format(OUTPUT_LINES), "w", "utf-8") as outfile:
		output_count = 0
		for i, line in enumerate(infile):
			if output_count < OUTPUT_LINES and random.random() < p:
				outfile.write(line)
				output_count += 1
			if output_count >= OUTPUT_LINES:
				break
print("done")

##################
# findbr.py
# Finds (b,r) parameters required for documents of 
# JS similarity s to be in candidate groups with probability p
p = 0.98
q = 1 - p
s = 0.75
rrange = range(2, 20)
brange = range(0, 250, 5)

res = []

for b in brange:
	b = 10**(-b/100)
	for r in rrange:
		if (1 - s**r < q**b):
			res.append((int(1/b),r))
l = len(res)
print(l)
if l < 250:
	print(res)

# findthreshold.py
# for given (b,r) parameters, finds at which point s in [0,1] the slope is maximum.
# also finds probability of document pairs that have JS=S is in candidate pairs

srange = range(0,1000)
# ordered b first, r second
br = [(32,4), (16,8), (32,8), (8,4), (4,4), (8,2), (12,8), (8,12), (4,2)]

fx = lambda s,b,r: 1-(1-s**r)**b
tx = lambda b,r: (1/b)**(1/r)
S = 0.75

for (b,r) in br:
	max_slope_threshold = (0, -1) # (s, f'(s))
	for s in srange:
		s = s/1000
		fpx = r*b*(1-s**r)**(b-1)*s**(r-1)
		if fpx > max_slope_threshold[1]:
			# print(max_slope_threshold)
			max_slope_threshold = (s, fpx)
	print("b {} r {} threshold {} p({}) {}".format(b, r, max_slope_threshold[0], S, fx(S, b, r)))

# Finding optimal values of r and b for target JS = 0.75
# these are ordered r first, b second
l = [(4,32),(8,16),(8,32),(4,8),(4,4),(2,8)]

fig = plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
for i, (r, b) in enumerate(l):
	X = np.arange(0, 1, 0.01)
	Y = list(map(lambda x: 1-(1-x**r)**b, X))
	plt.subplot(2,3,1+i)
	plt.plot(X, Y)
	plt.title('$f(x) = 1−(1−x^{{{}}})^{{{}}}$'.format(r, b))
	plt.xlabel('x')
	plt.ylabel('f(x)')
	x = 0.75
	X = r
	Y = b
	print(X*Y*((1-x**X)**(Y-1))*(x**(X-1)))
plt.tight_layout()
plt.show()