import os, sys

from gatech import session
from gatech.database import db_session
from gatech.models import Image, PlaySession, Play

def get_selections(imagename):

	imagename = imagename.split('.')[0]

	for result in db_session.query(Image).filter_by(imagename=imagename):
		selected_error_array = result.selected_error_array_game2
		break
	tokens = selected_error_array.split('|')
	selections = []
	for i in range(0, len(tokens)):
		selections.append(int(tokens[i].encode("ascii")))

	os.system('echo get_selections end')

	return selections

def update_winbatt_record (imagename, selection, selections):

	imagename = imagename.split('.')[0]
	selections[selection] += 1

	newSelections = ""
	for i in range(0, len(selections)-1):
		newSelections = newSelections + str(selections[i]) + "|"
	newSelections = newSelections + str(selections[len(selections)-1])

	for result in db_session.query(Image).filter_by(imagename=imagename):
		num_played_game2 = result.num_played_game2
		db_session.query(Image).filter(Image.imagename == imagename).update({"selected_error_array_game2": newSelections})
		db_session.query(Image).filter(Image.imagename == imagename).update({"num_played_game2": num_played_game2 + 1})
		db_session.commit()
		break

def get_image_id(imagename):
	os.system('echo get_image_id ' + imagename)
	for result in db_session.query(Image).filter_by(imagename=imagename):
		image_id = result.image_id
		break
	return image_id

def save_play(session_uuid, game_type, imagename, error_rate, bet):
	os.system('echo save_play start')

	for result in db_session.query(PlaySession).filter_by(session_uuid=session_uuid):
		session_id = result.session_id
		break

	os.system('echo save_play 1')
	p = Play(int(session_id), int(game_type), int(get_image_id(imagename)), 0, 0, 0, int(error_rate), int(bet), 0, 0, 0)
	os.system('echo save_play 2')
	db_session.add(p)
	os.system('echo save_play 3')
	db_session.commit()

	os.system('echo save_play end')
	return 'success'

def draw_winabatt_image_file():

	imagename = ""
	# os.system('rm -rf gatech/static/img/' + session['sessionid'])
	# os.system('mkdir gatech/static/img/' + session['sessionid'])

	drawnImageFilename = ''
	for result in db_session.query(Image).order_by(Image.num_played_game2):
		# orgImageId = result.image_id
		imagename = result.imagename
		# drawnImageFilename = result.filename
		# drawnImageData = result.image_file
		# drawnSblImageData = result.sbl_image_file
		break

	# with open('gatech/static/img/' + session['sessionid'] + '/' + drawnImageFilename, 'wb') as f1:
	# 	f1.write(drawnImageData)
	# f1.close()
	#
	# drawnSblImageFilename = drawnImageFilename.split('.png')[0] + '-sobel.png'
	# with open('gatech/static/img/' + session['sessionid'] + '/' + drawnSblImageFilename, 'wb') as f2:
	# 	f2.write(drawnSblImageData)
	# f2.close()

	# for degresult in db_session.query(DegradedImage).filter_by(org_image_id=orgImageId):
	# 	drawnImageFilename = degresult.filename
	# 	drawnImageData = degresult.image_file
	# 	with open('gatech/static/img/' + session['sessionid'] + '/' + drawnImageFilename, 'wb') as f2:
	# 		f2.write(drawnImageData)
	# 	f2.close()

	return imagename


