#!/bin/env python

from flask import render_template, request

from gatech import app, session

from game1_acceptable.acceptable import start_acceptable
from game2_winabatt.winabatt import start_winabatt
from game3_qna.qna import start_qna

from database import db_session
from database import init_db
from database import clean_db
from query import upload_files, upload_files_old, add_user, doLogin

import os, time
from enum import Enum

@app.route("/selectgame", methods=['POST', 'GET'])
def selectgame():

	if request.method == "POST":
		action = request.form.keys()[0]
		action = action.split('.')[0]
		msg = action  # for debug
		os.system('echo startgame: ' + msg)
		if action == 'start':
			return render_template('select_game.html')


@app.route("/playgame", methods=['POST', 'GET'])
def playgame():

	if request.method == "POST":
		action = request.form.keys()[0]
		action = action.split('.')[0]
		msg = action  # for debug
		os.system('echo rungame: ' + msg)
		if action == 'acceptable':
			return start_acceptable()
		if action == 'winabatt':
			return start_winabatt()
		if action == 'qna':
			return start_qna()

@app.route('/reset')
def reset():
	clean_database()
	initialize_database()
	status = upload()
	os.system('echo reset: ' + status)
	return status

@app.route('/upload')
def upload():
	status = upload_files()
	return status

@app.route('/upload_old', methods = ['POST', 'GET'])
def upload_old():
	orgpath = ''
	degpath = ''
	sobelpath = ''
	if request.method == "GET":
		orgpath = request.args.get('orgpath', '')
		degpath = request.args.get('degpath', '')
		sobelpath = request.args.get('sobelpath', '')
	status = upload_files_old(orgpath, degpath, sobelpath)
	return status

@app.route('/initdb')
def initialize_database():
	init_db()
	return "initializing database done ..."

@app.route('/cleandb')
def clean_database():
	clean_db()
	return "cleaning database done ..."

@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()

class State(Enum):
	default = 0
	login = 1
	login_success = 2
	register = 3
	create = 4
	mismatch = 5
	create_success = 6
	gohome = 7
	incorrect_password = 8
	duplicate_id = 9

@app.route("/login", methods = ['POST', 'GET'])
def login():
	if request.method == "POST":
		state = State.default
		for action in request.form.keys():
			action = action.split('.')[0]
			if action == "login":
				state = State.login
				break
			elif action == "register":
				state = State.register
				break
			elif action == "create":
				state = State.create
				break
			elif action == "gohome":
				state = State.gohome
				break
			elif action == "back":
				state = State.gohome
				break

		os.system('echo ' + str(action))
		if state == State.login:
			username = request.form['username']
			processed_username = username.lower()
			password = request.form['password']
			processed_password = password.lower()
			if doLogin(processed_username,processed_password):
				session['userid'] = processed_username
				return render_template('index.html',state=State.login_success)
			else:
				return render_template('index.html',state=State.incorrect_password)

		elif state == State.register:
			return render_template('index.html',state=State.register)
		elif state == State.create:
			username = request.form['username'].lower()
			password = request.form['password'].lower()
			repeat_password = request.form['repeat_password'].lower()
			if password != repeat_password:
				return render_template('index.html',state=State.mismatch)
			if add_user(username, password):
				return render_template('index.html',state=State.create_success)
			else:
				return render_template('index.html',state=State.duplicate_id)
		elif state == State.gohome:
			return render_template('index.html',state=State.default)

@app.route("/logout")
def logout():
	os.system('echo logout')
	session.clear()
	return render_template('index.html',state=State.default)

@app.route('/')
def index():
	return render_template('index.html',state=State.default)
