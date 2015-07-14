import os

from query_acceptable import get_num_played, get_num_decision, update_record

# todo: we need a real scoring algorithm
# update_todo: we need to incorporate the six level answers from strong accept to strong reject
def scoring(decision, betmoney, degImageId):
	os.system('echo acceptable scoring start')

	nPlayed = get_num_played(degImageId)
	nAgree = get_num_decision(degImageId, "agree")
	nDisagree = get_num_decision(degImageId, "disagree")

	records = [("agree", nAgree), ("disagree", nDisagree)]
	lsum = 0
	for i in range(0, len(records)):
		if records[i][0] == decision:
			records[i] = (decision, records[i][1] + 1)
			for j in range(0, i + 1):
				lsum += records[j][1]
			break
	percentage = float(lsum) / float(nPlayed + 1)
	decision_location = percentage
	if percentage >= 0.5: # y = -7.8x + 8.9
		c = (-7.8) * percentage + 8.9
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
