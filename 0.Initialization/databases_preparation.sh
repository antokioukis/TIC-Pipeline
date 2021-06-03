#!/bin/bash

##############
# Downloads  #
##############

# LTP
let LTP_version=132
wget https://www.arb-silva.de/fileadmin/silva_databases/living_tree/LTP_release_${LTP_version}/LTPs${LTP_version}_datasets.fasta.tar.gz
wget https://www.arb-silva.de/fileadmin/silva_databases/living_tree/LTP_release_${LTP_version}/LTPs${LTP_version}_SSU.csv
#extract file
tar -xvzf LTPs${LTP_version}_datasets.fasta.tar.gz


# SILVA
let SILVA_version=138
wget https://www.arb-silva.de/fileadmin/silva_databases/release_${SILVA_version}/Exports/SILVA_${SILVA_version}_SSURef_NR99_tax_silva.fasta.gz
#extract file
gunzip -d SILVA_${SILVA_version}_SSURef_NR99_tax_silva.fasta.gz


#####################
# Preprocessing LTP #
#####################

# remove extra spaces from aligned file
sed -r '/^[^>]/ s/\s+//g' < LTPs${LTP_version}_SSU_aligned.fasta > no_spaces_aligned.fasta
# remove extra spaces from compressed file
sed -r '/^[^>]/ s/\s+//g' < LTPs${LTP_version}_SSU_compressed.fasta > no_spaces_compressed.fasta

rm LTPs${LTP_version}_SSU_compressed.fasta LTPs${LTP_version}_SSU_aligned.fasta

# remove new lines from no space file
awk '/^>/{print (NR==1)?$0:"\n"$0;next}{printf "%s", $0}END{print ""}' < no_spaces_aligned.fasta > no_new_line_aligned.fasta
# remove new lines from no space file
awk '/^>/{print (NR==1)?$0:"\n"$0;next}{printf "%s", $0}END{print ""}' < no_spaces_compressed.fasta > no_new_line_compressed.fasta

rm no_spaces_aligned.fasta no_spaces_compressed.fasta

#RNA ---> DNA
sed '/^[^>]/ y/uU/tT/' no_new_line_aligned.fasta > clean_LTP_DNA_aligned.fasta
#RNA ---> DNA
sed '/^[^>]/ y/uU/tT/' no_new_line_compressed.fasta > clean_LTP_DNA_compressed.fasta

rm no_new_line_aligned.fasta no_new_line_compressed.fasta

#keep first and last columns from csv
awk '{print $1, $NF}' LTPs${version}_SSU.csv > LTP_info.csv
# get only archaea out of the LTP info
grep 'Archaea' LTP_info.csv | awk {'print $1'} > archaea_identifiers.txt

# multiline fasta to single line fasta, needed for grep -A 1
awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' < clean_LTP_DNA_compressed.fasta > out.fa
tail -n +2 out.fa > clean_LTP_DNA_compressed.fasta

awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' < clean_LTP_DNA_aligned.fasta > out.fa
tail -n +2 out.fa > clean_LTP_DNA_aligned.fasta

rm out.fa 

# use those identifiers to get the archaea sequences used for 98% match
grep -f archaea_identifiers.txt -A 1 clean_LTP_DNA_compressed.fasta > LTP_archaea_compressed.fasta
# extract the same sequences from the aligned.fasta to use for matching on the aligned sequences
grep -f archaea_identifiers.txt -A 1 clean_LTP_DNA_aligned.fasta > LTP_archaea_aligned.fasta

grep '^>' clean_LTP_DNA_compressed.fasta | awk -F'\t' 'BEGIN {OFS="\t"} {print $1,$6}' | awk -F '>' {'print $2'} > LTP_species_identifiers.txt
grep 'Archaea' LTP_info.csv > LTP_archaea_deep_taxonomy.txt

rm clean_LTP_DNA_compressed.fasta clean_LTP_DNA_aligned.fasta LTP_info.csv

# remove intermidiate files
rm LTPs${version}*
rm archaea_identifiers.txt

python3 update_LTP_taxonomy.py

mv updated_aligned.fasta LTP_archaea_aligned.fasta
mv updated_compressed.fasta LTP_archaea_compressed.fasta

rm LTP_archaea_deep_taxonomy.txt LTP_species_identifiers.txt



#######################
# Preprocessing SILVA #
#######################

# remove new lines from no space file
awk '/^>/{print (NR==1)?$0:"\n"$0;next}{printf "%s", $0}END{print ""}' < SILVA_${SILVA_version}_SSURef_NR99_tax_silva.fasta > no_new_line_compressed.fasta

#RNA ---> DNA
sed '/^[^>]/ y/uU/tT/' no_new_line_compressed.fasta > clean_SILVA_DNA_compressed.fasta

awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' < clean_SILVA_DNA_compressed.fasta > out.fa
tail -n +2 out.fa > fileout.fa

# extract archaea from SILVA
grep -A 1 'Archaea' fileout.fa > SILVA_archaea_unclean.fasta
sed '/^-/ d' SILVA_archaea_unclean.fasta > final_SILVA_archaea.fasta

mv final_SILVA_archaea.fasta SILVA_archaea_compressed.fasta

'''''''''''''''''


python3 update_SILVA_taxonomy.py
mv silva_updated.fasta SILVA_archaea_compressed.fasta

# remove intermidiate files
rm no_new_line_compressed.fasta
rm clean_SILVA_DNA_compressed.fasta
rm out.fa
rm fileout.fa
rm SILVA_archaea_unclean.fasta