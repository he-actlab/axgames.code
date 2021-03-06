#!/bin/env python

from flask import render_template, request

from gatech import app, session

from game1_pollice_verso.pollice_verso import start_acceptable
from game2_winabatt.winabatt import start_winabatt
from game3_qna.qna import start_qna

from database import db_session
from database import init_db
from database import clean_db
from query import upload_files, add_user, doLogin, get_user_id
from conf import max_round, GAME1_INIT_BALANCE, KERNEL_NAME, GAME_NAME

import os, time, threading
from enum import Enum

@app.route("/selectgame", methods=['POST', 'GET'])
def selectgame():

	os.system('echo startgame: here')
	if request.method == "POST":
		os.system('echo startgame: here2')
		action = request.form.keys()[0]
		os.system('echo startgame: ' + action)
		action = action.split('.')[0]
		os.system('echo startgame: ' + action)
		if action == 'start':
			return render_template('select_game.html', \
								   GAME_NAME=GAME_NAME)


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

# @app.route('/reset')
# def reset():
# 	clean_database()
# 	initialize_database()
# 	upload_thread = threading.Thread(target=upload_files, args='')
# 	upload_thread.start()
# 	return "reset start"
#
# @app.route('/upload')
# def upload():
# 	upload_thread = threading.Thread(target=upload_files, args='')
# 	upload_thread.start()
# 	return "upload_files start"
#
# @app.route('/initdb')
# def initialize_database():
# 	init_db()
# 	return "initializing database done ..."
#
# @app.route('/cleandb')
# def clean_database():
# 	clean_db()
# 	return "cleaning database done ..."

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
				session['userid'] = get_user_id(processed_username)
				renderState = State.login_success
			else:
				renderState = State.incorrect_password

		elif state == State.register:
			renderState = State.register
		elif state == State.create:
			username = request.form['username'].lower()
			password = request.form['password'].lower()
			repeat_password = request.form['repeat_password'].lower()
			if password != repeat_password:
				renderState = State.mismatch
			else:
				if add_user(username, password):
					renderState = State.create_success
				else:
					renderState = State.duplicate_id
		elif state == State.gohome:
			renderState = State.default

		return render_template('index.html', \
							   state=renderState, \
							   max_round=max_round, \
							   GAME1_INIT_BALANCE=GAME1_INIT_BALANCE, \
							   KERNEL_NAME=KERNEL_NAME, \
							   GAME_NAME=GAME_NAME)

@app.route("/logout")
def logout():
	os.system('echo logout')
	session.clear()
	return render_template('index.html', \
						   state=State.default, \
						   max_round=max_round, \
						   GAME1_INIT_BALANCE=GAME1_INIT_BALANCE, \
						   KERNEL_NAME=KERNEL_NAME, \
						   GAME_NAME=GAME_NAME)

@app.route('/')
def index():
	return render_template('index.html', \
						   state=State.default, \
						   max_round=max_round, \
						   GAME1_INIT_BALANCE=GAME1_INIT_BALANCE, \
						   KERNEL_NAME=KERNEL_NAME, \
						   GAME_NAME=GAME_NAME)
