#
# The list of image file names. It only has prefix without "_sobel" or error rate such as "_0.01".
#
imagelist_file_path = 'gatech/data/imagelist.txt'

#
# For each image, this file contains one content-based question. The first answer is the correct answer and the others are wrong ones.
#
question_file_path = 'gatech/data/questions.csv'

#
# The list for all degraded images in the database. As of now, the list should have all file names from IMAGENAME_0.01.png to IMAGENAME_0.5.png.
#
degimagelist_file_path = 'gatech/data/degimagelist.txt'

#
# Under this path, we can find the three directories, org_image, deg_image, and sobel_image.
#
gamedata_home_url = 'https://s3-us-west-1.amazonaws.com/game.data'

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
drawn_errors = [1, 3, 5, 7, 10, 15, 20, 30, 40, 50] # should be ordered

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
fleiss_kappa_threshold = 0.5

#
#
#
ERROR_MAX = 50

#
#
#
GAME2_INIT_ENERGY = 100.0
GAME2_DEFAULT_WINNING = 30
GAME2_MAX_WINNING_PROPORTION = 1.5

#
#
#
GAME3_INIT_ENERGY = 100.0
GAME3_DEFAULT_WINNING = 30
GAME3_MAX_WINNING_PROPORTION = 1.5
GAME3_WRONG_ANSWER_PENALTY = 20