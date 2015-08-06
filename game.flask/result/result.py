#!/bin/env python

from gatech import app

from flask import render_template
from gatech.conf import GAME_NAME
from query_result import get_org_images, get_deg_images, get_admin_sessions, get_plays, get_degimage, get_bad_users, get_bad_plays
from gatech.conf import drawn_errors, KERNEL_NAME, GAME2_BADPLAY_THRESHOLD, ERROR_MAX

import os

@app.route("/statistics_game1")
def statistics_game1():

	game1NumPlayed = {}
	game1NumAgreed = {}

	for err in range(1,100):
		game1NumPlayed[float(err) / 100.0] = 0
		game1NumAgreed[float(err) / 100.0] = 0

	for entry in get_deg_images():
		game1NumPlayed[entry.error] += entry.num_played - (entry.org_num_agree + entry.org_num_disagree)
		game1NumAgreed[entry.error] += entry.num_agree - entry.org_num_agree

	for asession in get_admin_sessions():
		sid = asession.session_id
		for play in get_plays(sid, 0):
			degimage = get_degimage(play.deg_image_id)
			err = degimage.error
			game1NumPlayed[err] -= 1
			if play.selection == 0:
				game1NumAgreed[err] -= 1

	keys = []
	for err in drawn_errors:
		keys.append(float(err) / 100.0)

	stat_filename = KERNEL_NAME + "_statistics_game1.csv"
	with open(os.path.dirname(__file__) + "/../static/temp/" + stat_filename,"w") as f:
		f.write('error,num_agreed,num_played\n')
		for key in keys:
			f.write(str(key) + ',' + str(game1NumAgreed[key]) + ',' + str(game1NumPlayed[key]) + '\n')
	f.close()

	return render_template('statistics_game1.html', \
						   keys=keys, \
						   game1NumPlayed=game1NumPlayed, \
						   game1NumAgreed=game1NumAgreed, \
						   stat_filename=stat_filename, \
						   GAME_NAME=GAME_NAME)

@app.route("/statistics_game2")
def statistics_game2():

	game2NumPlayed = []
	game2NumAgreed = []

	for i in range(1, 51):
		game2NumPlayed.append(0)
		game2NumAgreed.append(0)

	for org_image in get_org_images():
		history = org_image.game2_history
		records = history.split('|')
		index = 0
		for rec in records:
			nums = rec.split(',')
			game2NumPlayed[index] += int(nums[1])
			game2NumAgreed[index] += int(nums[0])
			index += 1

	for asession in get_admin_sessions():
		sid = asession.session_id
		for play in get_plays(sid, 0):
			error_rate = get_degimage(play.deg_image_id).error
			decision = play.selection
			game2NumPlayed, game2NumAgreed = remove_game1_plays(game2NumPlayed, game2NumAgreed, int(error_rate * 100), decision)
		for play in get_plays(sid, 1):
			error_rate = play.error_rate_game2
			for i in range(1, 51):
				game2NumPlayed[i-1] -= 1
				if i <= error_rate:
					game2NumAgreed[i-1] -= 1

	stat_filename = KERNEL_NAME + "_statistics_game2.csv"
	with open(os.path.dirname(__file__) + "/../static/temp/" + stat_filename,"w") as f:
		f.write('error,num_agreed,num_played\n')
		for key in range(1, 51):
			f.write(str(key) + ',' + str(game2NumAgreed[key-1]) + ',' + str(game2NumPlayed[key-1]) + '\n')
	f.close()

	return render_template('statistics_game2.html', \
						   keys=range(1,51), \
						   game2NumAgreed=game2NumAgreed, \
						   game2NumPlayed=game2NumPlayed, \
						   stat_filename=stat_filename, \
						   GAME_NAME=GAME_NAME)

