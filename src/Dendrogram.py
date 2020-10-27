#!/usr/bin/python3
'''
dendrogram.py
Date: 2020-10-22
Authors: Julio Ayala, Pinar Oncel, Mara Vizitiu
Description: Script to create dendograms using hierarchical clustering from the
scipy cluster package. The script receives files with similarity matrices, and
builds a hierarchical cluster using the linkage function. Then, a dendogram is
plotted for all matrices given, and saved to an external file.
Usage: dendogram.py [-h] [-m method]
        matrix_file_1 matrix_file_2 matrix_file_3 matrix_file_4
Arguments:
    - matrix_file_1: File with the first similarity matrix. For Running Exercise
        3 from BINP16, this corresponds to the Y chromosome identity matrix
    - matrix_file_2: File with the first similarity matrix. For Running Exercise
        3 from BINP16, this corresponds to the Y chromosome scoring matrix
    - matrix_file_3: File with the first similarity matrix. For Running Exercise
        3 from BINP16, this corresponds to the mtdna identity matrix
    - matrix_file_4: File with the first similarity matrix. For Running Exercise
        3 from BINP16, this corresponds to the mtdna scoring matrix
    - [-m method]: Method for the linkage hierarchical clustering. Defaults to single.
                    Values: single, average, weighted, centroid, median, ward

'''

import sys
import argparse
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt

def create_clusters(input_file, cluster_method = 'single'):
    '''
    Function to create a hierarchical cluster, given a matrix file. Returns an
    array with the relationships between sequences.
    Arguments:
        input_file: Similarity matrix in a tab delimited file.
        cluster_method: Method used for the linkage function.
    Returns:
        clusters: Array with the scores of relationships among sequences.
        labels: List of labels of the matrix file.
    '''
    #Initializing variables for the parsing of the file.
    data = []
    labels = []
    with open(input_file, 'r') as matrix_file:
        header = next(matrix_file)
        for line in matrix_file:
            line = line.strip().split()
            labels.append(line[0])  # first column is added to the labels
            row = []
            for i in range(1, len(line)):
                row.append(float(line[i]))  #The rest of columns are converted to float and added to the data
            data.append(row)
    # The linkage function is used to create the hierarchical cluster of the given data.
    clusters = linkage(data, method = cluster_method)
    return clusters, labels


if __name__ == '__main__':
    # The list of arguments is added. (Matrix 1 through 4)
    p = argparse.ArgumentParser(description=__doc__,
                            formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('matrix_file_1', help = 'matrix file 1',)
    p.add_argument('matrix_file_2', help = 'matrix file 1',)
    p.add_argument('matrix_file_3', help = 'matrix file 1',)
    p.add_argument('matrix_file_4', help = 'matrix file 1',)
    # Argument for the clustering method used. Defaults to single
    p.add_argument (
        '-m',
        dest ='method',
        metavar ='Method to use for clustering. Default is single',
        choices = ['single', 'average', 'weighted', 'centroid', 'median', 'ward'],
        default = 'single'
    )
    args = p.parse_args()

    # Build the clusters for all 4 matrix files
    clusters_id_ychr, labels_id_ychr = create_clusters(args.matrix_file_1, args.method)
    clusters_score_ychr, labels_score_ychr = create_clusters(args.matrix_file_2, args.method)
    clusters_id_mtdna, labels_id_mtdna = create_clusters(args.matrix_file_3, args.method)
    clusters_score_mtdna, labels_score_mtdna = create_clusters(args.matrix_file_4, args.method)

    # Create a figure with 4 subplots (2x2)
    plt.figure(figsize=(10,10))
    plt.suptitle('Hierarchical clustering dendograms for Y chromosome and mtDNA sequences')
    # Create dendogram for the Y Chromosome identity matrix
    plt.subplot(2,2,1) #Adding position in the subplot
    plt.title('Y Chromosome identity')
    dendrogram(clusters_id_ychr
               , labels=labels_id_ychr
               , orientation = 'left') # Setting orientation of the labels/tree
   # Create dendogram for the Y Chromosome scoring matrix
    plt.subplot(2,2,2)
    plt.title('Y Chromosome score')
    dendrogram(clusters_score_ychr
               , labels=labels_score_ychr
               , orientation = 'left')
   # Create dendogram for the mtDNA identity matrix
    plt.subplot(2,2,3)
    plt.title('mtDNA identity')
    dendrogram(clusters_id_mtdna
                , labels=labels_id_mtdna
                , orientation = 'left')
    # Create dendogram for the mtDNA scoring matrix
    plt.subplot(2,2,4)
    plt.title('mtDNA score')
    dendrogram(clusters_score_mtdna
                , labels=labels_score_mtdna
                , orientation = 'left')

    plt.show() # Plotting the figure
