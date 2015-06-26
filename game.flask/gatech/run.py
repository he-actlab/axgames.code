#!/usr/bin/python

import os, sys

sysname = os.popen('uname').read().strip('\n')

# Deployment on Linux machine. addr: taftan.cc.gt.atl.ga.us
if sysname == 'Linux':
	os.system('sudo service redis-server restart')
	os.system('sudo /etc/init.d/nginx restart')

	logname = os.popen('date +%m%d%Y_%H%M%S').read().strip('\n') + '.log'

	print('gunicorn gatech:app --log-file=- 2>> ' + logname + ' >> ' + logname + ' &')
	os.system('gunicorn gatech:app --log-file=- 2>> ' + logname + ' >> ' + logname + ' &')

# Only for development. addr: localhost:5000 
elif sysname == 'Darwin':
	os.system('redis-server > /dev/null 2> /dev/null & ')

	logname = os.popen('date +%H%M%S_%m%d%Y').read().strip('\n') + '.log'

	os.system('foreman start 2>> ' + logname + ' >> ' + logname + ' &')

else:
	print 'Error! Unknown System'



