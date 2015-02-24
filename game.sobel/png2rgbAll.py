#!/usr/bin/python

import os, sys

command = sys.argv[1]
inDir = sys.argv[2]
outDir = sys.argv[3]

if len(sys.argv) != 4:
	print "Usage: ./png2rgbAll.py [png2rgb|rgb2png|png2gray] INPUT_DIR OUTPUT_DIR"
	sys.exit(0)

if os.path.isdir(inDir) != True:
	print "Error! Input directores does not exist!"
	sys.exit(0)
if os.path.isdir(outDir) != True:
	print "Error! Output directores does not exist!"
	sys.exit(0)

fileList = os.popen('ls ' + inDir).readlines()
for f in fileList:
	outFilename = f.strip('\n').split('.rgb')[0] + '.png'
	os.system('./png2rgb.py ' + command + ' ' + inDir + '/' + f.strip('\n') + ' ' + outDir + '/' + outFilename + ' > /dev/null')
