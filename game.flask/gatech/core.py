import os, sys
import random 

from query import get_num_played, get_num_accepted, update_record

# todo: we need a real scoring algorithm
def scoring(decision, betmoney, degImageId):

	winlose = True

	numPlayed = get_num_played (degImageId)
	numAccepted = get_num_accepted (degImageId)

	if float(numPlayed) - 1 > 0:
		if float(numAccepted) / (float(numPlayed) - 1) > 0.5: # accept
			if decision == 'accept':
				winlose = True
			else:
				winlose = False
		else: # reject
			if decision == 'accept':
				winlose = False
			else:
				winlose = True
	else: # if this is the first time to be evaluated, just give the victory to the player
		winlose = True

	if winlose == True:
		ret = betmoney
	else:
		ret = -betmoney

	if decision == 'accept':
		update_record (degImageId)

	return ret

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