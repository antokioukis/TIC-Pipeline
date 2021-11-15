from sys import argv
from os import system

OUTPUT_FASTA_EXTRACTION = argv[1]
CLUSTERING_DIRECTORY = argv[2]


file_list = ['2.Taxonomy-Classification/good_ZOTUS.log',
             '2.Taxonomy-Classification/other_ZOTUS.fa',
             '2.Taxonomy-Classification/ZOTUs-Table.tab',
             '2.Taxonomy-Classification/alignment_vector.csv',
             OUTPUT_FASTA_EXTRACTION, CLUSTERING_DIRECTORY,
             'test_s.fasta', 'test_z.fasta', 'sina_output.csv',
             'sina_output.fasta']

for i in file_list:
    system('rm -r ' + i)
