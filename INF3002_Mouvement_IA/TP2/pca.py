import sys
import numpy as np

def bvh2matrix(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        ind = lines.index('MOTION') + 3
        return lines[:ind], list(map(lambda l: np.fromstring(l, dtype=np.float32, sep=' '), lines[ind:]))

def pca(mat):
    aat = np.dot(mat, np.transpose(mat))
    ata = np.dot(np.transpose(mat), mat)
    valp1, vecp1 = np.linalg.eig(aat)
    _, vecp2 = np.linalg.eig(ata)
    valp1_size = len(valp1)
    E = np.zeros((valp1_size, valp1_size))
    np.fill_diagonal(E, np.sqrt(valp1.clip(0)))
    U = np.transpose(vecp1)
    V = np.transpose(vecp2)
    return U, E, V, vecp2.shape[0]

def recompose_matrix(U, E, V, max_size, k):
    k = max_size if k > max_size else k
    return np.dot(U[:, :k], np.dot(E[:k, :k], np.transpose(V)[:k]))

def matrix2bvh(filename, hierarchy, mat):
    func = lambda l: np.array2string(l, precision=4, separator=' ', suppress_small=True, formatter={'float_kind':lambda x: "%.4f" % x}).replace('[', '').replace(']', '').replace('\n', '')
    hierarchy.extend(list(map(func, mat)))
    with open(filename, 'w') as f:
        for l in hierarchy:
            f.write(f'{l}\n')

def main(filename, k):
    newfilename = filename.split('.')[1].replace('/', '').replace('\\', '')
    hierarchy, mat = bvh2matrix(filename)
    U, E, V, max_size = pca(mat)
    matrix2bvh(f'{newfilename}_K{k}.bvh', hierarchy, recompose_matrix(U, E, V, max_size, k))

if __name__ == '__main__':
    try:
        main(sys.argv[1], int(sys.argv[2]))
    except Exception as e:
        print(e)
        print('usage: pca <filename> <k>')

# TODO:
#1 Récupérer la matrice à partir du bvh
#2 Décomposer la matrice en 3 autres à partir de la méthode ACP
#3 Choisir k élements dans chacunes des matrices
#4 Recomposer la matrice de départ
#5 Recréer un nouveau fichier bvh à partir de la nouvelle matrice
