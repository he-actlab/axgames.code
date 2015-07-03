import os

from query_winabatt import get_selections, update_winbatt_record
from gatech.conf import

def get_reward (filename, bet, error): # betting money should be in the formula

	os.system('echo get_reward start')

	selections = get_selections(filename)

	os.system('echo get_reward 1')

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

	update_winbatt_record (filename, error, selections)

	os.system('echo get_reward: reward ' + str(reward))
	os.system('echo get_reward: selections ' + str(selections))

	os.system('echo get_reward end')
	return reward, selections