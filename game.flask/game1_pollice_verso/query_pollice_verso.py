import os, random

from datetime import datetime, timedelta

from gatech import session
from gatech.database import db_session
from gatech.models import Image, DegradedImage, Play, PlaySession, ImageGallery, PlayGallery, BadPlayGallery
from gatech.conf import drawn_errors, max_round, num_people_gallery, GAME1, wait_minutes_for_newplayer, fleiss_kappa_threshold
from gatech.conf import ERROR_MAX, GAME1_GALLERY_ASSIGN_INTERVAL, KERNEL_NAME, APPLICATION_TYPE
from gatech.query import getExtensions
from gatech.analysis.fleiss import fleiss_kappa
from gatech.analysis.combination import get_combination

import os, sys

def getHtmlTemplate():
	if APPLICATION_TYPE == 'IP':
		return 'play_pollice_verso_ip.html'
	elif APPLICATION_TYPE == 'OCR':
		return 'play_pollice_verso_ocr.html'
	elif APPLICATION_TYPE == 'SR':
		return 'play_pollice_verso_sr.html'
	elif APPLICATION_TYPE == 'AE':
		return 'play_pollice_verso_ae.html'
	else:
		print 'Error: unknown applicaiton type'
		sys.exit()

def getResultTemplate():
	if APPLICATION_TYPE == 'IP':
		return 'result_pollice_verso_ip.html'
	elif APPLICATION_TYPE == 'OCR':
		return 'result_pollice_verso_ocr.html'
	elif APPLICATION_TYPE == 'SR':
		return 'result_pollice_verso_sr.html'
	elif APPLICATION_TYPE == 'AE':
		return 'result_pollice_verso_ae.html'
	else:
		print 'Error: unknown applicaiton type'
		sys.exit()


def get_file_paths(drawnImageFilename, orgImageId):
	filePaths = []
	inext, outext = getExtensions()
	filePaths.append('/orgimage/' + drawnImageFilename + inext)
	filePaths.append('/sobelimage/' + drawnImageFilename + '-' + KERNEL_NAME + outext)

	minPlayed = 100000
	for error in drawn_errors:
		tmpResult = db_session.query(DegradedImage).filter_by(org_image_id=orgImageId).filter_by(error=float(error)/100).first()
		if tmpResult.num_played < minPlayed:
			minPlayed = tmpResult.num_played
			candidates = []
			candidates.append(tmpResult.imagename)
		elif tmpResult.num_played == minPlayed:
			candidates.append(tmpResult.imagename)

	drawnImageFilename = random.choice(candidates)
	degImageId = db_session.query(DegradedImage).filter_by(imagename=drawnImageFilename).first().deg_image_id

	inext, outext = getExtensions()
	filePaths.append('/degimage/' + drawnImageFilename + outext)
	os.system('echo getFilePaths: filePaths = ' + str(filePaths))
	return filePaths, degImageId

def assign_newplayer(userId, igId, degImageSetStr, numAssigned, playedUsers, isWaited):
	# Assign a new player again
	tokens = degImageSetStr.split('|')
	filePathsList = []
	for token in tokens:
		degImageId = int(token)
		degImage = db_session.query(DegradedImage).filter_by(deg_image_id=degImageId).first()
		degImageName = degImage.imagename
		orgImageName = db_session.query(Image).filter_by(image_id=degImage.org_image_id).first().imagename

		filePaths = []
		inext, outext = getExtensions()
		filePaths.append('/orgimage/' + orgImageName + inext)
		filePaths.append('/sobelimage/' + orgImageName + '-' + KERNEL_NAME + outext)
		filePaths.append('/degimage/' + degImageName + outext)
		filePathsList.append(filePaths)

	os.system('echo filePaths(assign_newplayer) = "' + str(filePaths) + '"')

	# update num_assigned
	if isWaited == True:
		newNum = numAssigned
	else:
		newNum = numAssigned + 1
	db_session.query(ImageGallery).filter(ImageGallery.ig_id == igId).\
								update({"num_assigned": newNum})
	# update last_assignment
	db_session.query(ImageGallery).filter(ImageGallery.ig_id == igId).\
								update({"last_assignment": datetime.now()})
	# update played_users
	played_users = playedUsers + '|' + str(userId)
	db_session.query(ImageGallery).filter(ImageGallery.ig_id == igId).\
								update({"played_users": played_users})
	db_session.commit()

	return filePathsList

