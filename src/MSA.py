#!/usr/bin/python3

'''
MSA.py
identity and alignment scores
Date : 2020-10-21
Authors : Julio Ayala, Mara Vizitiu, Pinar Oncel

Description : this is a script to calculate identity and alignment scores for each pair of sequences in a given fasta file

Usage1 : mitochondrial DNA sequences : python3 MSA.py ../data/mtdna_orig.fasta ../data/weights.txt ../results/MSAmtdna.txt
Usage2 : Y chromosome sequences :      python3 MSA.py ../data/y_chromosome_orig.fasta ../data/weights.txt ../results/MSAYchr.txt

Arguments :
- mtdna_orig.fasta :        an input file in fasta format containing aligned mitochondrial DNA sequences
- y_chromosome_orig.fasta : an input file in fasta format containing aligned Y chromosome sequences
- weights.txt :             a reference file with weights used for alignment scoring
weight types and weight values are separated by a tab in one line : (1)match:1 (2)transition:-1 (3)transversion:-2 (4)gap:-1
- MSAmtdna.txt :            an output file including pairs of sequences and their respective identity scores
- MSAYchr.txt :             an output file including pairs of sequences and their respective alignment scores
'''

import sys

def score_alignment_identity(seq_1, seq_2, weights):
    '''
    this is a function to score an alignment of a pair of sequences
    Arguments :  seq_1, seq_2 (str) : two aligned sequences including gaps
                 weights (dict) : scores for reference
    Returns : identity and alignment scores (tuple)
    '''
    nucleotides = ['A', 'T', 'G', 'C', '?', '-']      # list of all nucleotides
    purines = ['A', 'G']                              # list of purine nucleotides
    pyrimidines = ['T', 'C']                          # list of pyrimidine nucleotides

    score = 0                                         # variable to store score
    identical = 0                                     # variable to store identical nucleotides

    # how to calculate pairwise alignment score
    for i in range(len(seq_1)):
        if (seq_1[i] == seq_2[i]):                    # when they are same
            if (seq_1[i] == '-' or seq_1[i] == '?'):  # when they are gaps
                pass
            else:                                     # when its a match
                score += weights['match']
                identical += 1
        elif (seq_1[i] in purines and seq_2[i] in purines) or (seq_1[i] in pyrimidines and seq_2[i] in pyrimidines):
            score += weights['transition']            # when its a transition
        elif (seq_1[i] == '-' or seq_2[i] == '-'):    # when theres a gap
            score += weights['gap']
        elif (seq_1[i] == '?' or seq_2[i] == '?'):    # when one is unknown
            pass
        else:                                         # when its a transversion
            score += weights['transversion']
    # how to calculate pairwise identity score
    identity = round(100 * identical / len(seq_1), 1) # divide nr of identical by length
    return identity, score                            # return score and identity as a tuple

def fasta_to_dict(fasta_file):
    '''
    this is a function to convert a fasta file into a dictionary
    Arguments : fasta_file : file with fasta sequences, where the header delimiter is a tab
    Returns : dictionary with sequence IDs as keys, and sequences as values
    '''
    sequences = {} # set up an empty dictionary to store sequence ID and sequence

    # how to retrieve sequences from the fasta file
    with open(fasta_file, 'r') as fasta:
        for line in fasta:
            if line.startswith('>'): # get ID and sequence and add to dictionary
                header = line.strip()[1:]
                sequences[header] = next(fasta).upper().strip()
    return sequences

weights = {} # set up an empty dictionary to store weight type and value

# how to build a dictionary from reference file
with open(sys.argv[2], 'r') as weight_file:
    for line in weight_file:
        line = line.split()
        weights[line[0]] = int(line[1]) # add weight type and values to dictionary

fasta_dict = fasta_to_dict(sys.argv[1]) # convert fasta to dictionary using function

with open(sys.argv[3], 'w') as output_file:
    output_file.write('SmpA\tSmpB\tId_s\tAl_s\n')               # write out header row
    for i, (key_1, seq_1) in enumerate(fasta_dict.items()):     # get ID and seq from dictionary
        for j, (key_2, seq_2) in enumerate(fasta_dict.items()): # get ID and seq from dictionary
            if i < j:                                           # compare two non-repeating sequences
                iden, score_seq = score_alignment_identity(seq_1, seq_2, weights) # get identity and alignment scores
                output_file.write('{}\t{}\t{}%\t{}\n'.format(key_1, key_2, iden, score_seq)) # write out data
print('DONE')
