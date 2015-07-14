def fleiss_kappa(N, n, k, table):
		p = []
		for j in range(0, k):
			localSum = 0.0
			for i in range(0, N):
				localSum += table[i][j]
			p.append(localSum / (N * n))

		P = []
		for i in range(0, N):
			localSum = 0.0
			for j in range(0, k):
				localSum += table[i][j] * table[i][j]
			Pval = (localSum - n) / (n * (n-1))
			P.append(Pval)

		Psum = 0.0
		for i in range(0, N):
			Psum += P[i]

		_P = Psum / N

		_Pe = 0.0
		for j in range(0, k):
			_Pe += p[j] * p[j]

		print "_P: " + str(_P)
		print "_Pe: " + str(_Pe)
		if _Pe == 1.0:
			return -1.0
		kappa = (_P - _Pe) / (1.0 - _Pe)

		return kappa

if __name__ == "__main__":

	# N = 10
	# n = 14
	# k = 5
	#
	# table = []
	# table.append([0,0,0,0,14])
	# table.append([0,2,6,4,2])
	# table.append([0,0,3,5,6])
	# table.append([0,3,9,2,0])
	# table.append([2,2,8,1,1])
	# table.append([7,7,0,0,0])
	# table.append([3,2,6,3,0])
	# table.append([2,5,3,2,2])
	# table.append([6,5,2,1,0])
	# table.append([0,2,2,3,7])

	# number of rounds
	N = 3

	# number of people
	n = 2

	# number of options (agree and disgree: 2)
	k = 2

	table = []
	table.append([0,2])
	table.append([2,0])
	table.append([0,2])
	# table.append([0,2])
	# table.append([2,0])
	# table.append([2,0])
	# table.append([1,1])
	# table.append([0,2])
	# table.append([2,0])
	# table.append([2,0])

	kappa = fleiss_kappa(N, n, k, table)

	print kappa


