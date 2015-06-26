#!/usr/bin/python

import os, sys

sysname = os.popen('uname').read().strip('\n')

if sysname == 'Linux':
	os.system('sudo service redis-server restart')
	os.system('sudo /etc/init.d/nginx restart')

	logname = os.popen('date +%m%d%Y_%H%M%S').read().strip('\n') + '.log'

	print('gunicorn gatech:app --log-file=- 2>> ' + logname + ' >> ' + logname + ' &')
	os.system('gunicorn gatech:app --log-file=- 2>> ' + logname + ' >> ' + logname + ' &')

elif sysname == 'Darwin':
	os.system('sudo service redis-server restart')
	os.system('sudo /etc/init.d/nginx restart')

	logname = os.popen('date +%m%d%Y_%H%M%S').read().strip('\n') + '.log'

	print('gunicorn gatech:app --log-file=- 2>> ' + logname + ' >> ' + logname + ' &')
	os.system('gunicorn gatech:app --log-file=- 2>> ' + logname + ' >> ' + logname + ' &')

else:
	os.system('Error! Unknown System')
	sys.exit()