@app.route("/statistics_game2_excluded")
def statistics_game2_excluded():

	game2NumPlayed = []
	game2NumAgreed = []

	for i in range(0, 50):
		game2NumPlayed.append(0)
		game2NumAgreed.append(0)

	# collecting and merging all the statistics from all images
	for org_image in get_org_images():
		history = org_image.game2_history
		records = history.split('|')
		index = 0
		for rec in records:
			nums = rec.split(',')
			game2NumPlayed[index] += int(nums[1])
			game2NumAgreed[index] += int(nums[0])
			index += 1

	# deleting statistics produced by admin accounts (1~100)
	for asession in get_admin_sessions():
		sid = asession.session_id
		for play in get_plays(sid, 0):
			error_rate = get_degimage(play.deg_image_id).error
			decision = play.selection
			game2NumPlayed, game2NumAgreed = remove_game1_plays(game2NumPlayed, game2NumAgreed, int(error_rate * 100), decision)
		for play in get_plays(sid, 1):
			error_rate = play.error_rate_game2
			for i in range(1, 51):
				game2NumPlayed[i-1] -= 1
				if i <= error_rate:
					game2NumAgreed[i-1] -= 1

	# exluding bad game2 plays
	busers = set()
	for bu in get_bad_users(1, GAME2_BADPLAY_THRESHOLD):
		if bu.user_id in busers:
			continue
		elif bu.user_id >=1 and bu.user_id <= 100:
			continue
		else:
			busers.add(bu.user_id)
			for bp in get_bad_plays(bu.user_id, 1):
				error_rate = bp.error_rate_game2
				for i in range(0, 50):
					game2NumPlayed[i] -= 1
					if i < error_rate:
						game2NumAgreed[i] -= 1

	# exluding bad game1 plays
	busers = set()
	for bu in get_bad_users(0, GAME2_BADPLAY_THRESHOLD):
		if bu.user_id in busers:
			continue
		elif bu.user_id >=1 and bu.user_id <= 100:
			continue
		else:
			busers.add(bu.user_id)
			for bp in get_bad_plays(bu.user_id, 0):
				error_rate = get_degimage(bp.deg_image_id).error
				decision = bp.selection
				game2NumPlayed, game2NumAgreed = remove_game1_plays(game2NumPlayed, game2NumAgreed, int(error_rate * 100), decision)

	stat_filename = KERNEL_NAME + "_statistics_game2_excluded.csv"
	with open(os.path.dirname(__file__) + "/../static/temp/" + stat_filename,"w") as f:
		f.write('error,num_agreed,num_played\n')
		for key in range(1, 51):
			f.write(str(key) + ',' + str(game2NumAgreed[key-1]) + ',' + str(game2NumPlayed[key-1]) + '\n')
	f.close()

	return render_template('statistics_game2.html', \
						   keys=range(1,51), \
						   game2NumAgreed=game2NumAgreed, \
						   game2NumPlayed=game2NumPlayed, \
						   stat_filename=stat_filename, \
						   GAME_NAME=GAME_NAME)

def remove_game1_plays(numPlayed, numAgreed, error, decision):
	preError = 0
	nxtError = ERROR_MAX
	for i in range(0, len(drawn_errors)):
		if drawn_errors[i] < error:
			preError = drawn_errors[i]
		if drawn_errors[i] >= error:
			nxtError = drawn_errors[i]
			break
	for e in range(1, ERROR_MAX + 1):
		if e > preError and e <= nxtError:
			if decision == 0:
				numAgreed[e - 1] -= 1
			numPlayed[e - 1] -= 1
	return numPlayed, numAgreed

@app.route("/statistics_game3")
def statistics_game3():

	game3NumPlayed = []
	game3NumAgreed = []

	for i in range(1, 51):
		game3NumPlayed.append(0)
		game3NumAgreed.append(0)

	for org_image in get_org_images():
		history = org_image.game3_history
		records = history.split('|')
		index = 0
		for rec in records:
			nums = rec.split(',')
			game3NumPlayed[index] += int(nums[1])
			game3NumAgreed[index] += int(nums[0])
			index += 1

	for asession in get_admin_sessions():
		sid = asession.session_id
		for play in get_plays(sid, 2):
			error_rate = play.error_rate_game3
			for i in range(0, 50):
				game3NumPlayed[i] -= 1
				if i < error_rate:
					game3NumAgreed[i] -= 1

	stat_filename = KERNEL_NAME + "_statistics_game3.csv"
	with open(os.path.dirname(__file__) + "/../static/temp/" + stat_filename,"w") as f:
		f.write('error,num_agreed,num_played\n')
		for key in range(1, 51):
			f.write(str(key) + ',' + str(game3NumAgreed[key-1]) + ',' + str(game3NumPlayed[key-1]) + '\n')
	f.close()

	return render_template('statistics_game3.html', \
						   keys=range(1,51), \
						   game3NumAgreed=game3NumAgreed, \
						   game3NumPlayed=game3NumPlayed, \
						   stat_filename=stat_filename, \
						   GAME_NAME=GAME_NAME)