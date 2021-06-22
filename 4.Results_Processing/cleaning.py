from sys import argv
from os import system

INPUT_FASTA_EXTRACTION = argv[1]
OUTPUT_FASTA_EXTRACTION = argv[2]
CLUSTERING_DIRECTORY = argv[3]


file_list = ['1.ASV-Creation/good_ZOTUS.log', '1.ASV-Creation/good_ZOTUS.fa', '1.ASV-Creation/denoising.tab',
             '1.ASV-Creation/other_ZOTUS.fa', '1.ASV-Creation/ZOTUs-Table.tab',
             '2.Taxonomy-Classification/alignment_vector.csv', INPUT_FASTA_EXTRACTION,
             OUTPUT_FASTA_EXTRACTION, CLUSTERING_DIRECTORY]

for i in file_list:
    system('rm -r ' + i)
