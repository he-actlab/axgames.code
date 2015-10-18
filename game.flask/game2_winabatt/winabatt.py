#!/bin/env python

from gatech import app
from gatech import session

from flask import render_template, request
from query_winabatt import draw_winabatt_image_file, save_play
from core_winbatt import get_reward, get_winning
from gatech.conf import gamedata_home_url, max_round, GAME2_INIT_ENERGY, KERNEL_NAME, GAME_NAME, APPLICATION_TYPE
from gatech.query import store_session, get_promo_code

import os, sys, uuid

def getHtmlTemplate():
	if APPLICATION_TYPE == 'IP':
		return 'play_winabatt_ip.html'
	elif APPLICATION_TYPE == 'OCR':
		return 'play_winabatt_ocr.html'
	elif APPLICATION_TYPE == 'SR':
		return 'play_winabatt_sr.html'
	elif APPLICATION_TYPE == 'AE':
		return 'play_winabatt_ae.html'
	else:
		print 'Error: unknown applicaiton type'
		sys.exit()

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
			os.system('echo action: ' + str(action))
			tokens = action.split("_")
			bet = tokens[1]
			error_rate = tokens[2]

			os.system('echo winabatt: tokens ' + str(tokens))
			session['power'] -= int(bet)

			# reward, selections, average = get_reward(session['imagename'] + ".png", int(bet), int(error_rate))
			reward, average = get_winning(session['imagename'] + ".png", int(error_rate))
			if save_play(session['sessionid'], 1, session['imagename'], error_rate, bet, reward) == True:
				os.system('echo power ' + str(session['power']))
				os.system('echo bet ' + bet)
				session['old_power_history'].append(session['power'] + int(bet))
				session['power'] += reward
				session['power_history'].append(session['power'])
				session['error_history'].append(error_rate)
				session['bet_history'].append(int(bet))
				session['reward_history'].append(reward)
				# session['selections_history'].append(selections)
				session['average_history'].append(average)

				os.system('echo winabatt: stage ' + str(session['stage']))
				os.system('echo winabatt: power_history ' + str(session['power_history']))
				os.system('echo winabatt: error_history ' + str(session['error_history']))
				os.system('echo winabatt: bet_history ' + str(session['bet_history']))
				os.system('echo winabatt: reward_history ' + str(session['reward_history']))
				# os.system('echo winabatt: selections_history ' + str(session['selections_history']))
				os.system('echo winabatt: average ' + str(session['average_history']))
			return render_template('result_winabatt.html',
									 imagename=session['imagename'], \
									 power=session['power'], \
									 stage=session['stage'], \
									 power_history=session['power_history'], \
									 old_power_history=session['old_power_history'], \
									 error_history=session['error_history'], \
									 bet_history=session['bet_history'], \
									 reward_history=session['reward_history'], \
									 # selections_history=session['selections_history'], \
									 sessionid=session['sessionid'], \
									 gamedata_home_url=gamedata_home_url, \
									 max_round=max_round, \
									 average=session['average_history'], \
								     uniq_code=session['uniq_code'], \
								     GAME_NAME=GAME_NAME)

		elif action == 'continue':
			os.system('echo continue')
			if len(session['power_history']) == session['stage']:
				session['stage'] = len(session['power_history']) + 1
				session['imagename'] = draw_winabatt_image_file()
			return render_template(getHtmlTemplate(), \
									 imagename=session['imagename'], \
									 power=session['power'], \
									 stage=session['stage'], \
									 sessionid=session['sessionid'], \
									 gamedata_home_url=gamedata_home_url, \
								     kernel_name=KERNEL_NAME, \
								     GAME_NAME=GAME_NAME)

		elif action == 'initialize':
			initialize()
			session['imagename'] = draw_winabatt_image_file()

		elif action == 'finish':
			session.clear()
			return render_template('index.html', \
								   state=0, \
								   GAME_NAME=GAME_NAME)

		return render_template(getHtmlTemplate(),
								 imagename=session['imagename'], \
								 power=session['power'], \
								 stage=session['stage'], \
								 sessionid=session['sessionid'], \
								 gamedata_home_url=gamedata_home_url, \
							     kernel_name=KERNEL_NAME, \
							     GAME_NAME=GAME_NAME)


def init_session():
	uid = uuid.uuid4()
	session['sessionid'] = str(uid)
	session['uniq_code'] = str(get_promo_code(10))
	store_session(session['userid'], session['sessionid'], session['uniq_code'])
	session['win'] = 0.0
	initialize()


def initialize():
	session['power'] = GAME2_INIT_ENERGY
	session['stage'] = 1
	session['power_history'] = []
	session['old_power_history'] = []
	session['error_history'] = []
	session['bet_history'] = []
	session['reward_history'] = []
	session['selections_history'] = []
	session['average_history'] = []


def start_winabatt():
	os.system('echo start_winabatt start')

	init_session()
	session['imagename'] = draw_winabatt_image_file()

	os.system('echo start_winabatt: ' + session['imagename'])
	return render_template(getHtmlTemplate(),
							 imagename=session['imagename'], \
							 power=session['power'], \
							 stage=session['stage'], \
							 sessionid=session['sessionid'], \
							 gamedata_home_url=gamedata_home_url, \
						     kernel_name=KERNEL_NAME, \
						     GAME_NAME=GAME_NAME)
