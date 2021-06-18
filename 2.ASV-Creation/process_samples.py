from sys import argv
from os import system, remove, chdir, getcwd


# return list with each line an element, clear of whitespace
def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


def fastq_merge_pairs(forward_file, reverse_file):
    cmd = CLUSTERING_TOOL + ' -fastq_mergepairs ' + forward_file + ' -reverse ' + reverse_file + ' '
    cmd += '-fastq_maxdiffs ' + MAXDIFF + ' -fastq_pctid ' + MINPCTID + ' -fastqout ' + USER_FASTQ_FOLDER
    cmd += '/merged.fasta -fastq_trunctail ' + TRIM_SCORE + ' -fastq_minmergelen ' + MINMERGELEN
    cmd += ' -fastq_maxmergelen ' + MAXMERGELEN + ' -report ' + USER_FASTQ_FOLDER + '/report.txt >/dev/null 2>/dev/null'
    system(cmd)


def trimming():
    cmd = CLUSTERING_TOOL + " -fastx_truncate " + USER_FASTQ_FOLDER + '/merged.fasta -stripleft '
    cmd += FORWARD_TRIM + ' -stripright ' + REVERSE_TRIM + ' -fastqout ' + USER_FASTQ_FOLDER + '/trimmed.fasta '
    cmd += '2>>' + USER_FASTQ_FOLDER + '/log_file.txt' + ' 1>>' + USER_FASTQ_FOLDER + '/log_file.txt'
    system(cmd)


def filtering():
    cmd = CLUSTERING_TOOL + " -fastq_filter " + USER_FASTQ_FOLDER + '/trimmed.fasta --fastq_maxee_rate '
    cmd += EXPECTED_ERROR_RATE + ' -fastaout ' + USER_FASTQ_FOLDER + '/filtered.fasta '
    cmd += '2>>' + USER_FASTQ_FOLDER + '/log_file.txt' + ' 1>>' + USER_FASTQ_FOLDER + '/log_file.txt'
    system(cmd)


def dereplication():
    cmd = CLUSTERING_TOOL + " -fastx_uniques " + USER_FASTQ_FOLDER + '/filtered.fasta -sizeout '
    cmd += '-minuniquesize 1 -threads ' + THREADS + ' -fastaout ' + USER_FASTQ_FOLDER + '/unique.fasta '
    cmd += '2>>' + USER_FASTQ_FOLDER + '/log_file.txt' + ' 1>>' + USER_FASTQ_FOLDER + '/log_file.txt'
    system(cmd)


def process_samples():
    top_directory = getcwd()
    chdir(USER_FASTQ_FOLDER)
    tab_file_contents = read_file('mapping_file.ssv')
    for line in tab_file_contents:
        tokens = line.split()
        sample_name = tokens[0]
        forward_file = tokens[2]
        if tokens[1] == '1':
            reverse_file = tokens[3]
        print('>>> Processing Sample:' + sample_name)
        out_file = open(top_directory + '/log_file.txt', 'a+')
        out_file.write('\n')
        out_file.write('>>> Processing Sample:' + sample_name + '\n')
        out_file.write('-----------------------------------\n')
        out_file.close()
        print('\tMerging...')
        try:
            fastq_merge_pairs(forward_file, reverse_file)
        except BaseException:
            print('Merging command failed with a critical failure. Exiting...\n')
            exit(1)
        print("\tMerging pairs " + forward_file + ' and ' + reverse_file + ' from sample ' + sample_name + '... Done')
        system('cat ' + USER_FASTQ_FOLDER + '/report.txt >> ' + top_directory + '/log_file.txt')
        remove(USER_FASTQ_FOLDER + '/report.txt')
        print('\tTrimming...')
        try:
            trimming()
        except BaseException:
            print('Trimming command failed with a critical failure. Exiting...\n')
            exit(1)
        else:
            print('\tDone')
        print('\tFiltering merged reads...')
        try:
            filtering()
        except BaseException:
            print('Filtering command failed. Exiting...\n')
            exit(1)
        else:
            print('\tDone')
        print('\tDereplicating sequences...')
        try:
            dereplication()
        except BaseException:
            print('Dereplication command failed. Exiting...\n')
            exit(1)
        else:
            print('\tDone')
        system('mv unique.fasta ' + sample_name + '_unique.fasta')
        remove('merged.fasta')
        remove('trimmed.fasta')
        remove('filtered.fasta')
    chdir(top_directory)


CLUSTERING_TOOL = argv[1]
MAXDIFF = argv[2]
USER_FASTQ_FOLDER = argv[3]
TRIM_SCORE = argv[4]
MINMERGELEN = argv[5]
MAXMERGELEN = argv[6]
FORWARD_TRIM = argv[7]
REVERSE_TRIM = argv[8]
EXPECTED_ERROR_RATE = argv[9]
THREADS = argv[10]
MINPCTID = argv[11]

process_samples()
