# Finds (b,r) parameters required for documents of 
# given JS similarity s to be in candidate groups with probability p
import math

p = 0.90
q = 1 - p
s = 0.75
brange = range(0, int(100 * math.log10(50)), 5)
rrange = range(0, 9)

res = []

for b in brange:
	b = 10**(b/100)
	b = 1/b
	for r in rrange:
		if (1 - s**r < q**b):
			res.append((int(1/b),r))
l = len(res)
print(l)
if l < 250:
	print(res)