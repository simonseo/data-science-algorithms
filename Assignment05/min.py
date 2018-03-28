#!/usr/bin/python
# -*- coding: utf-8 -*- 
# @File Name: min.py
# @Created:   2018-02-28 01:33:49  Simon Myunggun Seo (simon.seo@nyu.edu) 
# @Updated:   2018-03-05 14:33:50  Simon Seo (simon.seo@nyu.edu)
import matplotlib.pyplot as plt
import random

l = []
K = 100
n = 1000
EXk = []

for k in range(1,K+1):
	minl = []
	for i in range(n):
		l = []
		for j in range(k):
			l.append(random.random())
		xi = min(l)
		minl.append(xi)
	Exi = sum(minl)/len(minl)
	EXk.append(Exi)


plt.subplot()

plt.plot(range(1,K+1), EXk) # E(Xk) for k in 1..100

X = list(range(1,K+1))
Y = list(map(lambda x:1/(x+1), X))
plt.plot(X,Y) # 1/(1+k) for k in 1..100

plt.show()


