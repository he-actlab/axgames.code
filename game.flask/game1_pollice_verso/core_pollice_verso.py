import os

from query_pollice_verso import get_num_played, get_num_decision, update_record, get_num_rand_decision
from gatech.conf import GAME1_INIT_NUM_PLAYED, GAME1_RAND_RECORDS_THRESHOLD

# todo: we need a real scoring algorithm
# update_todo: we need to incorporate the six level answers from strong accept to strong reject
def scoring(decision, betmoney, degImageId):
	os.system('echo acceptable scoring start')

	nPlayed = get_num_played(degImageId)
	nAgree = get_num_decision(degImageId, "agree")
	nDisagree = get_num_decision(degImageId, "disagree")
	if nPlayed >= GAME1_INIT_NUM_PLAYED + GAME1_RAND_RECORDS_THRESHOLD:
		nPlayed -= GAME1_INIT_NUM_PLAYED
		nAgree -= get_num_rand_decision(degImageId, "agree")
		nDisagree -= get_num_rand_decision(degImageId, "disagree")
	os.system('echo decision = ' + str(decision))
	os.system('echo nPlayed = ' + str(nPlayed))
	os.system('echo nAgree = ' + str(nAgree))
	os.system('echo nDisagree = ' + str(nDisagree))

	records = [("agree", nAgree), ("disagree", nDisagree)]
	lsum = 0
	for i in range(0, len(records)):
		os.system('echo records[i][0] = ' + str(records[i][0]))
		if records[i][0] == decision:
			records[i] = (decision, records[i][1] + 1)
			lsum = records[i][1]
			break

	minWinningRate = 1.1
	maxWinningRate = 5.0
	os.system('echo lSum = ' + str(lsum))
	percentage = float(lsum) / float(nPlayed + 1)
	decision_location = percentage
	#
	# (1) y = (y0 - y1)/(x0 - x1) * x + p
	#          -> where
	#          -> x >= 0.5
	#          -> (x0, y0) = (0.5, maxWinningRate)
	#          -> (x1, y1) = (1.0, minWinningRate)
	#
	# (2) y = 2 * x   where x < 0.5
	#
	if percentage > 0.5:
		slope = (minWinningRate - maxWinningRate) / (1.0 - 0.5)
		os.system('echo slope = ' + str(slope))
		yIntercept = minWinningRate - slope
		os.system('echo yIntercept = ' + str(yIntercept))
		os.system('echo percentage = ' + str(percentage))
		c = slope * percentage + yIntercept
		os.system('echo c = ' + str(c))
	else:
		c = 2 * percentage
	score = betmoney * c

	options = []
	proportion = []
	for record in records:
		options.append(record[0])
		proportion.append(float(record[1]) / float(nPlayed + 1))

	update_record(degImageId, decision)

	os.system('echo acceptable scoring end')
	return score, options, proportion, decision_location


def final_score(list):
	sum = 0
	for element in list:
		sum += element
	return sum


def calculate_reward(totalscore):
	if totalscore < 0:
		return 0.01
	elif totalscore < 500:
		return 0.02
	elif totalscore < 1000:
		return 0.03
	elif totalscore < 2000:
		return 0.04
	elif totalscore < 5000:
		return 0.05
	elif totalscore < 10000:
		return 0.06
	else:
		return 0.07
