import os

from query_acceptable import get_num_played, get_num_decision, update_record

# todo: we need a real scoring algorithm
# update_todo: we need to incorporate the six level answers from strong accept to strong reject
def scoring(decision, betmoney, degImageId):

	os.system('echo degImageId=' + str(degImageId))
	nPlayed = get_num_played (degImageId)
	os.system('echo nPlayed=' + str(nPlayed))
	nAgree = get_num_decision (degImageId, "agree")
	nDisagree = get_num_decision (degImageId, "disagree")
	
	records = [("agree", nAgree), ("disagree", nDisagree)]
	os.system('echo records=' + str(records))
	sortedRecords = sorted(records, key=lambda x: x[1])
	lsum = 0
	for i in range(0, len(sortedRecords)):
		if sortedRecords[i][0] == decision:
			sortedRecords[i] = (decision, sortedRecords[i][1] + 1)
			#sortedRecords[i][1] = sortedRecords[i][1] + 1 # add the current decision
			for j in range(0, i+1):
				lsum += sortedRecords[j][1]
	percentage = float(lsum) / float(nPlayed + 1)
	decision_location = percentage
	os.system('echo decision_location=' + str(decision_location))
	percentage -= 0.5
	os.system('echo percentage=' + str(percentage))
	score = betmoney * percentage
	os.system('echo score=' + str(score))
	
	options = []
	proportion = []
	for record in sortedRecords:
		options.append(record[0])
		proportion.append(float(record[1])/float(nPlayed + 1))
	os.system('echo options=' + str(options))
	os.system('echo proportion=' + str(proportion))

	update_record (degImageId, decision)
	
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
