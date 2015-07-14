
def combination_util(arr, data, start, end, index, r, combinations):
	if index == r:
		c = []
		for j in range(0, r):
			c.append(data[j])
		combinations.append(c)
		return

	i = start
	while i <= end and end-i+1 >= r-index:
		data[index] = arr[i]
		combination_util(arr, data, i+1, end, index+1, r, combinations)
		i += 1

def get_combination(arr, n, r):
	data = []
	for i in range(0, r):
		data.append(0)
	combinations = []
	combination_util(arr, data, 0, n-1, 0, r, combinations)
	return combinations

if __name__ == '__main__':
	n = 5
	combinations = get_combination(range(0, n), n, 3)
	print combinations



