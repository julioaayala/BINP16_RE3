#!/bin/bash
# Julio Ayala, Pinar Oncel, Mara Vizitiu
# Run this script to generate all files and plot at once.
python src/MSA.py data/mtdna_orig.fasta data/weights.txt results/MSAmtdna.txt
python src/MSA.py data/y_chromosome_orig.fasta data/weights.txt results/MSAYchr.txt
python src/SimilarityMatrix.py results/MSAmtdna.txt results/output_id_mtdna.txt results/output_score_mtdna.txt
python src/SimilarityMatrix.py results/MSAYchr.txt results/output_id_ychr.txt results/output_score_ychr.txt
python src/Dendrogram.py results/output_id_ychr.txt results/output_score_ychr.txt results/output_id_mtdna.txt results/output_score_mtdna.txt
