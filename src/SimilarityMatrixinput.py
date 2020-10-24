#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 18:58:28 2020

@author: pinar
"""

import SimilarityMatrix as sm
import sys

name = input('Please enter one of the characters in the story, or ALL for everyone')
identity = sm.msa_to_dict(sys.argv[1])
if name != 'ALL':
    while name not in identity:
        name = input('The name is not in the list. Please enter one of the characters in the story: ')
    max_name, max_score = sm.get_most_similar(identity, name)
    print('{} is the most similar to {} with a score of {}'.format(name, max_name, max_score))
else:
    for key in identity:
        max_name, max_score = sm.get_most_similar(identity, key)
        print('{} is the most similar to {} with a score of {}'.format(key, max_name, max_score))