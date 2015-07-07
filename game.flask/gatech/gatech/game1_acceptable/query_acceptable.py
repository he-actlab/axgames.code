import os, random

from datetime import datetime, timedelta

from gatech import session
from gatech.database import db_session
from gatech.models import Image, DegradedImage, Play, PlaySession, ImageGallery, PlayGallery
from gatech.conf import drawn_errors, max_round, num_people_gallery, GAME1, wait_minutes_for_newplayer

def get_file_paths(drawnImageFilename, orgImageId):
	filePaths = []
	filePaths.append('/orgimage/' + drawnImageFilename + '.png')
	filePaths.append('/sobelimage/' + drawnImageFilename + '-sobel.png')

	minPlayed = 100000
	for error in drawn_errors:
		for tmpResult in db_session.query(DegradedImage).filter_by(org_image_id=orgImageId).filter_by(error=float(error)/100):
			if tmpResult.num_played < minPlayed:
				minPlayed = tmpResult.num_played
				candidates = []
				# os.system('echo candidate added cleared')
				candidates.append(tmpResult.imagename)
				# os.system('echo candidate added ' + str(tmpResult.imagename))
			elif tmpResult.num_played == minPlayed:
				candidates.append(tmpResult.imagename)
				# os.system('echo candidate added ' + str(tmpResult.imagename))
			break

	drawnImageFilename = random.choice(candidates)

	filePaths.append('/degimage/' + drawnImageFilename + '.png')
	os.system('echo getFilePaths: filePaths = ' + str(filePaths))
	return filePaths

def assign_newplayer_to_hung_gallery():
	#
	# Step 1: Find an image gallery that has been fully assigned but hasn't been finished by enough players. Assign a new player for the image gallery
	#
	for result in db_session.query(ImageGallery).filter_by(game_id=GAME1).filter_by(done=0).filter_by(num_assigned=num_people_gallery).order_by(ImageGallery.last_assignment):
		os.system('echo ig_id = ' + str(result.ig_id))
		waitedTime = datetime.now() - result.last_assignment
		os.system('echo time from last assignment to now = ' + str(waitedTime))
		if waitedTime < timedelta(minutes=wait_minutes_for_newplayer):
			os.system('echo ' + str(datetime.now() - result.last_assignment) + ' is smaller than ' + str(wait_minutes_for_newplayer))
		else:
			os.system('echo ' + str(datetime.now() - result.last_assignment) + ' is bigger than ' + str(wait_minutes_for_newplayer))
			os.system('echo reading from image_gallery table..')
			imageSetStr = result.image_set
			tokens = imageSetStr.split('|')
			filePathsList = []
			for token in tokens:
				orgImageId = int(token)
				image = db_session.query(Image).filter_by(image_id=orgImageId).first()
				drawnImageFilename = image.imagename

				filePaths = get_file_paths(drawnImageFilename, orgImageId)

				filePathsList.append(filePaths)
			newNum = result.num_assigned + 1
			db_session.query(ImageGallery).filter(ImageGallery.ig_id == result.ig_id).\
										update({"num_assigned": newNum})
			db_session.query(ImageGallery).filter(ImageGallery.ig_id == result.ig_id).\
										update({"last_assignment": datetime.now()})
			db_session.commit()
			os.system('echo over assigning a gallery to one more user..')
			return True, result.ig_id, filePathsList

	return False, -1, []

def assign_newplayer_to_available_gallery():
	#
	# Step 2: Try to find an image gallery that hasn't been assigned enough yet
	#
	for result in db_session.query(ImageGallery).filter_by(game_id=GAME1).order_by(ImageGallery.num_assigned):
		os.system('echo result.num_assigned = ' + str(result.num_assigned))
		os.system('echo num_people_gallery = ' + str(num_people_gallery))
		if result.num_assigned < num_people_gallery:
			os.system('echo reading from image_gallery table..')
			imageSetStr = result.image_set
			tokens = imageSetStr.split('|')
			filePathsList = []
			for token in tokens:
				orgImageId = int(token)
				image = db_session.query(Image).filter_by(image_id=orgImageId).first()
				drawnImageFilename = image.imagename

				filePaths = get_file_paths(drawnImageFilename, orgImageId)

				filePathsList.append(filePaths)
			newNum = result.num_assigned + 1
			os.system('echo result.ig_id = ' + str(result.ig_id))
			os.system('echo newNum = ' + str(newNum))
			db_session.query(ImageGallery).filter(ImageGallery.ig_id == result.ig_id).\
										update({"num_assigned": newNum})
			db_session.query(ImageGallery).filter(ImageGallery.ig_id == result.ig_id).\
										update({"last_assignment": datetime.now()})
			db_session.commit()
			return True, result.ig_id, filePathsList

	return False, -1, []

