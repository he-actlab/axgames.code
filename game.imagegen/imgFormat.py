#!/usr/bin/python

import os, sys

if len(sys.argv) != 3:
	print 'Usage: ./imgFormat.py [inDir-path] [outDir-path]'
	sys.exit()

inDir = sys.argv[1]
outDir = sys.argv[2]

if not os.path.exists(inDir):
	print 'Path[' + inDir + '] doesn\'t exist'
	sys.exit()

if os.path.exists(outDir):
	os.system('rm -rf ' + outDir)
os.system('mkdir ' + outDir)

nameMap = {}
os.system('mkdir temp')
for f in os.popen('ls ' + inDir):
	if '.jpg' in f:
		jpgFile = f.strip('\n')
		jpgPrefix  = jpgFile.split('.')[0]
		pngFile = jpgPrefix + '.png'
		os.system('convert ' + inDir + '/' + jpgFile + ' temp/' + jpgPrefix + '.png')
		print 'Converting [' + jpgFile +'] ==> [' + pngFile + ']'
	else:
		os.system('cp ' + inDir + '/' + f.strip('\n') + ' temp/' + f.strip('\n'))
		print 'Copying [' + f.strip('\n') +']'

for pngFile in os.popen('ls temp'):
	result = os.popen('sips -g pixelWidth -g pixelHeight temp/' + pngFile).readlines()
	width = int(result[1].strip('\n').split(':')[1])
	height = int(result[2].strip('\n').split(':')[1])

	key = str(width) + 'x' + str(height)
	if key in nameMap.keys():
		nameMap[key] += 1
	else:
		nameMap[key] = 0

	newPngFile = key + 'n' + str(nameMap[key]) + '.png'
	os.system('mv temp/' + pngFile.strip('\n') + ' ' + outDir + '/' + newPngFile)
	print 'Renaming [' + pngFile.strip('\n') + '] -> [' + newPngFile + ']'

os.system('rm -rf temp')