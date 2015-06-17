#!/bin/env python

from gatech import app
from gatech import session

from flask import render_template, request
from query import draw_image_files, get_image_id
from core import scoring

import os, uuid

from enum import Enum

class Color(Enum):
	saColor = "#006400"
	waColor = "#C0D890"
	wdColor = "#ffa07a"
	sdColor = "#8B0000"

def init_session():
	uid = uuid.uuid4()
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
	session['filepaths'] = []
	session['degimageid'] = -1
	session['expired'] = False


def getColor(decision):
	if decision == "SA":
		return Color.saColor
	elif decision == "WA":
		return Color.waColor
	elif decision == "WD":
		return Color.wdColor
	elif decision == "SD":
		return Color.sdColor

@app.route("/acceptable", methods=['POST', 'GET'])
def game():
	msg = ''
	money = 0
	final = 0
	decision = ''
	winlose = ''

	if request.method == "POST":
		action = request.form.keys()[0]
		action = action.split('.')[0]
		msg = action  # for debug
		os.system('echo ' + msg)
		if action == 'start':
			init_session()
			session['filepaths'] = draw_image_files()
			filename = ((session['filepaths'])[2]).split('/')[1]
			session['degimageid'] = get_image_id(filename)
		elif action == 'startbet':
			filename = ((session['filepaths'])[2]).split('/')[1]
			session['degimageid'] = get_image_id(filename)
		elif session['expired'] == True:
			decision = "finish"
		elif action == 'continue':
			os.system('echo continue')
			session['stage'] += 1
			session['bankroll'] += session['score'][len(session['score']) - 1]
			session['betmoney'] = 0
			session['filepaths'] = draw_image_files()
			filename = ((session['filepaths'])[2]).split('/')[1]
			session['degimageid'] = get_image_id(filename)
			#			return render_template('original.html', \
			return render_template('play_acceptable.html', \
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
		else:
			if action == 'SA' or action == 'WA' or action == 'WD' or action == 'SD':
				if session['betmoney'] == 0:
					decision = 'nobet'
				else:
					score, options, proportion, decision_location = scoring(action, session['betmoney'],
																			session['degimageid'])
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

					return render_template('result.html', \
										   stage=range(1, session['stage'] + 1), \
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
	return render_template('play_acceptable.html', \
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

def start_acceptable():
	msg = ''
	final = 0
	decision = ''
	winlose = ''

	init_session()
	session['filepaths'] = draw_image_files()
	filename = ((session['filepaths'])[2]).split('/')[1]
	session['degimageid'] = get_image_id(filename)
	os.system('echo here')
	return render_template('play_acceptable.html', \
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

#
# if __name__ == '__main__':
# 	app.debug = True
# 	app.secret_key = '\xc9\x93\xd6\x9d\x9b\x99d\xf6\x04\xcf%\xac\xc5\x00\xf0\xb1\x97U\xb4S\x805y'
# 	app.run()
