from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
import numpy as np

# Open matrix files
# Read data into array
# Assign keys to another list
# Apply linkage function to data
# Plot linkage results (i.e. Clustering)

import sys
# sys.argv[0] is the script file
# sys.argv[1] is the input file1
# sys.argv[2] is the input file2
# sys.argv[3] is the input file3
# sys.argv[4] is the input file4

def create_dendrogram(input_file):
    data = []
    labels = []
    with open(input_file, 'r') as matrix_file:
        header = next(matrix_file)
        for line in matrix_file:
            line = line.strip().split()
            labels.append(line[0])
            row = []
            for i in range(1, len(line)):
                row.append(float(line[i]))
            data.append(row)
    clusters = linkage(data, method = 'single')
    return clusters, labels

clusters_id_ychr, labels_id_ychr = create_dendrogram(sys.argv[1])
clusters_id_mtdna, labels_id_mtdna = create_dendrogram(sys.argv[2])
clusters_score_ychr, labels_score_ychr = create_dendrogram(sys.argv[3])
clusters_score_mtdna, labels_score_mtdna = create_dendrogram(sys.argv[4])


plt.figure(figsize=(10,10))
plt.subplot(2,2,1)
plt.title('Y Chromosome identity')
dendrogram(clusters_id_ychr
           , labels=labels_id_ychr
           , orientation = 'left')

plt.subplot(2,2,2)
plt.title('Y Chromosome score')
dendrogram(clusters_score_ychr
           , labels=labels_score_ychr
           , orientation = 'left')

plt.subplot(2,2,3)
plt.title('mtDNA identity')
dendrogram(clusters_id_mtdna
            , labels=labels_id_mtdna
            , orientation = 'left')

plt.subplot(2,2,4)
plt.title('mtDNA score')
dendrogram(clusters_score_mtdna
            , labels=labels_score_mtdna
            , orientation = 'left')

plt.show()