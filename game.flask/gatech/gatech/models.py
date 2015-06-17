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
	num_sagree = Column(Integer)
	num_wagree = Column(Integer)
	num_sdisagree = Column(Integer)
	num_wdisagree = Column(Integer)
	org_image_id = Column(Integer, ForeignKey("original_images.image_id"))

	def __init__(self, filename, image_file, error, num_played, num_sagree, num_wagree, num_sdisagree, num_wdisagree, org_image_id):	
		self.filename = filename
		self.image_file = image_file
		self.error = error
		self.num_played = num_played
		self.num_sagree = num_sagree
		self.num_wagree = num_wagree
		self.num_sdisagree = num_sdisagree
		self.num_wdisagree = num_wdisagree
		self.org_image_id = org_image_id

	def __repr__(self):
		return '<DegradedImage %r>' % (self.name)
