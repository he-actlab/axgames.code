#!/usr/bin/python

import os, sys, time

sysname = os.popen('uname').read().strip('\n')

if sysname == 'Linux':
	os.system('killall -9 gunicorn')

elif sysname == 'Darwin':
	os.system('pkill -f gunicorn > /dev/null 2> /dev/null ')
	os.system('pkill -f redis-server > /dev/null 2> /dev/null ')
	time.sleep(1)
	os.system('rm dump.rdb')

else:
	print 'Error! Unknown System'

