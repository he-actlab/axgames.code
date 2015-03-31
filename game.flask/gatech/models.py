#!/bin/env python

from sqlalchemy import Column, ForeignKey, Integer, String, LargeBinary, Float
from database import Base

class Image (Base):
	__tablename__ = 'original_images'
	image_id = Column(Integer, primary_key=True)
	filename = Column(String(50), unique=True)
	image_file = Column(LargeBinary)
	sbl_image_file = Column(LargeBinary)
	num_played = Column(Integer)

	def __init__(self, filename, image_file, sbl_image_file, num_played):	
		self.filename = filename
		self.image_file = image_file
		self.sbl_image_file = sbl_image_file
		self.num_played = num_played

	def __repr__(self):
		return '<OriginalImages %r>' % (self.name)

class DegradedImage (Base):
	__tablename__ = 'degraded_images'
	deg_image_id = Column(Integer, primary_key=True)
	filename = Column(String(50), unique=True)
	image_file = Column(LargeBinary)
	error = Column(Float)
	num_played = Column(Integer)
	num_saccept = Column(Integer)
	num_naccept = Column(Integer)
	num_waccept = Column(Integer)
	num_wreject = Column(Integer)
	num_nreject = Column(Integer)
	num_sreject = Column(Integer)
	org_image_id = Column(Integer, ForeignKey("original_images.image_id"))

	def __init__(self, filename, image_file, error, num_played, num_saccept, num_naccept, num_waccept, num_wreject, num_nreject, num_sreject, org_image_id):	
		self.filename = filename
		self.image_file = image_file
		self.error = error
		self.num_played = num_played
		self.num_saccept = num_saccept
		self.num_naccept = num_naccept
		self.num_waccept = num_waccept
		self.num_wreject = num_wreject
		self.num_nreject = num_nreject
		self.num_sreject = num_sreject
		self.org_image_id = org_image_id

	def __repr__(self):
		return '<DegradedImage %r>' % (self.name)