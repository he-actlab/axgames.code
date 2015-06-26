import os, sys

from gatech import session
from gatech.database import db_session
from gatech.models import Image, DegradedImage, Play, PlaySession

#
# webpage update - fetch random input image files from database and throw them to the game page
#
def draw_acceptable_image_files():

	filePaths = []
	os.system('echo draw_acceptable_image_files: 1')
	# os.system('rm -rf gatech/static/img/' + session['sessionid'])
	# os.system('echo rm -rf gatech/static/img/' + session['sessionid'])

	os.system('echo draw_acceptable_image_files: 2')
	drawnImageFilename = ''
	for result in db_session.query(Image).order_by(Image.num_played_game1):
		orgImageId = result.image_id
		drawnImageFilename = result.imagename
		# drawnImageFilename = result.filename
		# drawnImageData = result.image_file
		# drawnSblImageData = result.sbl_image_file
		break

	# os.system('echo draw_acceptable_image_files: 3')
	# with open('gatech/static/img/' + session['sessionid'] + '/' + drawnImageFilename, 'wb') as f1:
	# 	f1.write(drawnImageData)
	# f1.close()

	# os.system('echo draw_acceptable_image_files: 4')
	# drawnSblImageFilename = drawnImageFilename.split('.png')[0] + '-sobel.png'
	# with open('gatech/static/img/' + session['sessionid'] + '/' + drawnSblImageFilename, 'wb') as f2:
	# 	f2.write(drawnSblImageData)
	# f2.close()

	os.system('echo draw_acceptable_image_files: 5')
	filePaths.append('/orgimage/' + drawnImageFilename + '.png')
	filePaths.append('/sobelimage/' + drawnImageFilename + '-sobel.png')

	os.system('echo draw_acceptable_image_files: 6')
	for degresult in db_session.query(DegradedImage).filter_by(org_image_id=orgImageId).\
													 order_by(DegradedImage.num_played):
		drawnImageFilename = degresult.imagename
		# drawnImageFilename = degresult.filename
		# drawnImageData = degresult.image_file
		break

	# with open('gatech/static/img/' + session['sessionid'] + '/' + drawnImageFilename, 'wb') as f2:
	# 	f2.write(drawnImageData)
	# f2.close()

	os.system('echo draw_acceptable_image_files: 6-2 ' + str(drawnImageFilename))
	filePaths.append('/degimage/' + drawnImageFilename + '.png')
	os.system('echo draw_acceptable_image_files: 7 ' + str(filePaths))

	return filePaths

def get_image_id(imagename):
	imagename = imagename.split('.png')[0]
	os.system('echo get_image_id: ' + imagename)
	image_id = ''
	for result in db_session.query(Image).filter_by(imagename=imagename):
		os.system('echo get_image_id: 1')
		image_id = result.image_id
		os.system('echo get_image_id: 2')
		break
	os.system('echo get_image_id: 3')
	return image_id

def get_degimage_id(imagename):
	imagename = imagename.split('.png')[0]
	os.system('echo get_degimage_id: ' + imagename)
	image_id = ''
	for result in db_session.query(DegradedImage).filter_by(imagename=imagename):
		os.system('echo get_degimage_id: 1')
		image_id = result.deg_image_id
		os.system('echo get_degimage_id: 2')
		break
	os.system('echo get_degimage_id: 3')
	return image_id

def get_num_played(degImageId):
	for result in db_session.query(DegradedImage).filter_by(deg_image_id=degImageId):
		numPlayed = result.num_played
		break
	return numPlayed

def get_num_decision(degImageId, decision):
	for result in db_session.query(DegradedImage).filter_by(deg_image_id=degImageId):
		if decision == "SA":
			record = result.num_sagree
		elif decision == "WA":
			record = result.num_wagree
		elif decision == "SD":
			record = result.num_sdisagree
		elif decision == "WD":
			record = result.num_wdisagree
		break
	return record

def update_record(degImageId, decision):
	os.system('echo update_record start')
	for result in db_session.query(DegradedImage).filter_by(deg_image_id=degImageId):
		if decision == "SA":
			newNum = result.num_sagree + 1
			db_session.query(DegradedImage).filter(DegradedImage.deg_image_id == degImageId).\
										update({"num_sagree": newNum})
		elif decision == "WA":
			newNum = result.num_wagree + 1
			db_session.query(DegradedImage).filter(DegradedImage.deg_image_id == degImageId).\
										update({"num_wagree": newNum})
		elif decision == "SD":
			newNum = result.num_sdisagree + 1
			db_session.query(DegradedImage).filter(DegradedImage.deg_image_id == degImageId).\
										update({"num_sdisagree": newNum})
		elif decision == "WD":
			newNum = result.num_wdisagree + 1
			db_session.query(DegradedImage).filter(DegradedImage.deg_image_id == degImageId).\
										update({"num_wdisagree": newNum})
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

	if decision == "SA":
		selnum = 0
	elif decision == "WA":
		selnum = 1
	elif decision == "SD":
		selnum = 2
	elif decision == "WD":
		selnum = 3

	p = Play(int(session_id), int(game_type), int(image_id), int(deg_imageid), int(selnum), int(bet), 0, 0, 0, 0, 0)
	db_session.add(p)
	db_session.commit()

	os.system('echo save_play end')
	return 'success'

