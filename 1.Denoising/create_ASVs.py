from glob import glob
from os import system, remove, chdir, getcwd
from sys import argv

USER_FASTQ_FOLDER = argv[1]
CLUSTERING_TOOL = argv[2]
THREADS = argv[3]
MIN_ZOTU_SIZE = argv[4]
SORT_ME_RNA_DB1 = argv[5]
SORT_ME_RNA_DB2 = argv[6]
SORT_ME_RNA_TOOL = argv[7]
RAPID_NJ = argv[8]


def merging_all_samples():
    all_uniques = glob(USER_FASTQ_FOLDER + '/*_unique.fasta')
    output_file = open(USER_FASTQ_FOLDER + '/merged.fasta', 'w+')
    for curr_sample in all_uniques:
        sample_name = curr_sample.split('/')[-1].split('_')[0]
        with open(curr_sample) as fp:
            while True:
                line = fp.readline()
                if not line:
                    break
                if line[0] == '>':
                    output_file.write(line[:-1] + 'barcodelabel=' + sample_name + ';\n')
                else:
                    output_file.write(line)
    output_file.close()


def dereplication_merged():
    cmd = CLUSTERING_TOOL + " -fastx_uniques " + USER_FASTQ_FOLDER + '/merged.fasta -sizeout '
    cmd += '-sizein -threads ' + THREADS + ' -fastaout ' + USER_FASTQ_FOLDER + '/dereped.fasta '
    cmd += '> /dev/null 2>&1'
    system(cmd)


def sort_merged():
    cmd = CLUSTERING_TOOL + " -sortbysize " + USER_FASTQ_FOLDER + '/dereped.fasta'
    cmd += ' -fastaout ' + USER_FASTQ_FOLDER + '/sorted.fasta '
    cmd += '> /dev/null 2>&1'
    system(cmd)


def unoise():
    cmd = CLUSTERING_TOOL + " -unoise3 " + USER_FASTQ_FOLDER + '/sorted.fasta -minsize ' + MIN_ZOTU_SIZE
    cmd += ' -zotus 1.Denoising/zotus.fasta -tabbedout 1.Denoising/denoising.tab '
    cmd += '> /dev/null 2>&1'
    system(cmd)


def remove_chimeras():
    top_directory = getcwd()
    chdir('1.Denoising/')
    print(">>> Filtering out non 16S ZOTUs ... ")
    cmd = SORT_ME_RNA_TOOL + ' --ref ' + SORT_ME_RNA_DB1 + ' --ref ' + SORT_ME_RNA_DB2
    cmd += ' --reads zotus.fasta --fastx --aligned good_ZOTUS --other other_ZOTUS'
    cmd += ' --workdir sortme -e 0.1'
    try:
        system(cmd)
    except BaseException:
        print("The command for removal of non 16S seqs failed\n")
    else:
        system("rm -rf sortme/kvdb")
        remove('zotus.fasta')
        print("Done.\n\n")
    chdir(top_directory)


def create_zotu_table():
    top_directory = getcwd()
    chdir('1.Denoising/')
    cmd = CLUSTERING_TOOL + " -otutab " + USER_FASTQ_FOLDER + '/merged.fasta -zotus good_ZOTUS.fa'
    cmd += " -otutabout ZOTUs-Table.tab -id 0.97  -threads " + THREADS + " > /dev/null 2>&1"
    system(cmd)
    try:
        system(cmd)
    except BaseException:
        print("ZOTU table formation command failed\n")
    else:
        print("Done.\n\n")
    chdir(top_directory)


def create_rapid_nj_tree():
    cmd = RAPID_NJ + " 1.Denoising/good_ZOTUS.fa --input-format fa --cores " + THREADS + " --alignment-type d "
    cmd += "--output-format t --no-negative-length -x 1.Denoising/NJ_ZOTUs_tree.tre"
    system(cmd)


def create_ASVs():
    merging_all_samples()
    dereplication_merged()
    sort_merged()
    unoise()
    remove_chimeras()
    create_zotu_table()
    remove(USER_FASTQ_FOLDER + '/merged.fasta')
    remove(USER_FASTQ_FOLDER + '/dereped.fasta')
    remove(USER_FASTQ_FOLDER + '/sorted.fasta')


create_ASVs()
# create_rapid_nj_tree()