def handle_agreed(records, pgList):
	os.system('echo records = "' + str(records) + '"')
	badPgs = []
	for pg in pgList:
		badPgs.append(pg)
	for record in records:
		fk = (record.values())[0]
		os.system('echo fk = ' + str(fk))
		if fk > fleiss_kappa_threshold:
			for pgIndex in (record.keys())[0].strip('[').strip(']').split(','):
				os.system('echo good pgIndex = ' + str(pgIndex))
				pg = pgList[int(pgIndex)]
				badPgs.remove(pg)

	for badpg in badPgs:
		badFk = ""
		goodFk = ""
		cnt = 0
		for record in records:
			os.system('echo cnt = ' + str(cnt))
			cnt += 1
			isBad = False
			for pgIndex in (record.keys())[0].strip('[').strip(']').split(','):
				if badpg == pgList[int(pgIndex)]:
					badFk += str(record.values()[0]) + '|'
					isBad = True
					break
			if isBad == False and record.values()[0] > fleiss_kappa_threshold:
				goodFk += str(record.values()[0]) + '|'

		bpg = BadPlayGallery(badpg.pg_id, badFk, goodFk)
		db_session.add(bpg)
		db_session.commit()

def assign_newplayer_to_low_agreement(userId):
	os.system('echo assign_newplayer_to_low_agreement start')
	#
	# Step 1: If the agreement level is low, add another user to this gallery
	#
	for result in db_session.query(ImageGallery).filter_by(game_id=GAME1).filter_by(done=1).filter_by(agreed=0).order_by(ImageGallery.last_assignment):
		# if this play has already played this gallery, skip it
		playedUsers = result.played_users.split('|')
		if str(userId) in playedUsers:
			continue

		if result.num_assigned == result.num_completed:
			isAgreed = False
			pgList = db_session.query(PlayGallery).filter_by(ig_id=result.ig_id)
			for groupNum in range(result.num_assigned, 1, -1):
				groupRecords = []
				maxFleissKappa = -10.0
				combinations = get_combination(range(0, result.num_assigned), result.num_assigned, groupNum)
				for group in combinations:
					os.system('echo group = ' + str(group))
					table = []
					for i in range(0, max_round):
						table.append([0,0])
					for pgIndex in group:
						pg = pgList[pgIndex]
						playIdList = pg.play_id_list.split('|')
						for i in range(0, max_round):
							playId = playIdList[i]
							selection = db_session.query(Play).filter_by(play_id=int(playId)).first().selection
							if selection == 0:
								table[i][0] += 1
							else:
								table[i][1] += 1
					fk = fleiss_kappa(max_round, groupNum, 2, table)
					groupRecords.append({str(group): fk})
					if fk > maxFleissKappa:
						maxFleissKappa = fk

				if maxFleissKappa > fleiss_kappa_threshold:
					handle_agreed(groupRecords, pgList)
					isAgreed = True
					break

			if isAgreed == False:
				filePathsList = assign_newplayer(userId, result.ig_id, result.deg_image_set, result.num_assigned, result.played_users, False)
				return True, result.ig_id, filePathsList
			else:
				db_session.query(ImageGallery).filter(ImageGallery.ig_id == result.ig_id).update({"agreed": 1})
				db_session.commit()
		else:
			assert(result.num_assigned > result.num_completed)

			waitedTime = datetime.now() - result.last_assignment
			os.system('echo waitedTime => ' + str(waitedTime))
			if waitedTime > timedelta(minutes=wait_minutes_for_newplayer):
				filePathsList = assign_newplayer(userId, result.ig_id, result.deg_image_set, result.num_assigned, result.played_users, True)
				return True, result.ig_id, filePathsList

	return False, -1, []

def assign_newplayer_to_hung_gallery(userId):
	os.system('echo assign_newplayer_to_hung_gallery start')
	#
	# Step 2: Find an image gallery that has been fully assigned but hasn't been finished by enough players. Assign a new player for the image gallery
	#
	for result in db_session.query(ImageGallery).filter_by(game_id=GAME1).filter_by(done=0).order_by(ImageGallery.last_assignment):
		# if this play has already played this gallery, skip it
		playedUsers = result.played_users
		tokens = playedUsers.split('|')
		if str(userId) in tokens:
			continue

		os.system('echo ig_id = ' + str(result.ig_id))
		waitedTime = datetime.now() - result.last_assignment
		os.system('echo time from last assignment to now = ' + str(waitedTime))
		if result.num_assigned > result.num_completed:
			if waitedTime > timedelta(minutes=wait_minutes_for_newplayer):
				filePathsList = assign_newplayer(userId, result.ig_id, result.deg_image_set, result.num_assigned, result.played_users, True)
				return True, result.ig_id, filePathsList
			else:
				os.system('echo ' + str(datetime.now() - result.last_assignment) + ' is smaller than ' + str(wait_minutes_for_newplayer))

	return False, -1, []

