from sys import argv
from os import system

INPUT_FASTA_EXTRACTION = argv[1]
OUTPUT_FASTA_EXTRACTION = argv[2]
CLUSTERING_DIRECTORY = argv[3]


file_list = ['1.Denoising/good_ZOTUS.log', '1.Denoising/good_ZOTUS.fa',
             '1.Denoising/other_ZOTUS.fa', '1.Denoising/ZOTUs-Table.tab',
             '2.Taxonomy-Classification/alignment_vector.csv', INPUT_FASTA_EXTRACTION,
             OUTPUT_FASTA_EXTRACTION, CLUSTERING_DIRECTORY, 'test_s.fasta', 'test_z.fasta']

for i in file_list:
    system('rm -r ' + i)
