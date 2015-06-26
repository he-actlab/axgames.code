#!/bin/env python

from gatech import app
from gatech import session

from flask import render_template, request
from query_winabatt import draw_winabatt_image_file, save_play
from core_winbatt import get_reward
from gatech.conf import gamedata_home_url
from gatech.query import store_session

import os, uuid

@app.route("/winabatt", methods=['POST', 'GET'])
def winabatt():

	if request.method == "POST":
		action = request.form.keys()[0]
		action = action.split('.')[0]
		msg = action  # for debug

		if action == 'start':
			init_session()
			session['imagename'] = draw_winabatt_image_file()

		elif "bet" in action:
			os.system('echo userid: ' + str(session['userid']))
			os.system('echo sessionid: ' + str(session['sessionid']))
			tokens = action.split("_")
			bet = tokens[1]
			error_rate = tokens[2]

			os.system('echo winabatt: tokens ' + str(tokens))
			session['power'] -= int(bet)

			reward, selections = get_reward(session['imagename'] + ".png", int(bet), int(error_rate))
			save_play(session['sessionid'], 1, session['imagename'], error_rate, bet)

			session['power'] += reward
			session['power_history'].append(session['power'])
			session['bet_history'].append(float(bet))
			session['reward_history'].append(reward)
			session['selections_history'].append(selections)

			os.system('echo winabatt: stage ' + str(session['stage']))
			os.system('echo winabatt: power_history ' + str(session['power_history']))
			os.system('echo winabatt: bet_history ' + str(session['bet_history']))
			os.system('echo winabatt: reward_history ' + str(session['reward_history']))
			os.system('echo winabatt: selections_history ' + str(session['selections_history']))
			return render_template('result_winabatt.html',
						       imagename=session['imagename'], \
						       power=session['power'], \
						       stage=session['stage'], \
							   power_history=session['power_history'], \
							   bet_history=session['bet_history'], \
							   reward_history=session['reward_history'], \
							   selections_history=session['selections_history'], \
							   sessionid=session['sessionid'], \
							   gamedata_home_url=gamedata_home_url)

		elif action == 'continue':
			os.system('echo continue')
			session['stage'] = len(session['power_history']) + 1
			session['imagename'] = draw_winabatt_image_file()
			return render_template('play_winabatt.html', \
						       imagename=session['imagename'], \
						       power=session['power'], \
							   stage=session['stage'], \
							   sessionid=session['sessionid'], \
							   gamedata_home_url=gamedata_home_url)

		elif action == 'initialize':
			initialize()
			session['imagename'] = draw_winabatt_image_file()

		elif action == 'finish':
			session.clear()
			return render_template('index.html', state=0)

		return render_template('play_winabatt.html',
						   imagename=session['imagename'], \
						   power=session['power'], \
						   stage=session['stage'], \
						   sessionid=session['sessionid'], \
						   gamedata_home_url=gamedata_home_url)

def init_session():
	uid = uuid.uuid4()
	session['sessionid'] = str(uid)
	store_session(session['userid'], session['sessionid'])
	session['win'] = 0.0
	initialize()

def initialize():
	session['power'] = 200.0
	session['stage'] = 1
	session['power_history'] = []
	session['bet_history'] = []
	session['reward_history'] = []
	session['selections_history'] = []

def start_winabatt():
	os.system('echo start_winabatt start')

	init_session()
	session['imagename'] = draw_winabatt_image_file()

	os.system('echo start_winabatt: ' + session['imagename'])
	return render_template('play_winabatt.html',
						   imagename=session['imagename'], \
						   power=session['power'], \
						   stage=session['stage'], \
						   sessionid=session['sessionid'], \
						   gamedata_home_url=gamedata_home_url)
