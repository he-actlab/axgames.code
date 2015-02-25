
import random 

# todo: we need a real scoring algorithm
def scoring(decision, betmoney):
	ran = random.random()
	ret = 0
	if ran > 0.5:
		ret = betmoney
	else:
		ret -= betmoney
	return ret

def final_score(list):
	sum = 0
	for element in list:
		sum += element
	return sum