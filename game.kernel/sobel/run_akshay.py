#!/usr/bin/python

import os, sys
import subprocess

basedir = os.environ['GAME_SOBEL']

for filename in os.popen('ls images | grep .png').readlines():

	print
	print 'Working on ' + filename
	print 

	filename = filename.strip('\n')
	name = filename.split('.png')[0]
	rgbfilename = filename.split('.png')[0] + '.rgb'
	
	os.system(basedir + '/png2rgb.py png2rgb ' + basedir + '/images/' + filename + ' ' + basedir + '/images/' + rgbfilename)
	
	print "png2rgb.py done ... (png2rgb)"

	#subprocess.call("mkdir rgboutput", shell = True)
	#print "mkdir rgboutput done"
	subprocess.call("mkdir rgboutput/" + name, shell = True)
	print "mkdir rgboutput/name done"
	subprocess.call("mkdir rgboutput/" + name + "/nrmse", shell = True)
	print "mkdir rgboutput/name/nrmse done"
	
	#subprocess.call("mkdir rgboutput/" + name, shell = True)
	#subprocess.call("mkdir rgboutput/" + name + "/nrmse", shell = True)
	#os.system('mkdir ' + basedir + '/rgboutput/' + name)
	#os.system('mkdir ' + basedir + '/rgboutput/' + name + '/nrmse')
	#os.system('mkdir ' + basedir + '/rgboutput/' + name + '/psnr')
	
	print 
	print "Doing Sobel"
	#print 'java -cp ' + basedir + '/sobel.jar Sobel.RgbImage ' + basedir + '/images/' + rgbfilename + ' ' + basedir + '/rgboutput/' + name + ' nrmse'
	os.system('java -cp ' + basedir + '/sobel.jar Sobel.RgbImage ' + basedir + '/images/' + rgbfilename + ' ' + basedir + '/rgboutput/' + name + ' nrmse')
	print "Sobel done ... (nrmse)"
	
	#os.system('java -cp ' + basedir + '/sobel.jar Sobel.RgbImage ' + basedir + '/images/' + rgbfilename + ' ' + basedir + '/rgboutput/' + name + ' psnr')
	#print "Sobel done ... (psnr)"
	
	#subprocess.call("mkdir pngoutput", shell = True)
	#print "mkdir pngoutput done"
	subprocess.call("mkdir pngoutput/" + name, shell = True)
	print "mkdir pngoutput/name done"
	subprocess.call("mkdir pngoutput/" + name + "/nrmse", shell = True)
	print "mkdir pngoutput/name/nrmse done"
	
	#os.system('mkdir ' + basedir + '/pngoutput/' + name)
	#os.system('mkdir ' + basedir + '/pngoutput/' + name + '/nrmse')
	#os.system('mkdir ' + basedir + '/pngoutput/' + name + '/psnr')
	
	print 
	print "Doing png to rgb conversion"
	#print basedir + '/png2rgbAll.py rgb2png ' + basedir + '/rgboutput/' + name + '/nrmse ' + basedir + '/pngoutput/' + name + '/nrmse'
	os.system(basedir + '/png2rgbAll.py rgb2png ' + basedir + '/rgboutput/' + name + '/nrmse ' + basedir + '/pngoutput/' + name + '/nrmse')
	print "png2rgbAll.py done ... (rgb2png)"
	
	#os.system(basedir + '/png2rgbAll.py rgb2png ' + basedir + '/rgboutput/' + name + '/psnr ' + basedir + '/pngoutput/' + name + '/psnr')
	#print "png2rgbAll.py done ... (rgb2png)"
	
	os.system('rm -rf ' + basedir + '/rgboutput/' + name)
	os.system('rm ' + basedir + '/images/' + rgbfilename)
