import os, random

from gatech.database import db_session
from gatech.models import Image, DegradedImage, User, PlaySession
from conf import imagelist_file_path, question_file_path, degimagelist_file_path, GAME1_INIT_NUM_PLAYED
from conf import drawn_errors, APPLICATION_TYPE
from conf import ERROR_MAX, ERROR_MIN, ERROR_INT

import sys

def getExtensions():
	if APPLICATION_TYPE == "IP":
		inext = ".png"
		outext = ".png"
	elif APPLICATION_TYPE == "OCR":
		inext = ".jpg"
		outext = ".html"
	elif APPLICATION_TYPE == "SR":
		inext = ".wav"
		outext = ".html"
	elif APPLICATION_TYPE == "AE":
		inext = ".wav"
		outext = ".mp3"
	else:
		os.system("Error: unknown application type")
		sys.exit()
	return inext, outext

def doLogin(username, password):
	if db_session.query(User).count() != 0 and db_session.query(User).filter_by(username=username).count() != 0:
		os.system('echo doLogin1')
		user = db_session.query(User).filter_by(username=username).first()
		os.system('echo doLogin2')
		if user.password == password:
			os.system('echo doLogin3')
			return True
		else:
			os.system('echo doLogin4')
			return False
	else:
		return False


def add_user(username, password):
	os.system('echo add_user: username ' + username)
	os.system('echo add_user: password ' + password)

	if db_session.query(User).count() != 0 and db_session.query(User).filter_by(username=username).count() != 0:
		return False
	else:
		user = User(username, password)
		db_session.add(user)
		db_session.commit()

	return True


def read_questions(question_file_path):
	questions = {}
	with open(question_file_path, 'r') as q:
		lines = q.readlines()
		for line in lines:
			tokens = line.strip('\n').split(',')
			os.system('echo read_questions: tokens - ' + str(tokens))
			filename = tokens[0]
			question = tokens[1]
			correct_answer = tokens[2]
			wrong_answers = ""
			for i in range(3, len(tokens) - 1):
				wrong_answers += tokens[i] + '|'
			wrong_answers += tokens[len(tokens) - 1]
			os.system('echo read_questions: filename [' + filename + ']')
			os.system('echo read_questions: question ' + question)
			os.system('echo read_questions: correct ' + correct_answer)
			os.system('echo read_questions: wrong "' + wrong_answers + '"')
			questions[filename] = [question, correct_answer, wrong_answers]
			os.system('echo read_questions: triple "' + str(questions[filename]) + '"')
	q.close()

	return questions


#
# TODO - temporary mechanism (must be improved)
#
def initial_consensus(error):
	os.system('echo error = ' + str(error))
	# if APPLICATION_TYPE != 'AE':
	# 	if error <= drawn_errors[0] / 100.0:
	# 		agree = (GAME1_INIT_NUM_PLAYED - 5) + random.randint(0,5)
	# 	elif error <= drawn_errors[1] / 100.0:
	# 		agree = (GAME1_INIT_NUM_PLAYED - 15) + random.randint(0,10)
	# 	elif error <= drawn_errors[2] / 100.0:
	# 		agree = (GAME1_INIT_NUM_PLAYED - 25) + random.randint(0,10)
	# 	elif error <= drawn_errors[3] / 100.0:
	# 		agree = (GAME1_INIT_NUM_PLAYED - 35) + random.randint(0,10)
	# 	elif error <= drawn_errors[4] / 100.0:
	# 		agree = (GAME1_INIT_NUM_PLAYED - 45) + random.randint(0,10)
	# 	elif error <= drawn_errors[5] / 100.0:
	# 		agree = (GAME1_INIT_NUM_PLAYED - 55) + random.randint(0,10)
	# 	elif error <= drawn_errors[6] / 100.0:
	# 		agree = (GAME1_INIT_NUM_PLAYED - 65) + random.randint(0,10)
	# 	elif error <= drawn_errors[7] / 100.0:
	# 		agree = (GAME1_INIT_NUM_PLAYED - 85) + random.randint(0,10)
	# 	elif error <= drawn_errors[8] / 100.0:
	# 		agree = (GAME1_INIT_NUM_PLAYED - 95) + random.randint(0,10)
	# 	elif error <= drawn_errors[9] / 100.0:
	# 		agree = 0 + random.randint(0,5)
	# 	else:
	# 		os.system('echo Error: unknown error')
	# 		sys.exit()
	# else:
	# 	if error <= drawn_errors[0] / 100.0:
	# 		agree = 0 + random.randint(0,5)
	# 	elif error <= drawn_errors[1] / 100.0:
	# 		agree = (GAME1_INIT_NUM_PLAYED - 95) + random.randint(0,10)
	# 	elif error <= drawn_errors[2] / 100.0:
	# 		agree = (GAME1_INIT_NUM_PLAYED - 80) + random.randint(0,10)
	# 	elif error <= drawn_errors[3] / 100.0:
	# 		agree = (GAME1_INIT_NUM_PLAYED - 50) + random.randint(0,10)
	# 	elif error <= drawn_errors[4] / 100.0:
	# 		agree = (GAME1_INIT_NUM_PLAYED - 30) + random.randint(0,10)
	# 	elif error <= drawn_errors[5] / 100.0:
	# 		agree = (GAME1_INIT_NUM_PLAYED - 25) + random.randint(0,10)
	# 	elif error <= drawn_errors[6] / 100.0:
	# 		agree = (GAME1_INIT_NUM_PLAYED - 20) + random.randint(0,10)
	# 	elif error <= drawn_errors[7] / 100.0:
	# 		agree = (GAME1_INIT_NUM_PLAYED - 15) + random.randint(0,10)
	# 	elif error <= drawn_errors[8] / 100.0:
	# 		agree = (GAME1_INIT_NUM_PLAYED - 10) + random.randint(0,10)
	# 	elif error <= drawn_errors[9] / 100.0:
	# 		agree = (GAME1_INIT_NUM_PLAYED - 5) + random.randint(0,5)
	# 	else:
	# 		os.system('echo Error: unknown error')
	# 		sys.exit()
	agree = random.randint(0, 100)
	return agree, GAME1_INIT_NUM_PLAYED - agree

