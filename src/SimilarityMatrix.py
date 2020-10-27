#!/usr/bin/python3
'''
Title: SimilarityMatrix.py

Date: 2020-10-22

Authors: Pinar Oncel, Mara Vizitiu, Julio Ayala

Description: Using an input file consisting of scores of pairwise sequence alignments between multiple DNA sequences, the script builds two similarity matrices, one based on the percentage identity and the other one on the normalized values of the pairwise alignment scores. For the purpose of the exercise, the script will be used twice, once for the alignment of the mtDNA, and once for the alignment of the Y chromosome sequences.

List of user defined functions:
    msa_to_dict - converts the data stored into the multiple sequence alignment scores file into a nested dictionary containing all of the names of the sequences being compared and their scores in respect to all of the other sequences.
    make_matrix_file - prints the data as a similarity matrix into the output file
    get_most_similar - finds the most similar (highest score) sequence to a specified sequence and returns both the name of the found sequence, as well as the alignment score

List of modules used that are not explained in the course material: N/A

Procedure:
    1. Define a function that converts the data in the input file (i. e. scores and percentages of identity of pairwise sequence alignments) into similarity matrices in the form of nested dictionaries.
    2. Inside the same function, normalize the alignment scores for an easier interpretation of the results.
    3. Define a function that prints the resulting matrices to separate output files (for normalized score and percentage of identity), in the desired format.
    4. Call the above mentioned functions to create the matrices using the proper input files and build corresponding output files.

Usage: python SimilarityMatrix.py MSAmtdna.txt output_id_mtdna.txt output_score_mtdna.txt
        #For the mitochondrial DNA alignment file
       python SimilarityMatrix.py MSAYchr.txt output_id_ychr.txt output_score_ychr.txt
        #For the Y chromosome alignment file

Arguments: sys.argv[0] - script file
           sys.argv[1] - input file
           sys.argv[2] - output file 1 (Identity)
           sys.argv[3] - output file 2 (Score)

'''

import sys

def msa_to_dict(input_file):    #Function that stores data from the input file into a nested dictionary
    msa_matrix_identity = {}    #Matrix (dictionary of dictionaries) of identity percentages
    msa_matrix_score = {}       #Matrix (dictionary of dictionaries) of alignment scores
    list_of_scores = []         #List of all the alignment scores
    with open(input_file, 'r') as msa_file: #Read the input file
        header = next(msa_file) #Read the header (we do not need the information in the header)
        for line in msa_file:   #Read every line in the input file
            line = line.rstrip().split('\t') # Split the line by its columns and remove new line character
            if line[0] not in msa_matrix_identity: # If the ID does not exist in the dictionary
                msa_matrix_identity[line[0]] = {line[0]: '100'} #Add it with an identity percentage of 100 (when sequence is compared against itself)
                msa_matrix_score[line[0]] = {line[0]: '-'} #Add it without a score ("-") (when compared against itself)
    #We add the IDs in the second column of each line to the same dictionary so that the output will be a full, symmetrical matrix. The steps are identical to the ones above
            if line[1] not in msa_matrix_identity:
                msa_matrix_identity[line[1]] = {line[1]: '100'}
                msa_matrix_score[line[1]] = {line[1]: '-'}
    # The identity percentages and the alignment scores are then added to the corresponding dictionaries of dictionaries as values in the nested dictionaries
            msa_matrix_identity[line[0]][line[1]] = line[2].replace('%', '')
            msa_matrix_identity[line[1]][line[0]] = line[2].replace('%', '')
            msa_matrix_score[line[0]][line[1]] = line[3]
            msa_matrix_score[line[1]][line[0]] = line[3]
            list_of_scores.append(int(line[3])) #Add the alignment scores to a list
    #Normalizing the values of the alignment scores to add them to the matrix
    min_val = min(list_of_scores)   #Find the smallest alignment score
    max_val = max(list_of_scores)   #Find the largest alignment score
    for key1 in msa_matrix_score:   #Iterate through all the sequence IDs
        for key2 in msa_matrix_score[key1]: #Iterate through all the nested dictionaries
            if msa_matrix_score[key1][key2] != '-': #If a sequence is not compared with itself
                current_value = float(msa_matrix_score[key1][key2]) #Normalize the score value...
                msa_matrix_score[key1][key2] = round(100*(current_value + abs(min_val))/(max_val + abs(min_val)), 1)    #...by adding the absolute value of the smallest score to all scores and then dividing by the largest value. The result is multiplied by 100 to be easier to read as a percentage
            else:   #When the sequence is compared with itself
                msa_matrix_score[key1][key2] = 100  #Set the alignment score to 100
    return msa_matrix_identity, msa_matrix_score


def make_matrix_file(msa_matrix, output_file):
#Function that writes the matrices to the output files
    with open(output_file, 'w') as output_matrix:   #Open the output file for writing
        header = sorted(msa_matrix.keys())  #The first line consists of all the sequence IDs (sorted)
        header_str = '\t' + '\t'.join(header)   #Separate the IDs by tab in the header
        output_matrix.write(header_str + '\n')  #Write the header to the output file
        for key1 in sorted(msa_matrix.keys()):  #Iterate through all the sorted sequence IDs
            output_matrix.write(key1)           #Write one ID at a time to the output file
            for key2 in sorted(msa_matrix[key1]):
                output_matrix.write('\t' + str(msa_matrix[key1][key2])) #Followed by all of the alignment scores between that ID and the other ones, separated by tab
            output_matrix.write('\n')           #Add a new line

def get_most_similar(msa_dict, name):           #Function for finding the most similar sequence to a specific sequence
    max_value = 0                               #Variable that stores the value of the largest alignment score
    max_key = ''                                #Variable that stores the sequence ID corresponding to the largest alignment score
    for key in msa_dict[name].keys():           #Iterate through all the sequence IDs
        if key != name:                         #Exclude the case of a sequence being compared with itself
            if float(msa_dict[name][key]) > max_value:  #If an alignment score is larger than the current largest one being stored in the variable
                max_value = float(msa_dict[name][key])  #Store the new score as the largest
                max_key = key                   #Store the corresponding sequence ID
    return max_key, max_value


if __name__ == '__main__':
    identity, score = msa_to_dict(sys.argv[1])      #Calling the function for the input file; two matrices are returned
    make_matrix_file(identity, sys.argv[2])         #Write the percentage identity matrix to one output file by calling the proper function
    make_matrix_file(score, sys.argv[3])            #Write the normalized score matrix to another output file by calling the proper function
