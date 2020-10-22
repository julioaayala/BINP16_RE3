#!/usr/bin/python3
'''
MSA.py
Multiple Sequence Alignment
Date: 2020-10-21
Authors: Pinar Oncel, Mara Vizitiu, Julio Ayala
Description: Script to calculate the pairwise alignment score and the identity score for each pair of sequences in a file.
Usage: python MSA.py fasta_file weight_parameters output_file
Arguments:
    - fasta_file: Input file in the fasta_format containing aligned sequences.
    - weight_parameters: File with weights for the scoring of alignments. Weight type and value should be separated by a tab in one line. e.g.:
        match   1
        transition  -1
        transversion    -2
        gap -1
    - output_file: File with the sequence pairs with their respective identity and alignment score.
'''


# First, we define a function to calculate the alignment score for a pair of sequences:
def score_alignment_identity(seq_1, seq_2, weights):
    '''Function to score an alignment of two sequences
    Arguments:  seq_1, seq_2 (str): sequences, including gaps.
                weights (dict): scores for each case.
    Returns: score and identity of the alignment (tuple)
    '''
    nucleotides = ['A', 'T', 'G', 'C', '?', '-'] # list of all nucleotides
    purines = ['A', 'G']                        # list of purine nucleotides
    pyrimidines = ['T', 'C']                    # list of pyrimidine nucleotides

    score = 0 #Variable to store the score
    identical = 0 #Variable to store the identical nucleotides
    for i in range(len(seq_1)):
        # Add to the score given the different cases
        if (seq_1[i] == seq_2[i]):
            if (seq_1[i] == '-' or seq_1[i] == '?'): #When both are gaps, exclude
                pass
            else:
                score += weights['match']
                identical += 1
        elif (seq_1[i] in purines and seq_2[i] in purines) or (seq_1[i] in pyrimidines and seq_2[i] in pyrimidines):
            score += weights['transition']
        elif (seq_1[i] == '-' or seq_2[i] == '-'):
            score += weights['gap']
        elif (seq_1[i] == '?' or seq_2[i] == '?'): #When one of the nucleotides is
            pass
        else:
            score += weights['transversion']

    identity = round(100 * identical / len(seq_1), 1) # Calculate the identity by dividing identical/length
    return identity, score # Return score and identity as a tuple

# Lastly, we define a function to build a dictionary from a fasta file:
# keys = identity of person and values = DNA sequence
def fasta_to_dict(fasta_file):
    '''Function to convert a fasta file into a dictionary
    Arguments: fasta_file, file with fasta sequences, where the header delimiter is >
    Returns: dictionary with ids as keys, and sequences as values
    '''
    sequences = {}
    # Retrieve sequences from the fasta file
    with open(fasta_file, 'r') as fasta:
        for line in fasta:
            if line.startswith('>'): # Get the id from the header and add it to sequence dict
                header = line.strip()[1:]
                sequences[header] = next(fasta).upper().strip()
    return sequences


# Dictionary for weights file
weights = {}
with open('weights.txt', 'r') as weight_file: # Open a weights file and
    for line in weight_file:
        line = line.split()
        weights[line[0]] = int(line[1])

# Converting fasta files to dictionaries
mtdna_dict = fasta_to_dict('mtdna.fasta')
Ychr_dict = fasta_to_dict('y_chromosome.fasta')

# Running the MSA for the mtdna
with open('MSAmtdna.txt', 'w') as output_file:
    output_file.write('SmpA\tSmpB\tId_s\tAl_s\n')
    for i, (key_1, seq_1) in enumerate(mtdna_dict.items()): # Get and index, and items from dict.
        for j, (key_2, seq_2) in enumerate(mtdna_dict.items()):
            if i < j: # Compare with non-repeating sequences
                # Calculate scores and add to file
                iden, score_seq = score_alignment_identity(seq_1, seq_2, weights)
                output_file.writelines('{}\t{}\t{}%\t{}\n'.format(key_1, key_2, iden, score_seq))

# Running the MSA for the Y chromosome
with open('MSAYchr.txt', 'w') as output_file:
    output_file.write('SmpA\tSmpB\tId_s\tAl_s\n')
    for i, (key_1, seq_1) in enumerate(Ychr_dict.items()): # Get and index, and items from dict.
        for j, (key_2, seq_2) in enumerate(Ychr_dict.items()):
            if i < j: # Compare with non-repeating sequences
                # Calculate scores and add to file
                iden, score_seq = score_alignment_identity(seq_1, seq_2, weights)
                output_file.writelines('{}\t{}\t{}%\t{}\n'.format(key_1, key_2, iden, score_seq))
