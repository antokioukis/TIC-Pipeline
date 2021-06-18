from os.path import isdir
from os import system


# return list with each line an element, clear of whitespace
def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


config_file_contents = read_file('config_options.txt')
for line in config_file_contents:
    if not line or line[0] == '#':
        continue
    tokens = line.split(':')
    if tokens[0] == 'LTP_VERSION':
        LTP_VERSION = tokens[1]
    elif tokens[0] == 'LTP_DOWNLOAD':
        LTP_DOWNLOAD = tokens[1]
    elif tokens[0] == 'LTP_UNZIP':
        LTP_UNZIP = tokens[1]
    elif tokens[0] == 'LTP_PROCESS':
        LTP_PROCESS = tokens[1]
    elif tokens[0] == 'SILVA_VERSION':
        SILVA_VERSION = tokens[1]
    elif tokens[0] == 'SILVA_DOWNLOAD':
        SILVA_DOWNLOAD = tokens[1]
    elif tokens[0] == 'SILVA_UNZIP':
        SILVA_UNZIP = tokens[1]
    elif tokens[0] == 'SILVA_PROCESS':
        SILVA_PROCESS = tokens[1]
    elif tokens[0] == 'CLUSTERING_TOOL':
        CLUSTERING_TOOL = tokens[1]
    elif tokens[0] == 'SAMPLES_PROCESS_STEP':
        SAMPLES_PROCESS_STEP = tokens[1]
    elif tokens[0] == 'ASV_CREATION_STEP':
        ASV_CREATION_STEP = tokens[1]
    elif tokens[0] == 'USER_FASTQ_FOLDER':
        USER_FASTQ_FOLDER = tokens[1]
    elif tokens[0] == 'TRIM_SCORE':
        TRIM_SCORE = tokens[1]
    elif tokens[0] == 'MAXDIFF':
        MAXDIFF = tokens[1]
    elif tokens[0] == 'MINPCTID':
        MINPCTID = tokens[1]
    elif tokens[0] == 'MINMERGELEN':
        MINMERGELEN = tokens[1]
    elif tokens[0] == 'MAXMERGELEN':
        MAXMERGELEN = tokens[1]
    elif tokens[0] == 'FORWARD_TRIM':
        FORWARD_TRIM = tokens[1]
    elif tokens[0] == 'REVERSE_TRIM':
        REVERSE_TRIM = tokens[1]
    elif tokens[0] == 'EXPECTED_ERROR_RATE':
        EXPECTED_ERROR_RATE = tokens[1]
    elif tokens[0] == 'THREADS':
        THREADS = tokens[1]
    elif tokens[0] == 'MIN_ZOTU_SIZE':
        MIN_ZOTU_SIZE = tokens[1]
    elif tokens[0] == 'SORT_ME_RNA_DB1':
        SORT_ME_RNA_DB1 = tokens[1]
    elif tokens[0] == 'SORT_ME_RNA_DB2':
        SORT_ME_RNA_DB2 = tokens[1]
    elif tokens[0] == 'SORT_ME_RNA_TOOL':
        SORT_ME_RNA_TOOL = tokens[1]
    else:
        print('Configuration File Not valid')
        print('Option ' + tokens[0] + ' Not recognised')
        print('Exiting')
        exit(1)

print('Configuration File Valid and Complete')
arguments_list = ' '.join([CLUSTERING_TOOL, LTP_DOWNLOAD, LTP_UNZIP, LTP_PROCESS, LTP_VERSION, SILVA_DOWNLOAD,
                           SILVA_UNZIP, SILVA_PROCESS, SILVA_VERSION
                           ])
system('python3 1.Initialization/database_preparation.py ' + arguments_list)

if SAMPLES_PROCESS_STEP == 'YES':
    print('Processing Samples')
    if not isdir(USER_FASTQ_FOLDER):
        print('Specified Directory with FASTQ files not present')
        print('Exiting')
        exit(1)
    else:
        arguments_list = ' '.join([CLUSTERING_TOOL, MAXDIFF, USER_FASTQ_FOLDER, TRIM_SCORE,
                                   MINMERGELEN, MAXMERGELEN, FORWARD_TRIM, REVERSE_TRIM, EXPECTED_ERROR_RATE, THREADS,
                                   MINPCTID
                                   ])
        system('python3 2.ASV-Creation/process_samples.py ' + arguments_list)
elif SAMPLES_PROCESS_STEP == 'NO':
    print('Skipping Processing of Samples')

if ASV_CREATION_STEP == 'YES':
    print('Creating ASVs')
    if not isdir(USER_FASTQ_FOLDER):
        print('Specified Directory with FASTQ files not present')
        print('Exiting')
        exit(1)
    else:
        arguments_list = ' '.join([USER_FASTQ_FOLDER, CLUSTERING_TOOL, THREADS, MIN_ZOTU_SIZE,
                                   SORT_ME_RNA_DB1, SORT_ME_RNA_DB2, SORT_ME_RNA_TOOL
                                   ])
        system('python3 2.ASV-Creation/create_ASVs.py ' + arguments_list)
elif ASV_CREATION_STEP == 'NO':
    print('Skipping Creation of ASVs')
