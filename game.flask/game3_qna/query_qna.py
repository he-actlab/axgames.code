import os, random

from gatech import session
from gatech.database import db_session
from gatech.models import Image, PlaySession, Play
from gatech.conf import ERROR_MAX, APPLICATION_TYPE

import sys

def getHtmlTemplate():
	if APPLICATION_TYPE == 'IP':
		return 'play_qna_ip.html'
	elif APPLICATION_TYPE == 'OCR':
		return 'play_qna_ocr.html'
	elif APPLICATION_TYPE == 'SR':
		return 'play_qna_sr.html'
	elif APPLICATION_TYPE == 'AE':
		return 'play_qna_ae.html'
	else:
		print 'Error: unknown applicaiton type'
		sys.exit()

def get_selections(imagename):

	imagename = imagename.split('.')[0]

	for result in db_session.query(Image).filter_by(imagename=imagename):
		selected_error_array = result.selected_error_array_game3
		break
	tokens = selected_error_array.split('|')
	selections = []
	for i in range(0, len(tokens)):
		selections.append(int(tokens[i].encode("ascii")))
	return selections

def get_history(imagename):
	imagename = imagename.split('.')[0]

	result = db_session.query(Image).filter_by(imagename=imagename).first()
	tokens = result.game3_history.split('|')
	history = []
	for token in tokens:
		pair = token.strip('[').strip(']').split(',')
		nAgree = pair[0]
		nPlayed = pair[1]
		history.append([int(nAgree), int(nPlayed)])

	os.system('echo get_history end')

	return history

def update_history(imagename, error):
	oldHistory = db_session.query(Image).filter_by(imagename=imagename).first().game3_history

	newHistory = ""
	e = 1
	histories = oldHistory.split('|')
	for h in histories:
		tokens = h.split(',')
		if e <= error:
			numAgree = int(tokens[0]) + 1
		else:
			numAgree = int(tokens[0])
		numPlayed = int(tokens[1]) + 1
		newHistory += str(numAgree) + ',' + str(numPlayed)
		if e != ERROR_MAX:
			newHistory += '|'
		e += 1

	db_session.query(Image).filter(Image.imagename == imagename).update({"game3_history": newHistory})
	db_session.commit()

def update_qna_record (imagename, selection, selections):

	imagename = imagename.split('.')[0]
	selections[selection] += 1

	os.system('echo update_qna_record: ' + str(selections))
	newSelections = ""
	for i in range(0, len(selections)-1):
		newSelections = newSelections + str(selections[i]) + "|"
	newSelections = newSelections + str(selections[len(selections)-1])

	result = db_session.query(Image).filter_by(imagename=imagename).first()
	num_played_game3 = result.num_played_game3
	db_session.query(Image).filter(Image.imagename == imagename).update({"selected_error_array_game3": newSelections})
	db_session.query(Image).filter(Image.imagename == imagename).update({"num_played_game3": num_played_game3 + 1})
	db_session.commit()

	update_history(imagename, selection)

def get_image_id(imagename):
	os.system('echo get_image_id ' + imagename)
	for result in db_session.query(Image).filter_by(imagename=imagename):
		image_id = result.image_id
		break
	return image_id

def save_play(session_uuid, game_type, imagename, error_rate, bet, incorrect, winning):
	os.system('echo save_play start')

	for result in db_session.query(PlaySession).filter_by(session_uuid=session_uuid):
		session_id = result.session_id
		break

	if incorrect == True:
		incnum = 1
	else:
		incnum = 0

	cnt = 0
	for temp in db_session.query(Play).filter_by(session_id=session_id).filter_by(game_type=game_type).filter_by(image_id=get_image_id(imagename)):
		cnt += 1

	if cnt != 0:
		os.system('echo save_play false')
		return False

	p = Play(int(session_id), int(game_type), int(get_image_id(imagename)), 1, 0, 0, 0.0, 0, 0, 0.0, int(incnum), int(error_rate), int(bet), float(winning))
	db_session.add(p)
	db_session.commit()

	os.system('echo save_play end')
	return True

def draw_qna_image_file():
	minNumPlayed = db_session.query(Image).order_by(Image.num_played_game3).first().num_played_game3
	images = []
	for result in db_session.query(Image).filter_by(num_played_game3=minNumPlayed):
		images.append((result.image_id, result.imagename))
	random.shuffle(images)
	imagename = ""
	for image in images:
		imagename = image[1]
		break
	return imagename


def get_qna(imagename):

	os.system('echo get_qna start')

	imagename = imagename.split('.')[0]
	os.system('echo get_qna: imagename = ' + imagename)

	for result in db_session.query(Image).filter_by(imagename=imagename):
		question = result.question
		correct_answer = result.correct_answer
		wrong_answers = ((result.wrong_answers).split('|'))
		num_answers = len(wrong_answers) + 1
		num_correct_answer = int(random.random() * num_answers)
		answers = []
		j = 0
		for i in range(0, num_answers):
			if i == num_correct_answer:
				answers.append(correct_answer.encode("ascii"))
			else:
				answers.append(wrong_answers[j].encode("ascii"))
				j += 1
		break

	os.system('echo get_qna end')

	return question, correct_answer, answers