def create_new_gallery():
	#
	# Step 3: Create a new image gallery
	#
	length = max_round
	filePathsList = []
	orgImageIdSetStr = ''

	for result in db_session.query(Image).order_by(Image.num_played_game1):
		orgImageId = result.image_id
		orgImageIdSetStr += str(orgImageId)

		drawnImageFilename = result.imagename

		filePaths = get_file_paths(drawnImageFilename, orgImageId)
		filePathsList.append(filePaths)

		length = length - 1
		if length == 0:
			break

		orgImageIdSetStr += '|'

	ig = ImageGallery (GAME1, 1, 0, datetime.now(), orgImageIdSetStr, 0, "") # TODO - fix this
	db_session.add(ig)
	db_session.commit()

	return ig.ig_id, filePathsList

#
# webpage update - fetch random input image files from database and throw them to the game page
#
def draw_acceptable_image_files():
	os.system('echo draw_acceptable_image_files: start')

	#
	# Step 1
	#
	found, ig_id, filePathsList = assign_newplayer_to_hung_gallery()
	if found == True:
		return ig_id, filePathsList

	#
	# Step 2
	#
	assigned, ig_id, filePathsList = assign_newplayer_to_available_gallery()
	if assigned == True:
		return ig_id, filePathsList

	#
	# Step 3: Create a new image gallery
	#
	ig_id, filePathsList = create_new_gallery()

	os.system('echo draw_acceptable_image_files: end')
	return ig_id, filePathsList

def get_image_id(imagename):
	os.system('echo get_image_id: start')
	imagename = imagename.split('.png')[0]

	image_id = ''
	for result in db_session.query(Image).filter_by(imagename=imagename):
		image_id = result.image_id
		break
	return image_id

def get_degimage_id(imagename):
	os.system('echo get_degimage_id: stat')
	imagename = imagename.split('.png')[0]

	image_id = ''
	for result in db_session.query(DegradedImage).filter_by(imagename=imagename):
		image_id = result.deg_image_id
		break
	return image_id

def get_num_played(degImageId):
	for result in db_session.query(DegradedImage).filter_by(deg_image_id=degImageId):
		numPlayed = result.num_played
		break
	return numPlayed

def get_num_decision(degImageId, decision):
	for result in db_session.query(DegradedImage).filter_by(deg_image_id=degImageId):
		if decision == "agree":
			record = result.num_agree
		elif decision == "disagree":
			record = result.num_disagree
		break
	return record

def update_record(degImageId, decision):
	os.system('echo update_record start')
	for result in db_session.query(DegradedImage).filter_by(deg_image_id=degImageId):
		if decision == "agree":
			newNum = result.num_agree + 1
			db_session.query(DegradedImage).filter(DegradedImage.deg_image_id == degImageId).\
										update({"num_agree": newNum})
		elif decision == "disagree":
			newNum = result.num_disagree + 1
			db_session.query(DegradedImage).filter(DegradedImage.deg_image_id == degImageId).\
										update({"num_disagree": newNum})
		db_session.commit()

		# update num_played for degImage
		numPlayed = result.num_played + 1
		db_session.query(DegradedImage).filter(DegradedImage.deg_image_id == degImageId).\
										update({"num_played": numPlayed})
		db_session.commit()

		# update num_played for image
		for newresult in db_session.query(Image).filter_by(image_id=result.org_image_id):
			numPlayed = newresult.num_played_game1 + 1
			os.system('echo ' + str(numPlayed))
			db_session.query(Image).filter(Image.image_id == newresult.image_id).\
											update({"num_played_game1": numPlayed})
			db_session.commit()
			break
	os.system('echo update_record end')

def save_play(session_uuid, game_type, image_id, deg_imageid, decision, bet):
	os.system('echo save_play start')

	for result in db_session.query(PlaySession).filter_by(session_uuid=session_uuid):
		session_id = result.session_id
		break

	if decision == "agree":
		selnum = 0
	elif decision == "disagree":
		selnum = 1

	p = Play(int(session_id), int(game_type), int(image_id), int(deg_imageid), int(selnum), int(bet), 0, 0, 0, 0, 0)
	db_session.add(p)
	db_session.commit()

	os.system('echo save_play end')

	return p.play_id

def save_play_gallery(ig_id, session_uuid, play_id_list):

	os.system('echo save_play_gallery start')

	for result in db_session.query(PlaySession).filter_by(session_uuid=session_uuid):
		session_id = result.session_id
		break

	play_id_list_str = ''
	for play_id in play_id_list:
		play_id_list_str += str(play_id)
		if play_id == play_id_list[len(play_id_list)-1]:
			break
		play_id_list_str += '|'

	pg = PlayGallery (ig_id, session_id, play_id_list_str)
	db_session.add(pg)

	ig = db_session.query(ImageGallery).filter_by(ig_id=ig_id).first()
	newNumCompleted = ig.num_completed + 1
	db_session.query(ImageGallery).filter(ImageGallery.ig_id == ig_id).\
										update({"num_completed": newNumCompleted})

	if newNumCompleted ==ig.num_assigned:
		db_session.query(ImageGallery).filter(ImageGallery.ig_id == ig_id).\
										update({"done": 1})

	db_session.commit()

	os.system('echo save_play_gallery end')
