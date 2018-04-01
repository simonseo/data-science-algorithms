import math
import matplotlib.pyplot as plt

bits=[]
klist= list(range(10,1000))
for k in klist:
	k=float(k)
	top=-k*(10**6)
	bottom=math.log(1-(10**(-6/k)))
	bits.append(top/bottom)




for bit in bits:
	print(bit)

minbits=min(bits)
mink=klist[bits.index(minbits)]

plt.subplot()
plt.plot(klist,bits)
plt.title("Number of hash functions and bits required for $m=10^6$ and $p=10^{-6}$")
plt.xlabel('number of hash functions')
plt.ylabel('number of bits')
plt.axvline(x=mink,color='r')
plt.text(mink,minbits+10000,str(minbits))
plt.show()
