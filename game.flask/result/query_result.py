from gatech.database import db_session
from gatech.models import Image, DegradedImage, Play, PlaySession, ImageGallery, PlayGallery, BadPlayGallery
from gatech.conf import APPLICATION_TYPE

import os

def get_org_images():
	return db_session.query(Image)

def get_deg_images():
	return db_session.query(DegradedImage)

def get_admin_sessions():
	return db_session.query(PlaySession).filter(PlaySession.user_id >= 1, PlaySession.user_id <= 100)

def get_plays(session_id, game_type):
	return db_session.query(Play).filter(Play.session_id == session_id, Play.game_type == game_type)

def get_degimage(deg_image_id):
	return db_session.query(DegradedImage).filter_by(deg_image_id=deg_image_id).first()

def get_bad_users(game_type, threshold):
	if game_type == 0:
		return db_session.query(PlaySession).join(Play).join(DegradedImage).filter(Play.session_id == PlaySession.session_id, \
																				   Play.game_type == game_type, \
																				   Play.deg_image_id == DegradedImage.deg_image_id, \
																				   DegradedImage.error > float(threshold) / 100.0, \
																				   Play.selection == 0)
	elif game_type == 1:
		if APPLICATION_TYPE != "AE":
			return db_session.query(PlaySession).join(Play).filter(Play.session_id == PlaySession.session_id, Play.game_type == game_type, Play.error_rate_game2 >= threshold)
		else:
			return db_session.query(PlaySession).join(Play).filter(Play.session_id == PlaySession.session_id, Play.game_type == game_type, Play.error_rate_game2 <= threshold)
	else:
		if APPLICATION_TYPE != "AE":
			return db_session.query(PlaySession).join(Play).filter(Play.session_id == PlaySession.session_id, Play.game_type == game_type, Play.error_rate_game3 >= threshold)
		else:
			return db_session.query(PlaySession).join(Play).filter(Play.session_id == PlaySession.session_id, Play.game_type == game_type, Play.error_rate_game3 <= threshold)

def get_bad_plays(user_id, game_type):
	return db_session.query(Play).join(PlaySession).filter(PlaySession.user_id == user_id, \
														   Play.session_id == PlaySession.session_id, \
														   Play.game_type == game_type)

def get_history(image_id):
	result = db_session.query(Image).filter_by(image_id=image_id).first()
	tokens = result.game3_history.split('|')
	history = []
	for token in tokens:
		pair = token.strip('[').strip(']').split(',')
		nAgree = pair[0]
		nPlayed = pair[1]
		history.append([int(nAgree), int(nPlayed)])
	return history

def get_all_plays(game_type):
	os.system("echo get_all_plays")
	return db_session.query(Play).filter_by(game_type=str(game_type))

