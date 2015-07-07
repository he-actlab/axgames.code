import os, random

from gatech.database import db_session
from gatech.models import Image, DegradedImage, User, PlaySession
from conf import imagelist_file_path, question_file_path, degimagelist_file_path


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
	if error <= 0.01:
		return 10, 0
	elif error <= 0.03:
		return 9, 1
	elif error <= 0.05:
		return 8, 2
	elif error <= 0.1:
		return 5, 5
	elif error <= 0.2:
		return 2, 8
	elif error <= 0.4:
		return 1, 9
	elif error <= 0.5:
		return 0, 10

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
		for i in range(0, 50):
			selected_error_array = selected_error_array + "0|"
		selected_error_array = selected_error_array + str('0')

		question = questions[imagename][0]
		os.system('echo upload_files: ' + question)

		correct_answer = questions[imagename][1]
		os.system('echo upload_files: ' + correct_answer)

		wrong_answers = questions[imagename][2]
		os.system('echo upload_files: "' + wrong_answers + '"')

		# i = Image(imagename, 6, 0, 0, selected_error_array, question, correct_answer, wrong_answers, selected_error_array)
		i = Image(imagename, 2, 0, 0, selected_error_array, question, correct_answer, wrong_answers, selected_error_array)
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
		d = DegradedImage(imagename, error, agree + disagree, agree, disagree, orgImageId)
		db_session.add(d)
		db_session.commit()

	# debug
	user = User("12", "12")
	db_session.add(user)
	db_session.commit()

	return debugMsg


def store_session(username, session_uuid):
	os.system('echo store_session start')

	for result in db_session.query(User).filter_by(username=username):
		user_id = result.user_id
		break

	s = PlaySession(session_uuid, user_id)
	db_session.add(s)
	db_session.commit()

	os.system('echo store_session end')