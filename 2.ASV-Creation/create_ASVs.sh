########
# Get a FASTQ dataset from EBI
########
wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR212/001/SRR2127221/SRR2127221_1.fastq.gz -P ../0.Template-Data
wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR212/001/SRR2127221/SRR2127221_2.fastq.gz -P ../0.Template-Data

# unzip the dataset
gunzip -d ../0.Template-Data/SRR2127221_1.fastq.gz
gunzip -d ../0.Template-Data/SRR2127221_2.fastq.gz

# merge forward and reverse reads files
usearch -fastq_mergepairs ../0.Template-Data/SRR2127221_1.fastq -reverse ../0.Template-Data/SRR2127221_2.fastq -fastq_maxdiffs 50 -fastq_pctid 20 -fastqout merged.fastq -fastq_trunctail 20 -fastq_minmergelen 200 -fastq_maxmergelen 600 -report report.txt >/dev/null 2>/dev/null

# trim sides from both ends of the merged file to remove primers
usearch -fastx_truncate merged.fastq -stripleft 10 -stripright 10 -fastqout filtered_1.fastq


# filtering merged reads
usearch -fastq_filter filtered_1.fastq -fastq_maxee_rate 0.005 -fastaout filtered_2.fasta #2>>$logfile 1>>$logfile
rm filtered_1.fastq

# dereplicate all sample sequences
usearch -fastx_uniques filtered_2.fasta -fastaout dereped.fasta -sizein -sizeout -threads 4 # > /dev/null 2>&1"
rm filtered_2.fasta

# sort all samples seqs
usearch -sortbysize dereped.fasta -fastaout sorted.fasta # > /dev/null 2>&1
rm dereped.fasta

# create zotus
usearch -unoise3 sorted.fasta -minsize 4 -zotus zotus.fasta -tabbedout denoising.tab # > /dev/null 2>&1

# filter not 16S lookings sequences
rm -r /home/antonios/TIC-Pipeline/2.ASV-Creation/sortme/kvdb
../1.Initialization/sortmerna-4.3.3-Linux/bin/sortmerna --ref ../0.Template-Data/silva-bac-16s-id90.fasta --ref ../0.Template-Data/silva-arc-16s-id95.fasta --reads zotus.fasta --fastx --aligned good_ZOTUs --other non16SrRNA --workdir sortme -e 0.1

# prepare the ZOTUs fasta file by adding size to make it compatibe with UPARSE
python3 add_sizes.py



#############


# clusering of ZOTUs seq into OTUs
usearch -cluster_otus good-ZOTUs-sized.fasta  -fulldp -otus otus.fasta -minsize 1 -uparseout z2s.tab # > /dev/null 2>&1
rm good-ZOTUs-sized.fasta

# read through the OTU file and remove the size anotation to make compatible naming
sed 's:;size=1;::' otus.fasta > SOTUs-All.fasta

# identify non-chimeras
python3 identify_non_chimeras.py
rm z2s.tab

# keep non-chimeric ZOTUs
usearch -fastx_getseqs good_ZOTUs.fa -labels out_file.txt -label_substr_match -fastaout nochi-ZOTUs.fasta
rm out_file.txt

# build the ZOTU table
usearch -otutab merged.fastq -zotus nochi-ZOTUs.fasta -otutabout zotu_table.tab -id 0.97 -threads 4 # > /dev/null 2>&1