def upload_files():
	debugMsg = 'uploading files done ...'

	if os.path.isfile(imagelist_file_path) == False:
		return 'Failed: there is no path [' + imagelist_file_path + ']'

	imageList = open(imagelist_file_path, 'r')
	questions = read_questions(question_file_path)
	for imagename in imageList.readlines():
		os.system('echo imagename = ' + imagename)
		imagename = imagename.strip('\n').split()[0]

		if db_session.query(Image).filter_by(imagename=imagename).count() != 0:
			continue

		selected_error_array = ""
		for i in range(ERROR_MIN, ERROR_MAX, ERROR_INT):
			selected_error_array = selected_error_array + "0|"
		selected_error_array = selected_error_array + str('0')

		history = ""
		for i in range(ERROR_MIN, ERROR_MAX-ERROR_INT, ERROR_INT):
			history = history + "0,0|"
		history = history + str('0,0')

		question = questions[imagename][0]
		os.system('echo upload_files: ' + question)

		correct_answer = questions[imagename][1]
		os.system('echo upload_files: ' + correct_answer)

		wrong_answers = questions[imagename][2]
		os.system('echo upload_files: "' + wrong_answers + '"')

		i = Image(imagename, GAME1_INIT_NUM_PLAYED, 0, 0, selected_error_array, question, correct_answer, wrong_answers, selected_error_array, history, history)
		db_session.add(i)
		db_session.commit()

	degImageList = open(degimagelist_file_path, 'r')
	for imagename in degImageList.readlines():
		imagename = imagename.strip('\n')

		if db_session.query(DegradedImage).filter_by(imagename=imagename).count() != 0:
			continue

		tokens = imagename.split('_')
		error = float(tokens[1])
		orgimagename = tokens[0]

		orgImageId = -1
		for result in db_session.query(Image).filter_by(imagename=orgimagename):
			orgImageId = result.image_id
			break

		agree, disagree = initial_consensus(error)
		d = DegradedImage(imagename, error, agree + disagree, agree, disagree, agree, disagree, orgImageId)
		db_session.add(d)
		db_session.commit()

	# debug
	debug_add_user()

	return debugMsg

def debug_add_user():
	for i in range(0, 100):
		user = User(str(i), str(i))
		db_session.add(user)
	db_session.commit()

def get_user_id (username):
	result = db_session.query(User).filter_by(username=username).first()
	return result.user_id

def get_promo_code(num_chars):
	code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	code = ''
	for i in range(0, num_chars):
		slice_start = random.randint(0, len(code_chars) - 1)
		code += code_chars[slice_start: slice_start + 1]
	return code

def store_session(user_id, session_uuid, uniq_code):
	os.system('echo store_session start')

	s = PlaySession(session_uuid, user_id, uniq_code)
	db_session.add(s)
	db_session.commit()

	os.system('echo store_session end')

# test
