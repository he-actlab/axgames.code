#!/usr/bin/python

import os, sys

def main():
	if len(sys.argv) != 2:
		print "./merge_csv.py [bench.csv]"
		sys.exit()
	bench = sys.argv[1]
	lf = open(bench,"r")
	lines = lf.readlines()
	invk = []
	for i in range(0, 50):
		invk.append(0)
	for line in lines:
		tokens = line.strip('\n').split(',')
		invk[int(float(tokens[1])*100.0)-1] += int(tokens[2])
	lf.close()
	for i in range(1,51):
		print str(float(i)/100.0) + "," + str(invk[i-1])

if __name__ == '__main__':	
	main()
