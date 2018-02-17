import codecs
import random

TOTAL_LINES = 10**6 + 2
OUTPUT_LINES = 1000
p = OUTPUT_LINES/TOTAL_LINES

print("getting random sample of size {}".format(OUTPUT_LINES))
with codecs.open("data_v1.txt", "r", "utf-8") as infile:
	with codecs.open("data_random_{}.txt".format(OUTPUT_LINES), "w", "utf-8") as outfile:
		output_count = 0
		for i, line in enumerate(infile):
			if output_count < OUTPUT_LINES and random.random() < p:
				outfile.write(line)
				output_count += 1
			if output_count >= OUTPUT_LINES:
				break
print("done")