def assign_newplayer_to_available_gallery(userId):
	os.system('echo assign_newplayer_to_available_gallery start')
	#
	# Step 3: Try to find an image gallery that hasn't been assigned enough yet
	#
	for result in db_session.query(ImageGallery).filter_by(game_id=GAME1).order_by(ImageGallery.num_assigned):
		# if this player has already played this gallery, skip it
		playedUsers = result.played_users.split('|')
		if str(userId) in playedUsers:
			continue
		os.system('echo result.num_assigned = ' + str(result.num_assigned))
		os.system('echo num_people_gallery = ' + str(num_people_gallery))
		waitedTime = datetime.now() - result.last_assignment
		os.system('echo waitedTime => ' + str(waitedTime))
		if waitedTime < timedelta(minutes=GAME1_GALLERY_ASSIGN_INTERVAL):
			continue
		if result.num_assigned < num_people_gallery:
			filePathsList = assign_newplayer(userId, result.ig_id, result.deg_image_set, result.num_assigned, result.played_users, False)
			return True, result.ig_id, filePathsList

	return False, -1, []

def create_new_gallery(userId):
	os.system('echo create_new_gallery start')
	#
	# Step 4: Create a new image gallery todo - should mix low and high error images in an image gallery
	#
	length = max_round
	filePathsList = []
	orgImageIdSetStr = ''
	degImageIdSetStr = ''

	minNumPlayed = db_session.query(Image).order_by(Image.num_played_game1).first().num_played_game1
	while length != 0:
		images = []
		for result in db_session.query(Image).filter_by(num_played_game1=minNumPlayed):
		# for result in db_session.query(Image).filter_by(imagename='800x600n7'):
			images.append((result.image_id, result.imagename))
		os.system('echo images = "' + str(images) + '"')
		random.shuffle(images)
		os.system('echo shuffled_images = "' + str(images) + '"')

		for result in images:
			orgImageIdSetStr += str(result[0])
			filePaths, degImageId = get_file_paths(result[1], result[0])
			filePathsList.append(filePaths)
			degImageIdSetStr += str(degImageId)
			length -= 1
			if length == 0:
				break
			orgImageIdSetStr += '|'
			degImageIdSetStr += '|'

		minNumPlayed += 1

	ig = ImageGallery (GAME1, 1, 0, datetime.now(), orgImageIdSetStr, degImageIdSetStr, 0, str(userId), 0)
	db_session.add(ig)
	db_session.commit()
	os.system('echo create_new_gallery = ' + str(userId))

	return ig.ig_id, filePathsList

def draw_acceptable_output_files(userId):
	os.system('echo draw_acceptable_image_files: start')

	# Step 1
	# found, ig_id, filePathsList = assign_newplayer_to_low_agreement(userId)
	# if found == True:
	# 	return ig_id, filePathsList

	# Step 2
	found, ig_id, filePathsList = assign_newplayer_to_hung_gallery(userId)
	if found == True:
		return ig_id, filePathsList

	# Step 3
	assigned, ig_id, filePathsList = assign_newplayer_to_available_gallery(userId)
	if assigned == True:
		return ig_id, filePathsList

	# Step 4
	ig_id, filePathsList = create_new_gallery(userId)

	os.system('echo "' + str(filePathsList) + '"')
	os.system('echo draw_acceptable_image_files: end')
	return ig_id, filePathsList

def get_image_id(imagename):
	os.system('echo get_image_id: start imagename[' + imagename + "]")
	inext, outext = getExtensions()
	imagename = imagename.split(inext)[0]

	image_id = ''
	for result in db_session.query(Image).filter_by(imagename=imagename):
		image_id = result.image_id
		break
	return image_id

def get_degimage_id(imagename):
	inext, outext = getExtensions()
	imagename = imagename.split(outext)[0]
	os.system('echo get_degimage_id1: ' + imagename)

	image_id = ''
	for result in db_session.query(DegradedImage).filter_by(imagename=imagename):
		image_id = result.deg_image_id
		break
	os.system('echo get_degimage_id2: ' + str(image_id))
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

def get_num_rand_decision(degImageId, decision):
	result = db_session.query(DegradedImage).filter_by(deg_image_id=degImageId).first()
	if decision == "agree":
		record = result.org_num_agree
	elif decision == "disagree":
		record = result.org_num_disagree
	return record

