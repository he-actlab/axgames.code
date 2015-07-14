#!/bin/env python

from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy_utils.types.password import PasswordType
from database import Base


class Image(Base):
	__tablename__ = 'original_images'
	image_id = Column(Integer, primary_key=True)
	imagename = Column(String(300), unique=True)
	num_played_game1 = Column(Integer)
	num_played_game2 = Column(Integer)
	num_played_game3 = Column(Integer)
	selected_error_array_game2 = Column(String(300))
	question = Column(String(300))
	correct_answer = Column(String(100))
	wrong_answers = Column(String(450))  # at most four wrong answers, each of which has up to 100 chars
	selected_error_array_game3 = Column(String(300))
	game2_history = Column(String(500))
	game3_history = Column(String(500))

	def __init__(self, imagename, num_played_game1, num_played_game2, num_played_game3, selected_error_array_game2, \
							 question, correct_answer, wrong_answers, selected_error_array_game3, game2_history, game3_history):
		self.imagename = imagename
		self.num_played_game1 = num_played_game1
		self.num_played_game2 = num_played_game2
		self.num_played_game3 = num_played_game3
		self.selected_error_array_game2 = selected_error_array_game2
		self.question = question
		self.correct_answer = correct_answer
		self.wrong_answers = wrong_answers
		self.selected_error_array_game3 = selected_error_array_game3
		self.game2_history = game2_history
		self.game3_history = game3_history

	def __repr__(self):
		return '<OriginalImages %r>' % (self.name)


class DegradedImage(Base):
	__tablename__ = 'degraded_images'
	deg_image_id = Column(Integer, primary_key=True)
	imagename = Column(String(300), unique=True)
	error = Column(Float)
	num_played = Column(Integer)
	num_agree = Column(Integer)
	num_disagree = Column(Integer)
	org_image_id = Column(Integer, ForeignKey("original_images.image_id"))

	def __init__(self, imagename, error, num_played, num_agree, num_disagree, org_image_id):
		self.imagename = imagename
		self.error = error
		self.num_played = num_played
		self.num_agree = num_agree
		self.num_disagree = num_disagree
		self.org_image_id = org_image_id

	def __repr__(self):
		return '<DegradedImage %r>' % (self.name)


class User(Base):
	__tablename__ = 'users'
	user_id = Column(Integer, primary_key=True)
	username = Column(String(50), unique=True)
	password = Column(PasswordType(schemes=['pbkdf2_sha512', 'md5_crypt'], deprecated=['md5_crypt'], max_length=50))

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def __repr__(self):
		return '<User %r>' % (self.name)

class PlaySession(Base):
	__tablename__ = 'session'
	session_id = Column(Integer, primary_key=True)
	session_uuid = Column(String(100), unique=True)
	user_id = Column(Integer, ForeignKey("users.user_id"))

	def __init__(self, session_uuid, user_id):
		self.session_uuid = session_uuid
		self.user_id = user_id

	def __repr__(self):
		return '<PlaySession %r>' % (self.name)


class Play(Base):
	__tablename__ = 'play'
	play_id = Column(Integer, primary_key=True)
	session_id = Column(Integer, ForeignKey("session.session_id"))
	image_id = Column(Integer, ForeignKey("original_images.image_id"))
	game_type = Column(Integer)

	# Game1
	deg_image_id = Column(Integer, ForeignKey("degraded_images.deg_image_id"))
	selection = Column(Integer)
	bet_game1 = Column(Integer)

	# Game2
	error_rate_game2 = Column(Integer)
	bet_game2 = Column(Integer)

	# Game3
	is_correct = Column(Integer)
	error_rate_game3 = Column(Integer)
	bet_game3 = Column(Integer)

	def __init__(self, session_id, game_type, image_id, deg_image_id, selection, bet_game1, error_rate_game2, bet_game2, is_correct, error_rate_game3, bet_game3):
		self.session_id = session_id
		self.game_type = game_type
		self.image_id = image_id
		self.deg_image_id = deg_image_id
		self.selection = selection
		self.bet_game1 = bet_game1
		self.error_rate_game2 = error_rate_game2
		self.bet_game2 = bet_game2
		self.is_correct = is_correct
		self.error_rate_game3 = error_rate_game3
		self.bet_game3 = bet_game3

	def __repr__(self):
		return '<Play %r>' % (self.name)

class ImageGallery(Base):
	__tablename__ = 'image_gallery'
	ig_id = Column(Integer, primary_key=True)
	game_id = Column(Integer)
	num_assigned = Column(Integer)
	num_completed = Column(Integer)
	last_assignment = Column(DateTime)
	image_set = Column(String(300))
	deg_image_set = Column(String(300))
	done = Column(Integer)
	played_users = Column(String(300))
	agreed = Column(Integer)

	def __init__(self, game_id, num_assigned, num_completed, last_assignment, image_set, deg_image_set, done, played_users, agreed):
		self.game_id = game_id
		self.num_assigned = num_assigned
		self.num_completed = num_completed
		self.last_assignment = last_assignment
		self.image_set = image_set
		self.deg_image_set = deg_image_set
		self.done = done
		self.played_users = played_users
		self.agreed = agreed

	def __repr(self):
		return '<ImageGallery %r>' % (self.name)

class PlayGallery(Base):
	__tablename__ = 'play_gallery'
	pg_id = Column(Integer, primary_key=True)
	play_user_id = Column(Integer, ForeignKey("users.user_id"))
	ig_id = Column(Integer, ForeignKey("image_gallery.ig_id"))
	session_id = Column(Integer, ForeignKey("session.session_id"))
	play_id_list = Column(String(300))

	def __init__(self, play_user_id, ig_id, session_id, play_id_list):
		self.play_user_id = play_user_id
		self.ig_id = ig_id
		self.session_id = session_id
		self.play_id_list = play_id_list

	def __repr(self):
		return '<PlayGallery %r>' % (self.name)

class BadPlayGallery(Base):
	__tablename__ = 'bad_pg_records'
	bpg_id = Column(Integer, primary_key=True)
	pg_id = Column(Integer, ForeignKey("play_gallery.pg_id"))
	good_fleiss_kappa = Column(String(100))
	bad_fleiss_kappa = Column(String(100))

	def __init__(self, pg_id, good_fleiss_kappa, bad_fleiss_kappa):
		self.pg_id = pg_id
		self.good_fleiss_kappa = good_fleiss_kappa
		self.bad_fleiss_kappa = bad_fleiss_kappa

	def __repr__(self):
		return '<BadPlayGallery %r>' % (self.name)