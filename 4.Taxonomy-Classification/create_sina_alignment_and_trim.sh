# SILVA releases ARB file frequently please check https://www.arb-silva.de/download/arb-files/
# and replace the link with the Ref NR 99
wget https://www.arb-silva.de/fileadmin/arb_web_db/release_138_1/ARB_files/SILVA_138.1_SSURef_NR99_12_06_20_opt.arb.gz
gunzip -d SILVA_138.1_SSURef_NR99_12_06_20_opt.arb.gz

# change for the latest sina binary
wget https://github.com/epruesse/SINA/releases/download/v1.7.2/sina-1.7.2-linux.tar.gz
tar -xvzf sina-1.7.2-linux.tar.gz
rm sina-1.7.2-linux.tar.gz

# change to the sina version of the directory
# the index for the arb file will be created only the first time you run with a new ARB file
sina-1.7.2-linux/sina --in=archaea_total_replaced.fasta --out=sina_output.fasta --db=SILVA_138.1_SSURef_NR99_12_06_20_opt.arb --turn all --search --meta-fmt csv --lca-fields=tax_slv  --fasta-write-dna
rm archaea_total_replaced.fasta

# sum aligned bases for each of the 50K positions of the sina alignment
python3 create_alignment_vector.py -i sina_output.fasta

# plot the alignment vector so you can decide which is the representative region for your dataset
Rscript ggplot_alignment_vector.R

# extract sequences that have at least N aligned bases within your region
python3 extract_regions.py -i sina_output.fasta -s 10000 -e 25000 -l 100

# update taxonomy classifications from sina
python3 update_taxonomy.py

# cleanup intermidiate files
rm dataset_extracted.fasta sina_output.csv

mv dataset_extracted_new_taxonomy.fasta ../4.Taxonomy-Informed-Clustering/