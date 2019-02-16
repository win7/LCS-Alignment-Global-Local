# -------------------------------------------- #
def InitMatrix(n, m, g):
	S = []
	if g == 0:
		S.append([0] * (m + 1))
	else:
		S.append(range(0, (m + 1) * g, g))
	for i in range(1, n + 1):
		S.append([i * g] + [0] * (m))
	return S

def PrintMatrix(M, v, w):
	print "".rjust(3, " "),
	print "".rjust(3, " "),
	for i in w:
		print str(i).rjust(3, " "),
	print
	print "".rjust(3, " "),
	for i in M[0]:
		print str(i).rjust(3, " ") ,
	print
	for k, i in enumerate(M[1:]):
		print str(v[k]).rjust(3, " "),
		for j in i:
			print str(j).rjust(3, " ") ,
		print
	print

def ScoreP(v, w, i, j, p):
	if v[i] == w[j]:
		return p
	else:
		return -1 * p
# -------------------------------------------- #
def LCS(v, w):
	n = len(v)
	m = len(w)
	S = InitMatrix(n, m, 0)
	b = InitMatrix(n, m, 0)
	for i in range(1, n + 1):
		for j in range(1, m + 1):
			if v[i - 1] == w[j - 1]:
				S[i][j] = S[i - 1][j - 1] + 1
				b[i][j] = "\\"
			elif S[i - 1][j] >= S[i][j - 1]:
				S[i][j] = S[i - 1][j]
				b[i][j] = "|"
			else:
				S[i][j] = S[i][j - 1]
				b[i][j] = "-"
	return S, b

def PrintLCS(b, v, i, j, lcs):
	if i == 0 or j == 0:
		print "LCS: ", lcs, "\n"
		return
	if b[i][j] == "\\":
		lcs = v[i-1] + lcs
		PrintLCS(b, v, i - 1, j - 1, lcs)
	else:
		if b[i][j] == "|":
			PrintLCS(b, v, i - 1, j, lcs)
		else:
			PrintLCS(b, v, i, j - 1, lcs)
# -------------------------------------------- #
def AlignmentGlobal(v, w, g, p):
	n = len(v)
	m = len(w)
	S = InitMatrix(n, m, g)
	for i in range(1, n + 1):
		for j in range(1, m + 1):
			S[i][j] = max([S[i - 1][j] + g,
						   S[i - 1][j - 1] + ScoreP(v, w, i - 1, j - 1, p),
						   S[i][j - 1] + g])
	return S

def PrintAlignmentGlobal(S, v, w, i, j, g, p, L, avl, awl):
	if i == 0 and j == 0:
		L = 0
		print "v: ", avl
		print "w: ", awl
		return
	elif i > 0 and S[i][j] == (S[i - 1][j] + g):
		L += 1
		avl = v[i-1] + avl
		awl = "-" + awl
		PrintAlignmentGlobal(S, v, w, i - 1, j, g, p, L, avl, awl)
	elif i > 0 and j > 0 and S[i][j] == S[i - 1][j - 1] + ScoreP(v, w, i - 1, j - 1, p):
		L += 1
		avl = v[i - 1] + avl
		awl = w[j - 1] + awl
		PrintAlignmentGlobal(S, v, w, i - 1, j - 1, g, p, L, avl, awl)
	else:
		L += 1
		avl = "-" + avl
		awl = w[j - 1] + awl
		PrintAlignmentGlobal(S, v, w, i, j - 1, g, p, L, avl, awl)
# -------------------------------------------- #
def AlignmentLocal(v, w, g, p):
	n = len(v)
	m = len(w)
	S = InitMatrix(n, m, 0)
	max_ = 0
	i_max = j_max = 0
	for i in range(1, n + 1):
		for j in range(1, m + 1):
			S[i][j] = max([S[i - 1][j] + g,
						   S[i - 1][j - 1] + ScoreP(v, w, i - 1, j - 1, p),
						   S[i][j - 1] + g,
						   0])
			if S[i][j] > max_:
				max_ = S[i][j]
				i_max = i
				j_max = j
	return S, i_max, j_max

def PrintAlignmentLocal(S, v, w, i, j, g, p, L, avl, awl):
	if i == 0 and j == 0:
		L = 0
		print "v: ", avl
		print "w: ", awl
		return
	elif i > 0 and S[i][j] == (S[i - 1][j] + g):
		L += 1
		PrintAlignmentLocal(S, v, w, i - 1, j, g, p, L, avl, awl)
	elif i > 0 and j > 0 and S[i][j] == S[i - 1][j - 1] + ScoreP(v, w, i - 1, j - 1, p):
		L += 1
		avl = v[i - 1] + avl
		awl = w[j - 1] + awl
		PrintAlignmentLocal(S, v, w, i - 1, j - 1, g, p, L, avl, awl)
	else:
		L += 1
		PrintAlignmentLocal(S, v, w, i, j - 1, g, p, L, avl, awl)
# -------------------------------------------- #

import sys
if __name__ == "__main__":
	if len(sys.argv) > 1:
		f = open(sys.argv[1], "r")
		tc = int(f.readline())
		for i in range(tc):
			v = f.readline().strip("\n")
			w = f.readline().strip("\n")

			# LCS #
			"""S, b = LCS(v, w)
			PrintMatrix(S, v, w)
			PrintMatrix(b, v, w)
			PrintLCS(b, v, len(v), len(w), "") """

			# Alignment Global #
			""" g = -2
			p = 1
			S = AlignmentGlobal(v, w, g, p)
			PrintMatrix(S, v, w)
			PrintAlignmentGlobal(S, v, w, len(v), len(w), g, p, 0, "", "") """

			# Alignment Local #
			g = -2
			p = 1
			S, i_max, j_max = AlignmentLocal(v, w, g, p)
			print i_max, j_max
			PrintMatrix(S, v, w)
			PrintAlignmentLocal(S, v, w, i_max, j_max, g, p, 0, "", "")

		f.close()
	else:
		print "Pass test file..."