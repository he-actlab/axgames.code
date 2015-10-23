#!/bin/env python

from gatech import app
from gatech import session

from flask import render_template, request
from query_qna import draw_qna_image_file, get_qna, save_play, getHtmlTemplate, getResultTemplate
from core_qna import get_reward, get_winning
from gatech.conf import gamedata_home_url, max_round, GAME3_INIT_ENERGY, GAME3_WRONG_ANSWER_PENALTY, KERNEL_NAME, GAME_NAME, APPLICATION_TYPE
from gatech.query import store_session, get_promo_code
from gatech.query import getExtensions

import os, sys, uuid

@app.route("/qna", methods=['POST', 'GET'])
def qna():
	if request.method == "POST":
		for action in request.form.keys():
			action = action.split('.')[0]
			msg = action  # for debug
			inext, outext = getExtensions()
			if action == 'start':
				init_session()
				session['imagename'] = draw_qna_image_file()
				session['question'], session['correct_answer'], session['answers'] = get_qna(session['filename'] + inext)
				return render_template(getHtmlTemplate(),
										 imagename=session['imagename'], \
										 power=session['power'], \
										 stage=session['stage'], \
										 question=session['question'], \
										 answers=session['answers'], \
										 sessionid=session['sessionid'], \
										 gamedata_home_url=gamedata_home_url, \
									     kernel_name=KERNEL_NAME, \
									     init_slider_value='50', \
									     GAME_NAME=GAME_NAME)

			elif "bet" in action:
				tokens = action.split("_")
				bet = tokens[1]
				error_rate = tokens[2]
				os.system('echo qna: bet - ' + bet)
				os.system('echo qna: error_rate - ' + error_rate)

				if 'answer_radiobutton' in request.form.keys():
					selected_answer = request.form['answer_radiobutton']
					os.system('echo qna: ' + selected_answer)

					session['power'] -= int(bet)

					# reward, selections, average = get_reward(session['imagename'] + ".png", int(bet), int(error_rate), session['correct_answer'] == selected_answer)
					reward, average = get_winning(session['imagename'] + inext, int(error_rate))
					penalty = GAME3_WRONG_ANSWER_PENALTY if session['correct_answer'] != selected_answer else 0
					if save_play(session['sessionid'], 2, session['imagename'], error_rate, bet, session['correct_answer'] == selected_answer, reward - penalty) == True:
						session['old_power_history'].append(session['power'] + int(bet))
						session['power'] += reward - penalty
						session['power_history'].append(session['power'])
						session['error_history'].append(error_rate)
						session['bet_history'].append(int(bet))
						session['reward_history'].append(reward)
						# session['selections_history'].append(selections)
						session['average_history'].append(average)
						session['penalty_history'].append(int(penalty))

						os.system('echo qna: stage ' + str(session['stage']))
						os.system('echo qna: power_history ' + str(session['power_history']))
						os.system('echo qna: error_history ' + str(session['error_history']))
						os.system('echo qna: bet_history ' + str(session['bet_history']))
						os.system('echo qna: reward_history ' + str(session['reward_history']))
						# os.system('echo qna: selections_history ' + str(session['selections_history']))
						os.system('echo qna: average ' + str(session['average_history']))
						os.system('echo qna: penalty ' + str(session['penalty_history']))
					return render_template(getResultTemplate(),
											 imagename=session['imagename'], \
											 power=session['power'], \
											 stage=session['stage'], \
											 old_power_history=session['old_power_history'], \
											 power_history=session['power_history'], \
											 error_history=session['error_history'], \
											 bet_history=session['bet_history'], \
											 reward_history=session['reward_history'], \
											 # selections_history=session['selections_history'], \
											 sessionid=session['sessionid'], \
											 gamedata_home_url=gamedata_home_url, \
											 max_round=max_round, \
											 average=session['average_history'], \
											 penalty=session['penalty_history'], \
										     uniq_code=session['uniq_code'], \
										     GAME_NAME=GAME_NAME)
				else:
					return render_template(getHtmlTemplate(), \
										 imagename=session['imagename'], \
										 power=session['power'], \
										 stage=session['stage'], \
										 question=session['question'], \
										 answers=session['answers'], \
										 sessionid=session['sessionid'], \
										 gamedata_home_url=gamedata_home_url, \
										 kernel_name=KERNEL_NAME, \
										 init_slider_value=error_rate, \
									     GAME_NAME=GAME_NAME)

			elif action == 'continue':
				os.system('echo continue')
				if len(session['power_history']) == session['stage']:
					session['stage'] = len(session['power_history']) + 1
					session['imagename'] = draw_qna_image_file()
					session['question'], session['correct_answer'], session['answers'] = get_qna(session['imagename'] + inext)
				return render_template(getHtmlTemplate(), \
										 imagename=session['imagename'], \
										 power=session['power'], \
										 stage=session['stage'], \
										 question=session['question'], \
										 answers=session['answers'], \
										 sessionid=session['sessionid'], \
										 gamedata_home_url=gamedata_home_url, \
									     kernel_name=KERNEL_NAME, \
									     init_slider_value='50', \
									     GAME_NAME=GAME_NAME)

			elif action == 'initialize':
				initialize()
				session['imagename'] = draw_qna_image_file()
				session['question'], session['correct_answer'], session['answers'] = get_qna(session['imagename'])
				return render_template(getHtmlTemplate(),
										 imagename=session['imagename'], \
										 power=session['power'], \
										 stage=session['stage'], \
										 question=session['question'], \
										 answers=session['answers'], \
										 sessionid=session['sessionid'], \
										 gamedata_home_url=gamedata_home_url, \
									     kernel_name=KERNEL_NAME, \
									     init_slider_value='50', \
									     GAME_NAME=GAME_NAME)

			elif action == 'finish':
				session.clear()
				return render_template('index.html', \
									   state=0, \
									   GAME_NAME=GAME_NAME)


def init_session():
	uid = uuid.uuid4()
	session['sessionid'] = str(uid)
	session['uniq_code'] = str(get_promo_code(10))
	store_session(session['userid'], session['sessionid'], session['uniq_code'])
	session['win'] = 0.0
	initialize()


def initialize():
	session['power'] = GAME3_INIT_ENERGY
	session['stage'] = 1
	session['old_power_history'] = []
	session['power_history'] = []
	session['error_history'] = []
	session['bet_history'] = []
	session['reward_history'] = []
	session['selections_history'] = []
	session['average_history'] = []
	session['penalty_history'] = []

def start_qna():
	init_session()

	inext, outext = getExtensions()
	session['imagename'] = draw_qna_image_file()
	session['question'], session['correct_answer'], session['answers'] = get_qna(session['imagename'] + inext)

	os.system('echo start_qna: ' + session['imagename'])
	return render_template(getHtmlTemplate(),
							 imagename=session['imagename'], \
							 power=session['power'], \
							 stage=session['stage'], \
							 question=session['question'], \
							 answers=session['answers'], \
							 sessionid=session['sessionid'], \
							 gamedata_home_url=gamedata_home_url, \
						     kernel_name=KERNEL_NAME, \
						     init_slider_value='50', \
						     GAME_NAME=GAME_NAME)
