#!/usr/bin/python

import os, sys
from multiprocessing import Process

basedir = os.environ['GAME_MEAN']



def runMean(filename):
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
	
	os.system('java -cp ' + basedir + '/mean.jar Mean.RgbImage ' + basedir + '/images/' + rgbfilename + ' ' + basedir + '/rgboutput/' + name + ' nrmse')
	print "mean done ... (nrmse)"
	
	#os.system('java -cp ' + basedir + '/mean.jar Mean.RgbImage ' + basedir + '/images/' + rgbfilename + ' ' + basedir + '/rgboutput/' + name + ' psnr')
	#print "Mean done ... (psnr)"
	
	os.system('rm -rf ' + basedir + '/pngoutput/' + name + ' ; mkdir ' + basedir + '/pngoutput/' + name)
	os.system('rm -rf ' + basedir + '/pngoutput/' + name + '/nrmse ; mkdir ' + basedir + '/pngoutput/' + name + '/nrmse')
	#os.system('mkdir ' + basedir + '/pngoutput/' + name + '/psnr')
	
	os.system(basedir + '/png2rgbAll.py rgb2png ' + basedir + '/rgboutput/' + name + '/nrmse ' + basedir + '/pngoutput/' + name + '/nrmse')
	print "png2rgbAll.py done ... (rgb2png)"
	
	#os.system(basedir + '/png2rgbAll.py rgb2png ' + basedir + '/rgboutput/' + name + '/psnr ' + basedir + '/pngoutput/' + name + '/psnr')
	#print "png2rgbAll.py done ... (rgb2png)"
	
	os.system('rm -rf ' + basedir + '/rgboutput/' + name)
	os.system('rm ' + basedir + '/images/' + rgbfilename)

def main():
	newfiles = []
	files = os.popen('ls images | grep png').readlines()
	PARALLEL_WIDTH = 3
	for f in files:
		print f.strip('\n')
		newfiles.append(f.strip('\n'))

	for chunk in range(0, (len(newfiles) / PARALLEL_WIDTH) + 1):
		pool = [Process(target=runMean, args=(str(newfiles[i + chunk * PARALLEL_WIDTH]),)) for i in range(min(PARALLEL_WIDTH * (chunk+1), len(newfiles)) - PARALLEL_WIDTH * chunk)]
		for i in range(min(PARALLEL_WIDTH * (chunk + 1), len(newfiles)) - PARALLEL_WIDTH * chunk):
			pool[i].start()
		for p in pool:
			p.join()
	print
	print "DONE!"

if __name__ == '__main__':	
	main()
