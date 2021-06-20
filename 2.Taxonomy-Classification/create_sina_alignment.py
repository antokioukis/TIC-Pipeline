from os import system
from sys import argv

SILVA_ARB = argv[1]
SINA_EXECUTABLE = argv[2]
INPUT_FASTA_ALI_CLASS = argv[3]
PDF_REGION_OUTPUT = argv[4]
OUTPUT_FASTA_ALI_CLASS = argv[5]

cmd = SINA_EXECUTABLE + ' --in=' + INPUT_FASTA_ALI_CLASS + ' --out=' + OUTPUT_FASTA_ALI_CLASS + ' --db='
cmd += SILVA_ARB + ' --turn all --search --meta-fmt csv --lca-fields=tax_slv  --fasta-write-dna'
system(cmd)

cmd = 'python3 2.Taxonomy-Classification/create_alignment_vector.py '
cmd += '-i ' + OUTPUT_FASTA_ALI_CLASS + ' -o 2.Taxonomy-Classification'
system(cmd)

cmd = 'Rscript 2.Taxonomy-Classification/ggplot_alignment_vector.R 2.Taxonomy-Classification ' + PDF_REGION_OUTPUT
system(cmd)
