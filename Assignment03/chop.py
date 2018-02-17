import codecs

OUTPUT_LINES = 100

with codecs.open("data_v1.txt", "r", "utf-8") as infile:
	with codecs.open("data_out_{}.txt".format(OUTPUT_LINES), "w", "utf-8") as outfile:
		for i, line in enumerate(infile):
			if i > OUTPUT_LINES:
				break
			outfile.write(line)