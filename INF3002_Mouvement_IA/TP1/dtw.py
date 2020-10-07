import numpy as np
from numpy import loadtxt
from numpy.linalg import norm as de

file1 = './DATA_DTW/FC1_1.txt'
file2 = './DATA_DTW/FC2_2.txt'

def loadmat(f1, f2):
    sig1 = loadtxt(f1)
    sig2 = loadtxt(f2)
    return np.zeros(len(sig1) * len(sig2)).reshape((len(sig1), len(sig2))), sig1, sig2

def distance_euclidienne(f1, f2):
    M, sig1, sig2 = loadmat(f1, f2)
    for i in range(len(sig1)):
        for j in range(len(sig2)):
            M[i,j] = de(sig1[i] - sig2[j])
    return M

def distance_elastique(f1, f2):
    M, sig1, sig2 = loadmat(f1, f2)
    M = distance_euclidienne(f1, f2)
    for i in range(1, len(sig1)):
        for j in range(1, len(sig2)):
            M[i,j] += min(M[i-1, j-1], M[i-1, j], M[i, j-1])
    return M

def distance_total(M):
    return sum(sum(M)) / (M.shape[0] * M.shape[1])

print(distance_total(distance_euclidienne(file1, file2)))
print(distance_total(distance_elastique(file1, file2)))

def pcc(m):
    ret = []
    for sm in m:
        ret.append(np.argmin(sm[1:]))
    return ret

print(pcc(distance_euclidienne(file1, file2)))
print(pcc(distance_elastique(file1, file2)))
