import os

from query_qna import get_selections, update_qna_record

def get_reward (filename, bet, error, isCorrect): # betting money should be in the formula

	if isCorrect == True:
		os.system('echo ANSWER IS CORRECT')
	else:
		os.system('echo ANSWER IS WRONG')

	selections = get_selections(filename)

	num_groups = 5
	reward = 30
	max_reward = 2.0 # 2X reward

	groups_pair = []
	elements_in_group = float(len(selections)) / num_groups
	for i in range(0, num_groups): # five groups
		group_sum = 0
		for j in range(int(i * elements_in_group),int((i+1) * elements_in_group)):
			group_sum += selections[j]
		groups_pair.append([i,group_sum])
	groups_pair.sort(key=lambda x: x[1])

	os.system('echo get_reward: groups_pair ' + str(groups_pair))
	selected_group = int(error / elements_in_group)
	rank = num_groups
	os.system('echo get_reward: selected_group ' + str(selected_group))
	for i in range(0, len(groups_pair)):
		if (groups_pair[i])[0] == selected_group:
			break
		else:
			rank -= 1
	os.system('echo get_reward: rank ' + str(rank))
	reward *= max_reward * (rank / float(num_groups))
	reward = int(reward * 10) / 10.0
	os.system('echo get_reward: reward ' + str(reward))

	update_qna_record (filename, error, selections)

	os.system('echo get_reward: reward ' + str(reward))
	os.system('echo get_reward: selections ' + str(selections))
	return reward, selections