# Khaled Al Hosani (kah579), Myunggun Seo (ms9144)
import matplotlib.pyplot as plt
import numpy as np
import random
import math
import sys

vectors=[]
n=10000000

print("Generating Vectors...")
for i in range(n):
	a=random.uniform(-1,1)
	b=random.uniform(-1,1)
	vectors.append(math.atan2(b,a))
print("Done")

plt.subplot()
plt.hist(vectors,1000)
plt.xlabel("Angle")
plt.ylabel("Frequency")

plt.axvline(x=np.pi,color='r')
plt.text(np.pi,1000,r'$\pi$')

plt.axvline(x=np.pi/2,color='r')
plt.text(np.pi/2,1000,r'$\pi/2$')

plt.axvline(x=0,color='r')

plt.axvline(x=-np.pi/2,color='r')
plt.text(-np.pi/2,1000,r'$-\pi/2$')

plt.axvline(x=-np.pi,color='r')
plt.text(-np.pi,1000,r'$-\pi$')

plt.show()