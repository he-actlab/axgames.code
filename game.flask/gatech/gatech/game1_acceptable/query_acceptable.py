import os, sys

import time

from gatech import session
from gatech.database import db_session
from gatech.models import Image, DegradedImage, Play, PlaySession
from gatech.conf import drawn_errors

#
# webpage update - fetch random input image files from database and throw them to the game page
#
def draw_acceptable_image_files():
	os.system('echo draw_acceptable_image_files: start')
	filePaths = []

	drawnImageFilename = ''
	for result in db_session.query(Image).order_by(Image.num_played_game1):
		orgImageId = result.image_id
		drawnImageFilename = result.imagename
		break

	filePaths.append('/orgimage/' + drawnImageFilename + '.png')
	filePaths.append('/sobelimage/' + drawnImageFilename + '-sobel.png')

	drawnImageFilename = -1
	minPlayed = 100000
	for error in drawn_errors:
		for tmpResult in db_session.query(DegradedImage).filter_by(org_image_id=orgImageId).filter_by(error=float(error)/100):
			if tmpResult.num_played < minPlayed:
				minPlayed = tmpResult.num_played
				drawnImageFilename = tmpResult.imagename
			break

	filePaths.append('/degimage/' + drawnImageFilename + '.png')
	os.system('echo draw_acceptable_image_files: end filepaths = ' + str(filePaths))

	return filePaths

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
	return 'success'

