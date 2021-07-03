from os.path import isdir, isfile
from os import system


# return list with each line an element, clear of whitespace
def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


config_file_contents = read_file('config_options.txt')
inifile_contents = read_file('tool_and_db_options.ini')
for ini_line in inifile_contents:
    config_file_contents.append(ini_line)
for line in config_file_contents:
    if not line or line[0] == '#':
        continue
    tokens = line.split(':')
    if tokens[0] == 'TESTING_MODE':
        TESTING_MODE = tokens[1]
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
    elif tokens[0] == 'MIN_ZOTU_SIZE':
        MIN_ZOTU_SIZE = tokens[1]
    elif tokens[0] == 'MATCHING_STEP':
        MATCHING_STEP = tokens[1]
    elif tokens[0] == 'ASV_FILE':
        ASV_FILE = tokens[1]
    elif tokens[0] == 'ALIGNMENT_CLASSIFICATION_STEP':
        ALIGNMENT_CLASSIFICATION_STEP = tokens[1]
    elif tokens[0] == 'SILVA_ARB':
        SILVA_ARB = tokens[1]
    elif tokens[0] == 'SINA_EXECUTABLE':
        SINA_EXECUTABLE = tokens[1]
    elif tokens[0] == 'INPUT_FASTA_ALI_CLASS':
        INPUT_FASTA_ALI_CLASS = tokens[1]
    elif tokens[0] == 'OUTPUT_FASTA_ALI_CLASS':
        OUTPUT_FASTA_ALI_CLASS = tokens[1]
    elif tokens[0] == 'PDF_REGION_OUTPUT':
        PDF_REGION_OUTPUT = tokens[1]
    elif tokens[0] == 'EXTRACTION_STEP':
        EXTRACTION_STEP = tokens[1]
    elif tokens[0] == 'EXTRACTION_REGION_START':
        EXTRACTION_REGION_START = tokens[1]
    elif tokens[0] == 'EXTRACTION_REGION_END':
        EXTRACTION_REGION_END = tokens[1]
    elif tokens[0] == 'EXTRACTION_REGION_LIMIT':
        EXTRACTION_REGION_LIMIT = tokens[1]
    elif tokens[0] == 'INPUT_FASTA_EXTRACTION':
        INPUT_FASTA_EXTRACTION = tokens[1]
    elif tokens[0] == 'OUTPUT_FASTA_EXTRACTION':
        OUTPUT_FASTA_EXTRACTION = tokens[1]
    elif tokens[0] == 'TAXONOMIC_CLUSTERING_STEP':
        TAXONOMIC_CLUSTERING_STEP = tokens[1]
    elif tokens[0] == 'CLUSTERING_DIRECTORY':
        CLUSTERING_DIRECTORY = tokens[1]
    elif tokens[0] == 'INPUT_FASTA_CLUSTERING':
        INPUT_FASTA_CLUSTERING = tokens[1]
    elif tokens[0] == 'FAMILY_IDENTITY':
        FAMILY_IDENTITY = tokens[1]
    elif tokens[0] == 'GENERA_IDENTITY':
        GENERA_IDENTITY = tokens[1]
    elif tokens[0] == 'SPECIES_IDENTITY':
        SPECIES_IDENTITY = tokens[1]
    elif tokens[0] == 'RESULTS_CREATION_STEP':
        RESULTS_CREATION_STEP = tokens[1]
    elif tokens[0] == 'OUTPUT_ASV_FASTA_WITH_TAXONOMY':
        OUTPUT_ASV_FASTA_WITH_TAXONOMY = tokens[1]
    elif tokens[0] == 'INPUT_FASTA_CLUSTERING':
        INPUT_FASTA_CLUSTERING = tokens[1]
    elif tokens[0] == 'OUTPUT_ASV_TABLE':
        OUTPUT_ASV_TABLE = tokens[1]
    elif tokens[0] == 'OUTPUT_FOLDER':
        OUTPUT_FOLDER = tokens[1]
    elif tokens[0] == 'KRONA_TOOL':
        KRONA_TOOL = tokens[1]
    elif tokens[0] == 'RAPID_NJ':
        RAPID_NJ = tokens[1]
    elif tokens[0] == 'OUTPUT_SOTU_FASTA_WITH_TAXONOMY':
        OUTPUT_SOTU_FASTA_WITH_TAXONOMY = tokens[1]
    else:
        print('Configuration File Not valid')
        print('Option ' + tokens[0] + ' not recognised')
        print('Exiting')
        exit(1)

