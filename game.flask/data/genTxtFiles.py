#!/usr/bin/python

import os, sys

if len(sys.argv) != 3:
	print 'Usage: ./genTxtFiles.py [org-image-path] [deg-image-path]'
	sys.exit()

orgImagePath = sys.argv[1]
degImagePath = sys.argv[2]

if not os.path.exists(orgImagePath):
	print 'Path[' + orgImagePath + '] doesn\'t exist'
	sys.exit()
if not os.path.exists(degImagePath):
	print 'Path[' + degImagePath + '] doesn\'t exist'
	sys.exit()

imagelistTxt = open('imagelist.txt', 'w')
questionsCsv = open('questions.csv.template', 'w')
for oi in os.popen('ls ' + orgImagePath):
	prefix = oi.strip('\n').split('.')[0]
	imagelistTxt.write(prefix + '\n')
	questionsCsv.write(prefix + ',,,' + '\n')
imagelistTxt.close()

degimagelistTxt = open('degimagelist.txt', 'w')
for oi in os.popen('ls ' + degImagePath):
	prefix = oi.strip('\n').split('.png')[0]
	degimagelistTxt.write(prefix + '\n')
degimagelistTxt.close()
