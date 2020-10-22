#!/usr/bin/python3
'''
SimilarityMatrix.py
Similarity Matrix
Date: 2020-10-22
Authors: Pinar Oncel, Mara Vizitiu, Julio Ayala
Description:
Usage: python
Arguments:

'''

def msa_to_dict(input_file):
    msa_matrix_identity = {}
    msa_matrix_score = {}
    with open(input_file, 'r') as msa_file:
        header = next(msa_file)
        for line in msa_file:
            line = line.rstrip().split('\t') # Split the line by its columns
            if line[0] not in msa_matrix_identity: # Create a dictionary if it doesn't exist for both ids
                msa_matrix_identity[line[0]] = {line[0]: '100'}
                msa_matrix_score[line[0]] = {line[0]: '-'}
            if line[1] not in msa_matrix_identity:
                msa_matrix_identity[line[1]] = {line[1]: '100'}
                msa_matrix_score[line[1]] = {line[1]: '-'}

            msa_matrix_identity[line[0]][line[1]] = line[2].replace('%', '') # Add the value to both dictionaries
            msa_matrix_identity[line[1]][line[0]] = line[2].replace('%', '')
            msa_matrix_score[line[0]][line[1]] = line[3] # Add the value to both dictionaries
            msa_matrix_score[line[1]][line[0]] = line[3]

    return msa_matrix_identity, msa_matrix_score


def make_matrix_file(msa_matrix, output_file):
    with open(output_file, 'w') as output_matrix:
        header = sorted(msa_matrix.keys())
        header_str = '\t' + '\t'.join(header)
        output_matrix.write(header_str + '\n')
        for key1 in sorted(msa_matrix.keys()):
            output_matrix.write(key1)
            for key2 in sorted(msa_matrix[key1]):
                output_matrix.write('\t' + msa_matrix[key1][key2])
            output_matrix.write('\n')

def get_most_similar(msa_dict, name):
    max_value = 0
    max_key = ''
    for key in msa_dict[name].keys():
        if key != name:
            if float(msa_dict[name][key]) > max_value:
                max_value = float(msa_dict[name][key])
                max_key = key
    return max_key, max_value

identity_ychr, score_ychr = msa_to_dict('MSAYchr.txt')
identity_mtdna, score_mtdna = msa_to_dict('MSAmtdna.txt')

make_matrix_file(identity_ychr, 'output_id_ychr.txt')
make_matrix_file(score_ychr, 'output_score_ychr.txt')
make_matrix_file(identity_mtdna, 'output_id_mtdna.txt')
make_matrix_file(score_mtdna, 'output_score_mtdna.txt')

name = input('Please enter one of the characters in the story: ')

while name not in identity_ychr:
    name = input('The name is not in the list. Please enter one of the characters in the story: ')

max_name, max_score = get_most_similar(identity_ychr, name)
print('{} is the most similar to {} with a score of {}'.format(name, max_name, max_score))