print('Configuration File Valid and Complete')

if TESTING_MODE == 'YES':
    print('This is the testing mode of the TIC-Pipeline.')
    arguments_list = ' '.join([SILVA_ARB, SINA_EXECUTABLE, SORT_ME_RNA_DB1, SORT_ME_RNA_DB2,
                               SORT_ME_RNA_TOOL, CLUSTERING_TOOL, RAPID_NJ
                               ])
    system('python3 0.Setup_and_Testing/testing.py ' + arguments_list)
    exit()
elif TESTING_MODE == 'NO':
    print('This is the production mode of the TIC-Pipeline.')

if SAMPLES_PROCESS_STEP == 'YES':
    print('Processing Samples')
    if not isdir(USER_FASTQ_FOLDER):
        print('Specified Directory with FASTQ files not present')
        print('Exiting')
        exit(1)
    if int(FORWARD_TRIM) < 5:
        print('FORWARD_TRIM is <5')
        print('Exiting')
        exit(1)
    if int(FORWARD_TRIM) > 25:
        print('FORWARD_TRIM is >25')
        print('Exiting')
        exit(1)
    if int(REVERSE_TRIM) < 5:
        print('REVERSE_TRIM is <5')
        print('Exiting')
        exit(1)
    if int(REVERSE_TRIM) > 25:
        print('REVERSE_TRIM is >25')
        print('Exiting')
        exit(1)
    if int(TRIM_SCORE) < 3:
        print('REVERSE_TRIM is <3')
        print('Exiting')
        exit(1)
    if int(TRIM_SCORE) > 20:
        print('REVERSE_TRIM is >20')
        print('Exiting')
        exit(1)
    else:
        arguments_list = ' '.join([CLUSTERING_TOOL, MAXDIFF, USER_FASTQ_FOLDER, TRIM_SCORE,
                                   MINMERGELEN, MAXMERGELEN, FORWARD_TRIM, REVERSE_TRIM, EXPECTED_ERROR_RATE, THREADS,
                                   MINPCTID
                                   ])
        system('python3 1.ASV-Creation/process_samples.py ' + arguments_list)
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
                                   SORT_ME_RNA_DB1, SORT_ME_RNA_DB2, SORT_ME_RNA_TOOL, RAPID_NJ
                                   ])
        system('python3 1.ASV-Creation/create_ASVs.py ' + arguments_list)
elif ASV_CREATION_STEP == 'NO':
    print('Skipping Creation of ASVs')

if ALIGNMENT_CLASSIFICATION_STEP == 'YES':
    print('Classifying with SINA and SILVA ARB')
    if not isfile(SILVA_ARB):
        print('Specified SILVA_ARB File not present')
        print('Exiting')
        exit(1)
    if not isfile(SINA_EXECUTABLE):
        print('Specified SINA_EXECUTABLE not present')
        print('Exiting')
        exit(1)
    if not isfile(INPUT_FASTA_ALI_CLASS):
        print('Specified INPUT_FASTA_ALI_CLASS File not present')
        print('Exiting')
        exit(1)
    else:
        arguments_list = ' '.join([SILVA_ARB, SINA_EXECUTABLE, INPUT_FASTA_ALI_CLASS, PDF_REGION_OUTPUT,
                                   OUTPUT_FASTA_ALI_CLASS])
        system('python3 2.Taxonomy-Classification/create_sina_alignment.py ' + arguments_list)
elif ALIGNMENT_CLASSIFICATION_STEP == 'NO':
    print('Skipping Alignment and Classification Step')


