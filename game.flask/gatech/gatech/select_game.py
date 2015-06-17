#!/bin/env python

from flask import render_template, request
from gatech import app
from game1_acceptable import start_acceptable
from game2_winbatt import start_winbatt
from game3_qna import start_qna

from database import db_session
from database import init_db
from query import upload_files

import os

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
		if action == 'winbatt':
			return start_winbatt()
		if action == 'qna':
			return start_qna()

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