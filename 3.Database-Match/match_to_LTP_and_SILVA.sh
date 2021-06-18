#!/bin/bash

##############
#  MATCHES   #
##############

# create 98% matches between your dataset and the LTP database
python3 create_matches.py -t usearch -n 5 -d ../0.Template-Data/SRR2127221_archaea.fasta -b LTP_archaea_compressed.udb -o archaea -m LTP

# sequences not matched with LTP database, create 98% matches between your dataset and the SILVA database
python3 create_matches.py -t usearch -n 5 -d archaea_not_matched_LTP.fasta -b SILVA_archaea_compressed.udb -o archaea -m SILVA

# remove file containing sequences not matched with LTP, because we will use the double orphans
# from both LTP and SILVA
rm archaea_not_matched_LTP.fasta

# replace LTP matches to dataset
python3 replace_database_matches.py -m LTP

# replace SILVA matches to dataset
python3 replace_database_matches.py -m SILVA

# linearize double orphans so everything is linear
awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' < archaea_not_matched_SILVA.fasta > out.fa
tail -n +2 out.fa > archaea_not_matched_SILVA.fasta
rm out.fa

# concatenate all replacements with sequences not matched with the databases
cat archaea_replaced_SILVA.fasta archaea_replaced_LTP.fasta archaea_not_matched_SILVA.fasta >> archaea_total_replaced.fasta

# clean intermidiate files
rm archaea_replaced_SILVA.fasta archaea_replaced_LTP.fasta archaea_not_matched_SILVA.fasta
rm archaea_LTP.m2 archaea_SILVA.m2

# move final file to the next step
mv archaea_total_replaced.fasta ../3.Taxonomy-Classification/