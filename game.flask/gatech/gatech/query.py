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

def upload_files():

	debugMsg = 'uploading files done ...'

	if os.path.isfile(imagelist_file_path) == False:
		return 'Failed: there is no path [' + imagelist_file_path + ']'

	imageList = open(imagelist_file_path,'r')
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

		#i = Image(imagename, 6, 0, 0, selected_error_array, question, correct_answer, wrong_answers, selected_error_array)
		i = Image(imagename, 36, 0, 0, selected_error_array, question, correct_answer, wrong_answers, selected_error_array)
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

		# d = DegradedImage(imagename, error, 36, 1, 11, 5, 3, 9, 7, orgImageId)
		d = DegradedImage(imagename, error, 36, 10, 18, 5, 3, orgImageId)
		db_session.add(d)
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

def upload_files_old(orgpath, degpath, sblpath):
	debugMsg = 'uploading files done ...'

	# check if passed directoreis exist
	if os.path.isdir(orgpath) == False:
		return 'Failed: there is no path [' + orgpath + ']'
	if os.path.isdir(sblpath) == False:
		return 'Failed: there is no path [' + sblpath + ']'
	if os.path.isdir(degpath) == False:
		return 'Failed: there is no path [' + degpath + ']'

	# insert original image file with precisely sobel-filtered image
	imageList = os.popen('ls ' + orgpath + '|grep .png').readlines()
	questions = read_questions(orgpath)
	for image in imageList:
		imageFilename = image.strip('\n')
		if db_session.query(Image).filter_by(filename=imageFilename).count() != 0:
			continue
		with open(orgpath + '/' + imageFilename, 'rb') as f:
			imagedata = f.read()
		f.close()
		sblImageFilename = imageFilename.split('.png')[0] + '-sobel.png'
		if os.path.isfile(sblpath + '/' + sblImageFilename) == False:
			return 'Failed: there is no file [' + sblpath + '/' + sblImageFilename+ ']'
		with open(sblpath + '/' + sblImageFilename, 'rb') as f:
			sblImagedata = f.read()
		f.close()

		selected_error_array = ""
		for i in range(0, 50):
			selected_error_array = selected_error_array + "0|"
		selected_error_array = selected_error_array + str('0')

		question = questions[imageFilename][0]
		correct_answer = questions[imageFilename][1]
		wrong_answers = questions[imageFilename][2]
		os.system('echo upload_files: ' + question)
		os.system('echo upload_files: ' + correct_answer)
		os.system('echo upload_files: "' + wrong_answers + '"')
		#i = Image(imageFilename, imagedata, sblImagedata, 6, 0, 0, selected_error_array, question, correct_answer, wrong_answers, selected_error_array)
		i = Image(imageFilename, imagedata, sblImagedata, 36, 0, 0, selected_error_array, question, correct_answer, wrong_answers, selected_error_array)
		db_session.add(i)
		db_session.commit()

	# approximately sobel-filtered image file directory
	imageList = os.popen('ls ' + degpath).readlines()
	for image in imageList:
		imageFilename = image.strip('\n')
		if db_session.query(DegradedImage).filter_by(filename=imageFilename).count() != 0:
			continue
		with open(degpath + '/' + imageFilename, 'rb') as f:
			imagedata = f.read()
		f.close()
		tokens = imageFilename.strip('.png').split('_')
		error = float(tokens[1])
		orgImageFileName = tokens[0] + '.png'

		orgImageId = -1
		for result in db_session.query(Image).filter_by(filename=orgImageFileName):
			orgImageId = result.image_id
			break

#		d = DegradedImage(imageFilename, imagedata, error, 36, 1, 11, 5, 3, 9, 7, orgImageId)
		d = DegradedImage(imageFilename, imagedata, error, 36, 10, 18, 5, 3, orgImageId)
		db_session.add(d)
		db_session.commit()

	return debugMsg