# def get_newhistory(oldHistory, isAgree, error):
# 	newHistory = ""
# 	e = 1
# 	preError = 0
# 	nxtError = ERROR_MAX
# 	for i in range(0, len(drawn_errors)):
# 		if drawn_errors[i] < error:
# 			preError = drawn_errors[i]
# 		if drawn_errors[i] >= error:
# 			nxtError = drawn_errors[i]
# 			break
# 	histories = oldHistory.split('|')
# 	for h in histories:
# 		if e > preError and e <= nxtError:
# 			tokens = h.split(',')
# 			if isAgree == True:
# 				numAgree = int(tokens[0]) + 1
# 			else:
# 				numAgree = tokens[0]
# 			numPlayed = int(tokens[1]) + 1
# 			newH = str(numAgree) + ',' + str(numPlayed)
# 		else:
# 			newH = h
# 		newHistory += newH
# 		if e != ERROR_MAX:
# 			newHistory += '|'
# 		e += 1
#
# 	return newHistory
#
# def update_history(degImageId, isAgree, error):
# 	os.system('echo called?')
# 	orgImageId = db_session.query(DegradedImage).filter_by(deg_image_id=degImageId).first().org_image_id
# 	oldHistory2 = db_session.query(Image).filter_by(image_id=orgImageId).first().game2_history
# 	oldHistory3 = db_session.query(Image).filter_by(image_id=orgImageId).first().game3_history
#
# 	newHistory2 = get_newhistory(oldHistory2, isAgree, error)
# 	newHistory3 = get_newhistory(oldHistory3, isAgree, error)
#
# 	db_session.query(Image).filter(Image.image_id == orgImageId).update({"game2_history": newHistory2})
# 	db_session.query(Image).filter(Image.image_id == orgImageId).update({"game3_history": newHistory3})
# 	db_session.commit()


def update_record(degImageId, decision):
	os.system('echo update_record start')
	result = db_session.query(DegradedImage).filter_by(deg_image_id=degImageId).first()
	if decision == "agree":
		newNum = result.num_agree + 1
		#update_history(degImageId, True, int(float(result.error)*100))
		os.system('echo degImageId = ' + str(degImageId))
		os.system('echo num_agree = ' + str(newNum))
		db_session.query(DegradedImage).filter(DegradedImage.deg_image_id == degImageId).update({"num_agree": newNum})
		# db_session.commit()
	elif decision == "disagree":
		newNum = result.num_disagree + 1
		#update_history(degImageId, False, int(float(result.error)*100))
		os.system('echo degImageId = ' + str(degImageId))
		os.system('echo num_disagree = ' + str(newNum))
		db_session.query(DegradedImage).filter(DegradedImage.deg_image_id == degImageId).update({"num_disagree": newNum})
	db_session.commit()

	# update num_played for degImage
	numPlayed = result.num_played + 1
	db_session.query(DegradedImage).filter(DegradedImage.deg_image_id == degImageId).update({"num_played": numPlayed})
	db_session.commit()

	# update num_played for image
	newresult = db_session.query(Image).filter_by(image_id=result.org_image_id).first()
	numPlayed = newresult.num_played_game1 + 1
	os.system('echo ' + str(numPlayed))
	db_session.query(Image).filter(Image.image_id == newresult.image_id).update({"num_played_game1": numPlayed})
	db_session.commit()

	os.system('echo update_record end')

def save_play(session_uuid, game_type, image_id, deg_image_id, decision, bet, winning):
	os.system('echo save_play start')
	os.system('echo save_play deg_image_id = ' + str(deg_image_id))

	for result in db_session.query(PlaySession).filter_by(session_uuid=session_uuid):
		session_id = result.session_id
		break

	if decision == "agree":
		selnum = 0
	elif decision == "disagree":
		selnum = 1

	p = Play(int(session_id), int(game_type), int(image_id), int(deg_image_id), int(selnum), int(bet), float(winning), 0, 0, 0.0, 0, 0, 0, 0.0)
	db_session.add(p)
	db_session.commit()

	os.system('echo save_play end')

	return p.play_id

def save_play_gallery(user_id, ig_id, session_uuid, play_id_list):

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

	pg = PlayGallery (user_id, ig_id, session_id, play_id_list_str)
	db_session.add(pg)

	ig = db_session.query(ImageGallery).filter_by(ig_id=ig_id).first()
	newNumCompleted = ig.num_completed + 1
	db_session.query(ImageGallery).filter(ImageGallery.ig_id == ig_id).\
										update({"num_completed": newNumCompleted})

	if newNumCompleted == num_people_gallery:
		db_session.query(ImageGallery).filter(ImageGallery.ig_id == ig_id).\
										update({"done": 1})

	db_session.commit()

	os.system('echo save_play_gallery end')
