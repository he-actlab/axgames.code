import os, sys

from database import db_session
from models import Image, DegradedImage

#
# admin purpose - updata input dataset
#
def upload_files(orgpath, degpath, sblpath):
	debugMsg = 'uploading files done ...'

	# check if passed directoreis exist
	if os.path.isdir(orgpath) == False:
		return 'Failed: there is no path [' + orgpath + ']'
	if os.path.isdir(sblpath) == False:
		return 'Failed: there is no path [' + sblpath + ']'
	if os.path.isdir(degpath) == False:
		return 'Failed: there is no path [' + degpath + ']'

	# insert original image file with precisely sobel-filtered image
	imageList = os.popen('ls ' + orgpath).readlines()
	for image in imageList:
		imageFilename = image.strip('\n')
		if db_session.query(Image).filter_by(filename=imageFilename).count() != 0:
			continue
		with open(orgpath + '/' + imageFilename, 'rb') as f:
			imagedata = f.read()
		f.close()
		sblImageFilename = imageFilename.split('.png')[0] + '-sobel.png'
		if os.path.isfile(sblpath + '/' + sblImageFilename) == False:
			return 'Failed: there is no file [' + sblpath + '/' + sblImageFilename+ ']'
		with open(sblpath + '/' + sblImageFilename, 'rb') as f:
			sblImagedata = f.read()
		f.close()

		i = Image(imageFilename, imagedata, sblImagedata, 0)
		db_session.add(i)
		db_session.commit()
		# i2 = Image.query.get(1)
		# i2 = db_session.query(Image).get(1)

	# approximately sobel-filtered image file directory
	imageList = os.popen('ls ' + degpath).readlines()
	for image in imageList:
		imageFilename = image.strip('\n')
		if db_session.query(DegradedImage).filter_by(filename=imageFilename).count() != 0:
			continue
		with open(degpath + '/' + imageFilename, 'rb') as f:
			imagedata = f.read()
		f.close()
		tokens = imageFilename.strip('.png').split('_')
		error = float(tokens[1])
		orgImageFileName = tokens[0] + '.png'

		orgImageId = -1
		for result in db_session.query(Image).filter_by(filename=orgImageFileName):
			orgImageId = result.image_id
			break
		d = DegradedImage(imageFilename, imagedata, error, 0, 0, 0, 0, 0, 0, 0, orgImageId)
		db_session.add(d)
		db_session.commit()

	return debugMsg

#
# webpage update - fetch random input image files from database and throw them to the game page
#
def draw_image_files():

	filePaths = []	
	os.system('rm gatech/static/img/*.png')

	drawnImageFilename = ''
	for result in db_session.query(Image).order_by(Image.num_played):
		orgImageId = result.image_id
		drawnImageFilename = result.filename
		drawnImageData = result.image_file
		drawnSblImageData = result.sbl_image_file
		numPlayed = result.num_played + 1
		db_session.query(Image).filter(Image.image_id == orgImageId).\
		 						update({"num_played": numPlayed})		
		db_session.commit()
		break
	with open('gatech/static/img/' + drawnImageFilename, 'wb') as f1:
		f1.write(drawnImageData)
	f1.close()
	drawnSblImageFilename = drawnImageFilename.split('.png')[0] + '-sobel.png'
	with open('gatech/static/img/' + drawnSblImageFilename, 'wb') as f2:
		f2.write(drawnSblImageData)
	f2.close()

	filePaths.append('img/' + drawnImageFilename)
	filePaths.append('img/' + drawnSblImageFilename)

	for degresult in db_session.query(DegradedImage).filter_by(org_image_id=orgImageId).\
													 order_by(DegradedImage.num_played):
		degImageId = degresult.deg_image_id
		drawnImageFilename = degresult.filename
		drawnImageData = degresult.image_file
		numPlayed = degresult.num_played + 1
		db_session.query(DegradedImage).filter(DegradedImage.deg_image_id == degImageId).\
		 						update({"num_played": numPlayed})		
		db_session.commit()
		break
	with open('gatech/static/img/' + drawnImageFilename, 'wb') as f2:
		f2.write(drawnImageData)
	f2.close()

	filePaths.append('img/' + drawnImageFilename)

	return filePaths

def get_image_id(filename):
	image_id = ''
	for result in db_session.query(DegradedImage).filter_by(filename=filename):
		image_id = result.deg_image_id
		break
	return image_id

def get_num_played(degImageId):
	for result in db_session.query(DegradedImage).filter_by(deg_image_id=degImageId):
		numPlayed = result.num_played
		break
	return numPlayed

def get_num_accepted(degImageId):
	for result in db_session.query(DegradedImage).filter_by(deg_image_id=degImageId):
		numAccepted = result.num_accepted
		break
	return numAccepted

def update_record(degImageId):
	for result in db_session.query(DegradedImage).filter_by(deg_image_id=degImageId):
		numAccepted = result.num_accepted + 1
		db_session.query(DegradedImage).filter(DegradedImage.deg_image_id == degImageId).\
		 								update({"num_accepted": numAccepted})		
		db_session.commit()
		break
	



