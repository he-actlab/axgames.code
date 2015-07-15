#!/usr/bin/python

import os, sys

if len(sys.argv) < 4:
	print 'USAGE: ./copyfiles.py [orgdir] [degdir] [dstdir]'
	sys.exit()

orgdir = sys.argv[1]
degdir = sys.argv[2]
dstdir = sys.argv[3]

if os.path.exists(dstdir + '/orgimage'):
	os.system('rm -rf ' + dstdir + '/orgimage; mkdir ' + dstdir + '/orgimage')
if os.path.exists(dstdir + '/degimage'):
	os.system('rm -rf ' + dstdir + '/degimage; mkdir ' + dstdir + '/degimage')
if os.path.exists(dstdir + '/sobelimage'):
	os.system('rm -rf ' + dstdir + '/sobelimage; mkdir ' + dstdir + '/sobelimage')

for line in  os.popen('ls ' + orgdir + ' | grep -v images*').readlines():
	pngfilename = line.strip('\n')
	filename = pngfilename = line.split('.')[0]
	print filename

	if not (filename in os.popen('ls ' + degdir + ' | grep ' + filename).read()):
		print 'No degraded image file in: ' + degdir + '/' + filename
		sys.exit()

	os.system('cp ' + orgdir + '/' + filename + '.png ' + dstdir + '/orgimage') 
	os.system('cp ' + degdir + '/' + filename + '/nrmse/' + filename + '_* ' +  dstdir + '/degimage') 
	os.system('cp ' + degdir + '/' + filename + '/nrmse/' + filename + '-sobel* ' +  dstdir + '/sobelimage') 
	
