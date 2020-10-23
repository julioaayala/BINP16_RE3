from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt

import numpy as np

X = np.array([[1,10,10],
    [10,15,23],
    [15,12, 34],
    [24,10, 45],
    [30,30, 56],
    [85,70, 67],
    [71,80, 78],
    [60,78, 89],
    [70,55, 91],
    [10, 1, 10],])
linked = linkage(X, 'single')

labelList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

#plt.figure(figsize=(10, 7))
dendrogram(linked,
            orientation='left',
            labels=labelList,
            distance_sort='descending',
            show_leaf_counts=True)
plt.show()
