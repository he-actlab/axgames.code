#!/bin/env python
	
from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.session import Session
from flask.ext.uuid import FlaskUUID
from flask.ext.sqlalchemy import SQLAlchemy

from database import db_session
from database import init_db
from query import upload_files, draw_image_files
#from models import Image, DegradedImage
from models import Image
from core import scoring, final_score

import os, random, uuid
import psycopg2
import urlparse

app = Flask(__name__)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
FlaskUUID(app)

def init_session():
	uid=uuid.uuid4()
	session['username'] = str(uid)
	session['bankroll'] = 10000
	session['bet'] = 0
	session['win'] = 0
	session['stage'] = 1
	session['betmoney'] = 0
	session['score'] = []
	session['lock'] = False
	session['filepaths'] = []

@app.route("/game", methods = ['POST', 'GET'])
def game():
	msg = ''
	money = 0
	final = 0
	decision = ''
	winlose = ''
	
	if request.method == "POST":
		action = request.form.keys()[0]
		action = action.split('.')[0]
		msg = action # for debug
		if action == 'start':
			init_session()
			session['filepaths'] = draw_image_files()
		elif session['lock'] == True:
			if action == 'continue':
				session['stage'] += 1
				session['bankroll'] += session['score'][len(session['score']) - 1]
				session['betmoney'] = 0
				session['lock'] = False
				session['filepaths'] = draw_image_files()
			elif action == 'final':
				finalNum = final_score(session['score'])
				decision = "final"
				final = str(finalNum)
				if final > 0:
					winlose = 'Win'
				else:
					winlose = 'Lose'
			else:
				decision = 'pending'
		else:
			if action == 'accept':
				if session['betmoney'] == 0:
					decision = 'nobet'
				else:
					decision = 'accept'	
					score = scoring(decision, session['betmoney'])
					if score > 0.0:
						winlose = 'Win'
					else:
						winlose = 'Lose'
					session['score'].append(score)
					session['lock'] = True
			elif action == 'reject':
				if session['betmoney'] == 0:
					decision = 'nobet'
				else:
					decision = 'reject'
					score = scoring(decision, session['betmoney'])
					if score > 0.0:
						winlose = 'Win'
					else:
						winlose = 'Lose'
					session['score'].append(score)
					session['lock'] = True
			elif action == 'clear':
				session['betmoney'] = 0
			elif action == '5d':
				money = 5
			elif action == '25d':
				money = 25
			elif action == '100d':
				money = 100
			elif action == '500d':
				money = 500
			elif action == '1000d':
				money = 1000
			elif action == '5000d':
				money = 5000
			if (session['bankroll'] - session['betmoney'] - money > 0):
				session['betmoney'] += money
	return render_template('play.html', \
						bankroll=session['bankroll'] - session['betmoney'], \
						bet=session['bet'] + session['betmoney'], \
						win=session['win'], \
						stage=session['stage'], \
						decision=decision, \
						winlose=winlose, \
						score=session['score'], \
						final=final, \
						filePaths=session['filepaths'], \
						msg=str(msg), \
						username=session['username'])

@app.route('/upload', methods = ['POST', 'GET'])
def upload():
	orgpath = ''
	degpath = ''
	sobelpath = ''
	if request.method == "GET":
		orgpath = request.args.get('orgpath', '')
		degpath = request.args.get('degpath', '')
		sobelpath = request.args.get('sobelpath', '')
	status = upload_files(orgpath, degpath, sobelpath)
	return status

@app.route('/initdb')
def initialize_database():
	init_db()
	return "initializing database done ..."

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
 	return render_template('index.html')

if __name__ == '__main__':
	app.debug = True
	app.secret_key = '\xc9\x93\xd6\x9d\x9b\x99d\xf6\x04\xcf%\xac\xc5\x00\xf0\xb1\x97U\xb4S\x805y'
	app.run()
