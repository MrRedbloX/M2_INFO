# 1.1
# 2^n*m

# 1.2

# 1.3
# ATG / AGT / CGT / CTG

# 1.4
import numpy as np

def construire_table(x, y):
    return np.zeros(len(x) * len(y)).reshape((len(x), len(y)))

print(construire_table(['A', 'C', 'T'], ['A', 'T', 'G', 'C']))

# 1.5
# O(n*m)

# 1.6
def lcs(x, y):
    M = construire_table(x, y)
    for i in range(1, len(x)):
        for j in range(1, len(y)):
            if x[i] == y[j]:
                M[i, j] = M[i-1, j-1] + 1
            else:
                M[i, j] = max(M[i-1, j], M[i, j-1])
    return M

X = ['C', 'A', 'T', 'G', 'T']
Y = ['A', 'C', 'G', 'C', 'T', 'G']
print(lcs(X, Y))

# 1.7
# O(n*m + (n-1)*(m-1))

# 2.1
def init_lev(x, y):
    M = construire_table(x, y)
    for i in range(1, len(x)):
        M[i, 0] = i
    for j in range(1, len(y)):
        M[0, j] = j
    return M

# 2.2
def lev(x, y):
    M = init_lev(x, y)
    for i in range(1, len(x)):
        for j in range(1, len(y)):
            M[i,j] = min(M[i-1, j] + 1, M[i, j-1] + 1, M[i-1, j-1] + 0 if x[i] == y[j] else 1)
    return M

print(lev(X, Y))

# 2.3
def lev_with_cost(x, y):
    M = init_lev(x, y)
    for i in range(1, len(x)):
        for j in range(1, len(y)):
            subcost = 0
            if x[i] != y[j]:
                if (x[i] == 'A' and y[j] == 'C') or (x[i] == 'C' and y[j] == 'G') or (x[i] == 'A' and y[j] == 'C'):
                    subcost = 1
                elif (x[i] == 'A' and y[j] == 'G') or (x[i] == 'C' and y[j] == 'T'):
                    subcost = 2
                elif x[i] == 'A' and y[j] == 'T':
                    subcost = 3
            M[i,j] = min(M[i-1, j] + 1, M[i, j-1] + 1, M[i-1, j-1] + subcost)
    return M

print(lev(X, Y))
