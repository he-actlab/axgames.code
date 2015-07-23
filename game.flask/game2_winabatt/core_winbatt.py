import os, random

from query_winabatt import get_selections, update_winbatt_record, get_history
from gatech.conf import drawn_errors, GAME2_DEFAULT_WINNING, GAME2_MAX_WINNING_PROPORTION

def find_first_disagree_error(history):
	for i in range(0, len(history)):
		if float(history[i][1]) == 0.0:
			continue
		if float(history[i][0]) / float(history[i][1]) < 0.5:
			return i
	return len(history) - 1

def get_winning(filename, error):
	os.system('echo get_winning start')
	history = get_history(filename)
	firstDisagreeError = find_first_disagree_error(history)
	winning= GAME2_DEFAULT_WINNING * GAME2_MAX_WINNING_PROPORTION + (random.random() * 0.5) * (1.0 - abs(firstDisagreeError - error) / 50.0)
	os.system('echo get_winning end')

	update_winbatt_record (filename, error, get_selections(filename))

	return winning, firstDisagreeError

def get_reward (filename, bet, error): # betting money should be in the formula

	os.system('echo get_reward start')

	selections = get_selections(filename)

	num_groups = 5
	reward = 30
	max_reward = 2.0 # 2X reward

	groups_pair = []
	total_sum = 0
	total_cnt = 0
	for i in range(0, len(selections)):
		if selections[i] != 0:
			total_sum += i * selections[i]
			total_cnt += selections[i]
			os.system('echo selections[' + str(i) + '] total_sum = [' + str(total_sum) + ']')
		if i == 0:
			group_sum = 0
		elif i in drawn_errors:
			groups_pair.append([i,group_sum])
			group_sum = 0
		else:
			group_sum += selections[i]
	groups_pair.sort(key=lambda x: x[1])
	if total_cnt == 0:
		average = 25
	else:
		average = total_sum / total_cnt

	os.system('echo get_reward: groups_pair ' + str(groups_pair))
	for i in range(0, len(drawn_errors)):
		if error <= drawn_errors[i]:
			selected_group = drawn_errors[i]
	os.system('echo get_reward: selected_group ' + str(selected_group))
	rank = len(drawn_errors)
	for i in range(0, len(groups_pair)):
		if (groups_pair[i])[0] == selected_group:
			break
		else:
			rank -= 1
	os.system('echo get_reward: rank ' + str(rank))
	reward *= max_reward * (rank / float(num_groups))
	reward = int(reward * 10) / 10.0
	os.system('echo get_reward: reward ' + str(reward))

	update_winbatt_record (filename, error, selections)

	os.system('echo get_reward: reward ' + str(reward))
	os.system('echo get_reward: selections ' + str(selections))

	os.system('echo get_reward end')
	return reward, selections, average