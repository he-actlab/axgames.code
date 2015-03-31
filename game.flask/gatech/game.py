#!/bin/env python
	
from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.session import Session
from flask.ext.uuid import FlaskUUID
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from database import db_session
from database import init_db
from query import upload_files, draw_image_files, get_image_id
#from models import Image, DegradedImage
from models import Image
from core import scoring, final_score, calculate_reward

import os, random, uuid
import psycopg2
import urlparse

from enum import Enum
class Color(Enum):
	saColor = "#006400"
	naColor = "#3EA055" 
	waColor = "#C0D890"
	wrColor = "#ffa07a"
	nrColor = "#ed4337"
	srColor = "#8B0000"

app = Flask(__name__)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
FlaskUUID(app)
Bootstrap(app)

def init_session():
	uid=uuid.uuid4()
	session['username'] = str(uid)
	session['win'] = 0.0
	initialize()

def initialize():
	session['bankroll'] = 10000
	session['bet'] = 0
	session['stage'] = 1
	session['betmoney'] = 0
	session['score'] = []
	session['options'] = []
	session['proportion'] = []
	session['decision_location'] = []
	session['color'] = []
	session['bankroll_history'] = []
	session['lock'] = False
	session['filepaths'] = []
	session['degimageid'] = -1
	session['expired'] = False

@app.route("/original", methods = ['POST', 'GET'])
def original():
	msg = ''
	money = 0
	final = 0
	decision = ''
	winlose = ''

	if request.method == "POST":
		action = request.form.keys()[0]
		action = action.split('.')[0]
		msg = action # for debug
		os.system('echo ' + msg)

		init_session()
		session['filepaths'] = draw_image_files()
		filename = ((session['filepaths'])[2]).split('/')[1]
		session['degimageid'] = get_image_id(filename)

	return render_template('original.html', \
						bankroll=session['bankroll'], \
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

def getColor(decision):
	if decision == "SA":
		return Color.saColor
	elif decision == "NA":
		return Color.naColor
	elif decision == "WA":
		return Color.waColor
	elif decision == "WR":
		return Color.wrColor
	elif decision == "NR":
		return Color.nrColor
	elif decision == "SR":
		return Color.srColor

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
		os.system('echo ' + msg)
		if action == 'startbet':
			filename = ((session['filepaths'])[2]).split('/')[1]
			session['degimageid'] = get_image_id(filename)
		elif session['expired'] == True:
			decision = "finish"
		elif action == 'continue':
			os.system('echo continue')
			session['stage'] += 1
			session['bankroll'] += session['score'][len(session['score']) - 1]
			session['betmoney'] = 0
			session['lock'] = False
			session['filepaths'] = draw_image_files()
			filename = ((session['filepaths'])[2]).split('/')[1]
			session['degimageid'] = get_image_id(filename)
			return render_template('original.html', \
									bankroll=session['bankroll'], \
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
		elif action == 'finish':
			return render_template('index.html')
		elif action == 'initialize':
				initialize()
				session['filepaths'] = draw_image_files()
				filename = ((session['filepaths'])[2]).split('/')[1]
				session['degimageid'] = get_image_id(filename)
		elif session['lock'] == True:
			if action == 'final':
				finalNum = final_score(session['score'])
				decision = "final"
				final = str(finalNum)
				if final > 0:
					winlose = 'Win'
				else:
					winlose = 'Lose'
				session['lock'] = True	
			else:
				decision = 'pending'
		else:
			if action == 'SA' or action == 'NA' or action == 'WA' or action == 'WR' or action == 'NR' or action == 'SR':
				if session['betmoney'] == 0:
					decision = 'nobet'
				else:
					score, options, proportion, decision_location = scoring(action, session['betmoney'], session['degimageid'])
					if score > 0.0:
						winlose = 'Win'
					else:
						winlose = 'Lose'
					session['score'].append(int(score))
					bankroll = session['bankroll'] + int(score)
					session['bankroll_history'].append(bankroll)
					session['options'].append(options)
					session['proportion'].append(proportion)
					session['decision_location'].append(decision_location)
					color = []
					for option in options:
						color.append(getColor(option))
					session['color'].append(color)
					session['lock'] = True
					
					return render_template('result.html', \
											stage=range(1,session['stage'] + 1), \
											score=session['score'], \
											options=session['options'], \
											proportion=session['proportion'], \
											decision_location=session['decision_location'], \
											color=session['color'], \
											bankroll_history=session['bankroll_history'])

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
			if (session['bankroll'] - session['betmoney'] - money >= 0):
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
