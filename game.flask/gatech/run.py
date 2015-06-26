#!/usr/bin/python

import os, sys

os.system('sudo service redis-server restart')
os.system('sudo /etc/init.d/nginx restart')
os.system('gunicorn gatech:app --log-file=-')
