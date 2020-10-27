#!/usr/bin/env python3
'''
Title: SimilarityMatrixPt2.py

Date: 2020-10-22

Authors: Mara Vizitiu, Pinar Oncel, Julio Ayala

Description: Script to show the most similar sequences to one or all sequences of an input score file.

List of user defined functions: N/A

List of modules used that are not explained in the course material:
    SimilarityMatrix - creates a similarity matrix based on pairwise sequence alignment scores and also finds the most similar sequence (based on identity percentage) to a user input sequence.

Procedure:
    1. Import all necessary modules and specifiy command line arguments.
    2. Use a msa_to_dict function to generate an array (dictionary of dictionaries) containing all of the identity percentages of the pairwise sequence alignments.
    3. Check the user input and print the most similar sequence to each of the sequences in the array, the most similar sequence to the one specified by the user, or an appropriate message, respectively.

Usage: python SimilarityMatrixPt2.py input_file name_to_compare
Example: python SimilarityMatrixPt2.py MSAmtdna.txt ALL

Arguments: input_file: File with all combinations of pairwise identity and raw scores,
                        separated by tabs (Same input file used in SimilarityMatrix)
           name_to_compare: name to compare to the rest of sequences in the file.
                            Use one id from the file, or 'ALL' for all names.

'''

import SimilarityMatrix as sm #Import the previously used script
import sys

name = sys.argv[2]          #Define user input as the third argument
identity = sm.msa_to_dict(sys.argv[1])  #Create an array of identity percentage values using the same function as in the previous part of the exercise
if name.upper() == 'ALL':   #If the name input by the user is "ALL"
    for key in identity[0]: #Iterate through all the identity percentages
        max_name, max_score = sm.get_most_similar(identity[0], key) #Retrieve the most similar hit from the array, and the corresponding score
        print('{} is the most similar to {} with a score of {}%'.format(key, max_name, max_score))  #Print all of the sequences and their corresponding most similar sequence, one pair at a time
elif name in identity[0]:   #If a sequence name is given
    max_name, max_score = sm.get_most_similar(identity[0], name) #Use the identity matrix to find the most similar sequence to the input
    print('{} is the most similar to {} with a score of {}'.format(name, max_name, max_score))  #Print the most similar sequence and the identity percentage
else:       #If the input name is not one of the sequence names
    print('This name is not in the matrix. Please check the sequence id')   #Print relevant message to the user
