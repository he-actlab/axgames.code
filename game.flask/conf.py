#
#
#
GAME_NAME = 'ApproxiGame'

#
# IP:  Image Processing [input:image, output:image]
# OCR: Optical Character Recognition [input:image, output:text]
# SR:  Speech Recognition [input:wav, output:text]
# AE:  Audio Compressor (Encoder) [input:wav, output:mp3]
#
APPLICATION_TYPE = 'AE'

#
#
#
KERNEL_NAME = 'ae'

#
# The list of image file names. It only has prefix without "_sobel" or error rate such as "_0.01".
#
# imagelist_file_path = 'gatech/data/imagelist.txt'
# imagelist_file_path = 'gatech/data/imagelist-ocr.txt'
# imagelist_file_path = 'gatech/data/imagelist-sr.txt'
imagelist_file_path = 'gatech/data/imagelist-ae.txt'

#
# For each image, this file contains one content-based question. The first answer is the correct answer and the others are wrong ones.
#
# question_file_path = 'gatech/data/questions.csv'
# question_file_path = 'gatech/data/questions-ocr.csv'
# question_file_path = 'gatech/data/questions-sr.csv'
question_file_path = 'gatech/data/questions-ae.csv'

#
# The list for all degraded images in the database. As of now, the list should have all file names from IMAGENAME_0.01.png to IMAGENAME_0.5.png.
#
# degimagelist_file_path = 'gatech/data/degimagelist.txt'
# degimagelist_file_path = 'gatech/data/degimagelist-ocr.txt'
# degimagelist_file_path = 'gatech/data/degimagelist-sr.txt'
degimagelist_file_path = 'gatech/data/degimagelist-ae.txt'

#
# Under this path, we can find the three directories, org_image, deg_image, and sobel_image.
#
gamedata_home_url = 'https://s3.amazonaws.com/game.data.' + KERNEL_NAME

#
# Game IDs
#
GAME1 = 0
GAME2 = 1
GAME3 = 2

#
# [Game #1] Which error rate will be accompanied with the image when drawn.
# [Game #2 & #3] This decides the ranges that we differentiate the answers
#
# drawn_errors = [1, 3, 5, 7, 10, 15, 20, 30, 40, 50]
drawn_errors = [500, 650, 700, 800, 900, 1000, 1200, 1500, 2000, 2950] # for audio encoder

#
#
#
# ERROR_MIN = 0
# ERROR_INT = 1
# ERROR_MAX = 50
ERROR_MIN = 3000
ERROR_INT = -50
ERROR_MAX = 500

#
# Number of rounds in a game. This decides how many images should be grouped
#
max_round = 3

#
# Number of people that are initially assigned the same gallery
#
num_people_gallery = 2

#
# Number of seconds that wait for assigning an additional image gallery to one more player
#
#wait_minutes_for_newplayer = 60
wait_minutes_for_newplayer = 30

#
# threshold for rejecting the agreement
#
fleiss_kappa_threshold = 0.3

#
#
#
BADPLAY_THRESHOLD = 40

#
#
#
GAME1_INIT_NUM_PLAYED = 100
GAME1_INIT_BALANCE = 500
GAME1_GALLERY_ASSIGN_INTERVAL = 1
GAME1_RAND_RECORDS_THRESHOLD = 1
#
#
#
GAME2_INIT_ENERGY = 100
GAME2_DEFAULT_WINNING = 5
GAME2_MAX_WINNING_PROPORTION = 1.0
GAME2_INIT_AVG = 20

#
#
#
GAME3_INIT_ENERGY = 100
GAME3_DEFAULT_WINNING = 5
GAME3_MAX_WINNING_PROPORTION = 1.0
GAME3_WRONG_ANSWER_PENALTY = 20
GAME3_INIT_AVG = 20
