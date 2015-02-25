#!/bin/env python

from sqlalchemy import Column, ForeignKey, Integer, String, LargeBinary, Float
from database import Base

class Image (Base):
	__tablename__ = 'original_images'
	imageId = Column(Integer, primary_key=True)
	filename = Column(String(50))
	imageFile = Column(LargeBinary)
	nPlayed = Column(Integer)

	def __init__(self, imageId, filename, imageFile, nPlayed):	
		self.imageId = imageId
		self.filename = filename
		self.imageFile = imageFile
		self.nPlayed = nPlayed

	def __repr__(self):
		return '<OriginalImages %r>' % (self.name)

class DegradedImage (Base):
	__tablename__ = 'degraded_images'
	degImageId = Column(Integer, primary_key=True)
	filename = Column(String(50))
	imageFile = Column(LargeBinary)
	error = Column(Float)
	nPlayed = Column(Integer)
	nAccepted = Column(Integer)
	orgImageId = Column(Integer, ForeignKey("original_images.imageId"))

	def __init__(self, degImageId, filename, imageFile, error, nPlayed, nAcceped):	
		self.degImageId = degImageId
		self.filename = filename
		self.imageFile = imageFile
		self.error = error
		self.nPlayed = nPlayed
		self.nAcceped = nAcceped
		self.orgImageId = orgImageId

	def __repr__(self):
		return '<DegradedImage %r>' % (self.name)