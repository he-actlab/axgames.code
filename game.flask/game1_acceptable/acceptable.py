#!/bin/env python

from gatech import app
from gatech import session

from flask import render_template, request
from query_acceptable import draw_acceptable_image_files, get_image_id, get_degimage_id, save_play, save_play_gallery
from core_acceptable import scoring
from gatech.query import store_session
from gatech.conf import gamedata_home_url, max_round

import os, uuid

from enum import Enum


class Color(Enum):
	agreeColor = "#006400"
	disagreeColor = "#8B0000"


def getColor(decision):
	if decision == "agree":
		return Color.agreeColor
	elif decision == "disagree":
		return Color.disagreeColor


@app.route("/acceptable", methods=['POST', 'GET'])
def acceptable():
	msg = ''
	money = 0
	final = 0
	decision = ''
	if request.method == "POST":
		action = request.form.keys()[0]
		action = action.split('.')[0]
		msg = action  # for debug
		os.system('echo ' + msg)
		if action == 'start':
			init_session()
			session['ig_id'], session['filePathsList'] = draw_acceptable_image_files(session['userid'])
			session['filepaths'] = (session['filePathsList'])[session['stage']-1]
			session['imageid'] = get_image_id(((session['filepaths'])[0]).split('/')[2])
			session['degimageid'] = get_degimage_id(((session['filepaths'])[2]).split('/')[2])
		elif action == 'startbet':
			session['imageid'] = get_image_id(((session['filepaths'])[0]).split('/')[2])
			session['degimageid'] = get_degimage_id(((session['filepaths'])[2]).split('/')[2])
		elif session['expired'] == True:
			decision = "finish"
		elif action == 'continue':
			session['stage'] = len(session['bankroll_history']) + 1
			session['bankroll'] += session['score'][len(session['score']) - 1] - session['betmoney'] # todo - known bug: if players click continue twice quickly, the bankroll will be increased twice
			session['betmoney'] = 0
			session['filepaths'] = (session['filePathsList'])[session['stage']-1]
			session['imageid'] = get_image_id(((session['filepaths'])[0]).split('/')[2])
			session['degimageid'] = get_degimage_id(((session['filepaths'])[2]).split('/')[2])
			return render_template('play_acceptable.html', \
									 bankroll=session['bankroll'], \
									 bet=session['betmoney'], \
									 win=session['win'], \
									 stage=session['stage'], \
									 decision=decision, \
									 score=session['score'], \
									 final=final, \
									 filePaths=session['filepaths'], \
									 msg=str(msg), \
									 sessionid=session['sessionid'], \
									 gamedata_home_url=gamedata_home_url)
		elif action == 'finish':
			save_play_gallery(session['userid'], session['ig_id'], session['sessionid'], session['playidlist'])
			session.clear()
			return render_template('index.html', state=0)
		elif action == 'initialize':
			save_play_gallery(session['userid'], session['ig_id'], session['sessionid'], session['playidlist'])
			initialize()
			session['ig_id'], session['filePathsList'] = draw_acceptable_image_files(session['userid'])
			session['filepaths'] = (session['filePathsList'])[session['stage']-1]
			session['imageid'] = get_image_id(((session['filepaths'])[0]).split('/')[2])
			session['degimageid'] = get_degimage_id(((session['filepaths'])[2]).split('/')[2])
		else:
			if action == 'agree' or action == 'disagree':
				if session['betmoney'] == 0:
					decision = 'nobet'
				else:
					score, options, proportion, decision_location = scoring(action, session['betmoney'], session['degimageid'])

					play_id = save_play(session['sessionid'], 0, session['imageid'], session['degimageid'], action, session['betmoney'], score)

					session['playidlist'].append(play_id)
					session['score'].append(int(score))
					session['old_bankroll_history'].append(session['bankroll'])
					session['bankroll_history'].append(session['bankroll'] + int(score) - session['betmoney'])
					session['options'].append(options)
					session['proportion'].append(proportion)
					session['decision_location'].append(decision_location)
					session['bet_history'].append(session['betmoney'])
					color = []
					for option in options:
						color.append(getColor(option))
					session['color'].append(color)

					return render_template('result_acceptable.html', \
											 stage=range(1, session['stage'] + 1), \
											 score=session['score'], \
											 options=session['options'], \
											 proportion=session['proportion'], \
											 decision_location=session['decision_location'], \
											 color=session['color'], \
										   	 old_bankroll_history=session['old_bankroll_history'], \
											 bankroll_history=session['bankroll_history'], \
											 gamedata_home_url=gamedata_home_url, \
											 max_round=max_round, \
										     bet_history=session['bet_history'])
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
			os.system('echo acceptable: filepaths = ' + str(session['filepaths']))
	return render_template('play_acceptable.html', \
							 bankroll=session['bankroll'] - session['betmoney'], \
							 bet=session['betmoney'], \
							 win=session['win'], \
							 stage=session['stage'], \
							 decision=decision, \
							 score=session['score'], \
							 final=final, \
							 filePaths=session['filepaths'], \
							 msg=str(msg), \
							 sessionid=session['sessionid'], \
							 gamedata_home_url=gamedata_home_url)


def start_acceptable():
	os.system('echo start_acceptable start')

	msg = ''
	final = 0
	decision = ''

	init_session()
	session['ig_id'], session['filePathsList'] = draw_acceptable_image_files(session['userid'])
	session['filepaths'] = (session['filePathsList'])[session['stage']-1]
	session['imageid'] = get_image_id(((session['filepaths'])[0]).split('/')[2])
	session['degimageid'] = get_degimage_id(((session['filepaths'])[2]).split('/')[2])
	return render_template('play_acceptable.html', \
							 bankroll=session['bankroll'] - session['betmoney'], \
							 bet=session['betmoney'], \
							 win=session['win'], \
							 stage=session['stage'], \
							 decision=decision, \
							 score=session['score'], \
							 final=final, \
							 filePaths=session['filepaths'], \
							 msg=str(msg), \
							 gamedata_home_url=gamedata_home_url)


def init_session():
	uid = uuid.uuid4()
	session['sessionid'] = str(uid)
	store_session(session['userid'], session['sessionid'])
	session['win'] = 0.0
	initialize()

def initialize():
	session['bankroll'] = 5000
	session['stage'] = 1
	session['betmoney'] = 0
	session['score'] = []
	session['options'] = []
	session['proportion'] = []
	session['color'] = []
	session['ig_id'] = -1
	session['filePathsList'] = []
	session['degimageid'] = -1
	session['expired'] = False
	session['playidlist'] = []
	session['decision_location'] = []
	session['old_bankroll_history'] = []
	session['bankroll_history'] = []
	session['bet_history'] = []

#
# if __name__ == '__main__':
# 	app.debug = True
# 	app.secret_key = '\xc9\x93\xd6\x9d\x9b\x99d\xf6\x04\xcf%\xac\xc5\x00\xf0\xb1\x97U\xb4S\x805y'
# 	app.run()
