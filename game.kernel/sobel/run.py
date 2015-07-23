#!/usr/bin/python

import os, sys

basedir = os.environ['GAME_SOBEL']

for filename in os.popen('ls images | grep png').readlines():

	print
	print 'Working on ' + filename
	print 

	filename = filename.strip('\n')
	name = filename.split('.png')[0]
	rgbfilename = filename.split('.png')[0] + '.rgb'
	
	os.system(basedir + '/png2rgb.py png2rgb ' + basedir + '/images/' + filename + ' ' + basedir + '/images/' + rgbfilename)
	
	print "png2rgb.py done ... (png2rgb)"

	os.system('rm -rf ' + basedir + '/rgboutput/' + name + ' ; mkdir ' + basedir + '/rgboutput/' + name)
	os.system('rm -rf ' + basedir + '/rgboutput/' + name + '/nrmse ; mkdir ' + basedir + '/rgboutput/' + name + '/nrmse')
	#os.system('mkdir ' + basedir + '/rgboutput/' + name + '/psnr')
	
	os.system('java -cp ' + basedir + '/sobel.jar Sobel.RgbImage ' + basedir + '/images/' + rgbfilename + ' ' + basedir + '/rgboutput/' + name + ' nrmse')
	print "sobel done ... (nrmse)"
	
	#os.system('java -cp ' + basedir + '/sobel.jar Sobel.RgbImage ' + basedir + '/images/' + rgbfilename + ' ' + basedir + '/rgboutput/' + name + ' psnr')
	#print "Sobel done ... (psnr)"
	
	os.system('rm -rf ' + basedir + '/pngoutput/' + name + ' ; mkdir ' + basedir + '/pngoutput/' + name)
	os.system('rm -rf ' + basedir + '/pngoutput/' + name + '/nrmse ; mkdir ' + basedir + '/pngoutput/' + name + '/nrmse')
	#os.system('mkdir ' + basedir + '/pngoutput/' + name + '/psnr')
	
	os.system(basedir + '/png2rgbAll.py rgb2png ' + basedir + '/rgboutput/' + name + '/nrmse ' + basedir + '/pngoutput/' + name + '/nrmse')
	print "png2rgbAll.py done ... (rgb2png)"
	
	#os.system(basedir + '/png2rgbAll.py rgb2png ' + basedir + '/rgboutput/' + name + '/psnr ' + basedir + '/pngoutput/' + name + '/psnr')
	#print "png2rgbAll.py done ... (rgb2png)"
	
	os.system('rm -rf ' + basedir + '/rgboutput/' + name)
	os.system('rm ' + basedir + '/images/' + rgbfilename)