if EXTRACTION_STEP == 'YES':
    print('Region Extraction')
    if not isfile(INPUT_FASTA_EXTRACTION):
        print('Specified INPUT_FASTA_EXTRACTION File not present')
        print('Exiting')
        exit(1)
    if int(EXTRACTION_REGION_START) > 50000 or int(EXTRACTION_REGION_START) < 0:
        print('EXTRACTION_REGION_START over the limits of 0, 50000')
        print('Exiting')
        exit(1)
    if int(EXTRACTION_REGION_END) > 50000 or int(EXTRACTION_REGION_END) < 0:
        print('EXTRACTION_REGION_END over the limits of 0, 50000')
        print('Exiting')
        exit(1)
    if int(EXTRACTION_REGION_START) >= int(EXTRACTION_REGION_END):
        print('Specified EXTRACTION_REGION_START >=  EXTRACTION_REGION_END')
        print('Exiting')
        exit(1)
    else:
        arguments_list = ' '.join([INPUT_FASTA_EXTRACTION, EXTRACTION_REGION_START, EXTRACTION_REGION_END,
                                   EXTRACTION_REGION_LIMIT, OUTPUT_FASTA_EXTRACTION])
        system('python3 2.Taxonomy-Classification/extract_regions.py ' + arguments_list)
        OUTPUT_CSV_ALI_CLASS = OUTPUT_FASTA_ALI_CLASS.split('.')[0] + '.csv'
        arguments_list = ' '.join([OUTPUT_FASTA_EXTRACTION, OUTPUT_CSV_ALI_CLASS])
        system('python3 2.Taxonomy-Classification/update_taxonomy.py ' + arguments_list)
elif EXTRACTION_STEP == 'NO':
    print('Skipping Region Extraction Step')

if TAXONOMIC_CLUSTERING_STEP == 'YES':
    print('Taxonomic Clustering')
    if not isfile(INPUT_FASTA_CLUSTERING):
        print('Specified INPUT_FASTA_CLUSTERING File not present')
        print('Exiting')
        exit(1)
    if int(FAMILY_IDENTITY) > 100 or int(FAMILY_IDENTITY) < 0:
        print('FAMILY_IDENTITY over the limits of 0, 100')
        print('Exiting')
        exit(1)
    if int(GENERA_IDENTITY) > 100 or int(GENERA_IDENTITY) < 0:
        print('GENERA_IDENTITY over the limits of 0, 100')
        print('Exiting')
        exit(1)
    if int(SPECIES_IDENTITY) > 100 or int(SPECIES_IDENTITY) < 0:
        print('SPECIES_IDENTITY over the limits of 0, 100')
        print('Exiting')
        exit(1)
    else:
        arguments_list = ' '.join([CLUSTERING_DIRECTORY, INPUT_FASTA_CLUSTERING])
        cmd = 'python3 3.Taxonomy-Informed-Clustering/split_based_on_taxonomy.py '
        cmd += ' -d ' + CLUSTERING_DIRECTORY + ' -i ' + INPUT_FASTA_CLUSTERING
        system(cmd)
        arguments_list = ' '.join([CLUSTERING_DIRECTORY, FAMILY_IDENTITY, GENERA_IDENTITY, SPECIES_IDENTITY])
        cmd = 'python3 3.Taxonomy-Informed-Clustering/complex_TIC.py '
        cmd += ' -f ' + FAMILY_IDENTITY + ' -g ' + GENERA_IDENTITY + ' -s ' + SPECIES_IDENTITY
        cmd += ' -t ' + CLUSTERING_TOOL + ' -n ' + THREADS + ' -d ' + CLUSTERING_DIRECTORY
        system(cmd)
elif TAXONOMIC_CLUSTERING_STEP == 'NO':
    print('Skipping Taxonomic Clustering Step')

if RESULTS_CREATION_STEP == 'YES':
    print('Creating Results')
    if isdir(OUTPUT_FOLDER):
        print('Specified OUTPUT_FOLDER Directory already present')
        print('Exiting')
        exit(1)
    elif not isdir(CLUSTERING_DIRECTORY):
        print('Specified CLUSTERING_DIRECTORY Directory not present')
        print('Exiting')
        exit(1)
    elif not isfile(INPUT_FASTA_CLUSTERING):
        print('Specified INPUT_FASTA_CLUSTERING File not present')
        print('Exiting')
        exit(1)
    else:
        arguments_list = ' '.join([OUTPUT_FOLDER, OUTPUT_ASV_FASTA_WITH_TAXONOMY, OUTPUT_ASV_TABLE,
                                   CLUSTERING_DIRECTORY, INPUT_FASTA_CLUSTERING, KRONA_TOOL,
                                   OUTPUT_SOTU_FASTA_WITH_TAXONOMY])
        system('python3 4.Results_Processing/create_fasta_and_table.py ' + arguments_list)
        arguments_list = ' '.join([INPUT_FASTA_EXTRACTION, OUTPUT_FASTA_EXTRACTION, CLUSTERING_DIRECTORY])
        system('python3 4.Results_Processing/cleaning.py ' + arguments_list)
elif ALIGNMENT_CLASSIFICATION_STEP == 'NO':
    print('Skipping Alignment and Classification Step')
