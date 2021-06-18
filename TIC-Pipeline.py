import wget
from glob import glob
from os.path import isfile, isdir
from os import system, remove, chdir, getcwd


# return list with each line an element, clear of whitespace
def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


def download_LTP(version):
    LTP_URL = 'https://www.arb-silva.de/fileadmin/silva_databases/previous_living_tree/LTP_release_' + version
    LTP_URL += '/LTPs' + version + '_datasets.fasta.tar.gz'
    try:
        wget.download(LTP_URL, out='0.Template-Data')
    except BaseException:
        return 1
    return 0


def download_SILVA(version):
    SILVA_URL = 'https://www.arb-silva.de/fileadmin/silva_databases/release_' + version
    SILVA_URL += '/Exports/SILVA_' + version + '_SSURef_NR99_tax_silva.fasta.gz'
    try:
        wget.download(SILVA_URL, out='0.Template-Data')
    except BaseException:
        return 1
    return 0


def unzip_LTP(version):
    LTP_File = '0.Template-Data/LTPs' + LTP_VERSION + '_datasets.fasta.tar.gz'
    if not isfile(LTP_File):
        print('LTP Not present in 0.Template-Data Directory.')
        print('Please check that your config file has the correct LTP Version')
        return 1
    cmd = 'tar -xzf 0.Template-Data/LTPs' + version + '_datasets.fasta.tar.gz -C 1.Initialization'
    try:
        system(cmd)
    except BaseException:
        return 1
    return 0


def unzip_SILVA(version):
    SILVA_File = '0.Template-Data/SILVA_' + version + '_SSURef_NR99_tax_silva.fasta.gz'
    if not isfile(SILVA_File):
        print('SILVA Not present in 0.Template-Data Directory.')
        print('Please check that your config file has the correct SILVA Version')
        return 1
    cmd = 'gunzip -c 0.Template-Data/SILVA_' + version + '_SSURef_NR99_tax_silva.fasta.gz > '
    cmd += './1.Initialization/SILVA_' + version + '_SSURef_NR99_tax_silva.fasta'
    try:
        system(cmd)
    except BaseException:
        return 1
    return 0


def replace_spaces(input_file, output_file_name):
    output_file = open(output_file_name, 'w+')
    with open(input_file) as fp:
        while True:
            line = fp.readline()
            if not line:
                break
            if line[0] == '>':
                output_file.write(line)
            else:
                new_line = line.replace(' ', '').replace('U', 'T').replace('u', 't')
                output_file.write(new_line)
    output_file.close()


def extract_full_taxonomy_information(version):
    csv_contents = read_file('0.Template-Data/LTPs' + version + '_SSU.csv')
    out_file_1 = open('./1.Initialization/LTP_info.csv', 'w+')
    for line in csv_contents:
        tokens = line.split('\t')
        out_line = tokens[0] + '\t' + tokens[-1] + '\n'
        out_file_1.write(out_line)
    out_file_1.close()
    out_file_2 = open('./1.Initialization/LTP_species_identifiers.txt', 'w+')
    for line in csv_contents:
        tokens = line.split('\t')
        out_line = tokens[0] + '\t' + tokens[4] + '\n'
        out_file_2.write(out_line)
    out_file_2.close()


def create_UDB(input_file, output_udb):
    cmd = CLUSTERING_TOOL + ' -makeudb_usearch ' + input_file + ' -output '
    cmd += output_udb + ' 1>/dev/null 2>/dev/null'
    try:
        system(cmd)
    except BaseException:
        print('Creation of UDB database failed')
        return 1


def process_LTP(version):
    LTP_file_aligned = './1.Initialization/LTPs' + version + '_SSU_aligned.fasta'
    LTP_file_compressed = './1.Initialization/LTPs' + version + '_SSU_compressed.fasta'
    LTP_file_blast = '1.Initialization/LTPs' + version + '_SSU_blastdb.fasta'
    out_file_aligned_name = '1.Initialization/clean_LTP_DNA_aligned.fasta'
    out_file_compressed_name = '1.Initialization/clean_LTP_DNA_compressed.fasta'
    replace_spaces(LTP_file_aligned, out_file_aligned_name)
    replace_spaces(LTP_file_compressed, out_file_compressed_name)
    remove(LTP_file_aligned)
    remove(LTP_file_compressed)
    remove(LTP_file_blast)
    extract_full_taxonomy_information(version)
    top_directory = getcwd()
    chdir('1.Initialization')
    system("python3 update_LTP_taxonomy.py")
    status = create_UDB('clean_LTP_DNA_compressed.fasta', '../3.Database-Match/LTP_compressed.udb')
    if status:
        return 1
    chdir(top_directory)
    remove(out_file_compressed_name)
    remove('./1.Initialization/LTP_info.csv')
    remove('./1.Initialization/LTP_species_identifiers.txt')
    return 0


def process_SILVA(version):
    SILVA_file_initial = './1.Initialization/SILVA_' + version + '_SSURef_NR99_tax_silva.fasta'
    SILVA_file_compressed_name = '1.Initialization/clean_SILVA_DNA_compressed.fasta'
    replace_spaces(SILVA_file_initial, SILVA_file_compressed_name)
    top_directory = getcwd()
    chdir('1.Initialization')
    system("python3 update_SILVA_taxonomy.py")
    status = create_UDB('clean_SILVA_DNA_compressed.fasta', '../3.Database-Match/SILVA_compressed.udb')
    if status:
        return 1
    chdir(top_directory)
    return 0


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
    cmd += ' -zotus ' + USER_FASTQ_FOLDER + '/zotus.fasta -tabbedout ' + USER_FASTQ_FOLDER + '/denoising.tab '
    cmd += '> /dev/null 2>&1'
    system(cmd)


def create_ASVs():
    merging_all_samples()
    dereplication_merged()
    sort_merged()
    remove(USER_FASTQ_FOLDER + '/merged.fasta')
    remove(USER_FASTQ_FOLDER + '/dereped.fasta')
    unoise()


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
    else:
        print('Configuration File Not valid')
        print('Option ' + tokens[0] + ' Not recognised')
        print('Exiting')
        exit(1)

print('Configuration File Valid and Complete')

if LTP_DOWNLOAD == 'YES' and LTP_UNZIP == 'YES' and LTP_PROCESS == 'YES':
    print('LTP VERSION specified:' + LTP_VERSION)
    print('Downloading LTP')
    status = download_LTP(LTP_VERSION)
    if status == 0:
        print('LTP Download: Complete')
    else:
        print('LTP Download: Failed')
        exit(1)
    print('Unzipping LTP')
    status = unzip_LTP(LTP_VERSION)
    if status == 0:
        print('LTP Unzip: Complete')
    else:
        print('LTP Unzip: Failed')
    print('Processing LTP')
    status = process_LTP(LTP_VERSION)
    if status == 0:
        print('LTP Process: Complete')
    else:
        print('LTP Process: Failed')
        exit(1)
elif LTP_DOWNLOAD == 'NO' and LTP_UNZIP == 'YES' and LTP_PROCESS == 'YES':
    print('Skipping LTP Download')
    print('Unzipping LTP')
    status = unzip_LTP(LTP_VERSION)
    if status == 0:
        print('LTP Unzip: Complete')
    else:
        print('LTP Unzip: Failed')
    print('Processing LTP')
    status = process_LTP(LTP_VERSION)
    if status == 0:
        print('LTP Process: Complete')
    else:
        print('LTP Process: Failed')
        exit(1)
elif LTP_DOWNLOAD == 'NO' and LTP_UNZIP == 'NO' and LTP_PROCESS == 'YES':
    print('Skipping LTP Download')
    print('Skipping LTP Unzip')
    print('Processing LTP')
    status = process_LTP(LTP_VERSION)
    if status == 0:
        print('LTP Process: Complete')
    else:
        print('LTP Process: Failed')
        exit(1)
elif LTP_DOWNLOAD == 'NO' and LTP_UNZIP == 'NO' and LTP_PROCESS == 'NO':
    print('Skipping LTP Download')
    print('Skipping LTP Unzip')
    print('Skipping LTP Processing')

else:
    print('Combination of options for LTP is not valid')
    print('Exiting')
    exit(1)

if SILVA_DOWNLOAD == 'YES' and SILVA_UNZIP == 'YES' and SILVA_PROCESS == 'YES':
    print('SILVA VERSION specified:' + SILVA_VERSION)
    print('Downloading SILVA')
    status = download_SILVA(SILVA_VERSION)
    if status == 0:
        print('SILVA Download: Complete')
    else:
        print('SILVA Download: Failed')
    print('Unzipping SILVA')
    status = unzip_SILVA(SILVA_VERSION)
    if status == 0:
        print('SILVA Unzip: Complete')
    else:
        print('SILVA Unzip: Failed')
    print('Processing SILVA')
    status = process_SILVA(SILVA_VERSION)
    if status == 0:
        print('SILVA Process: Complete')
    else:
        print('SILVA Process: Failed')
elif SILVA_DOWNLOAD == 'NO' and SILVA_UNZIP == 'YES' and SILVA_PROCESS == 'YES':
    print('Skipping SILVA Download')
    print('Unzipping SILVA')
    status = unzip_SILVA(SILVA_VERSION)
    if status == 0:
        print('SILVA Unzip: Complete')
    else:
        print('SILVA Unzip: Failed')
    print('Processing SILVA')
    status = process_SILVA(SILVA_VERSION)
    if status == 0:
        print('SILVA Process: Complete')
    else:
        print('SILVA Process: Failed')
elif SILVA_DOWNLOAD == 'NO' and SILVA_UNZIP == 'NO' and SILVA_PROCESS == 'YES':
    print('Skipping SILVA Download')
    print('Skipping SILVA Unzip')
    print('Processing SILVA')
    status = process_SILVA(SILVA_VERSION)
    if status == 0:
        print('SILVA Process: Complete')
    else:
        print('SILVA Process: Failed')
elif SILVA_DOWNLOAD == 'NO' and SILVA_UNZIP == 'NO' and SILVA_PROCESS == 'NO':
    print('Skipping SILVA Download')
    print('Skipping SILVA Unzip')
    print('Skipping SILVA Processing')
else:
    print('Combination of options for SILVA is not valid')
    print('Exiting')
    exit(1)

if SAMPLES_PROCESS_STEP == 'YES':
    print('Processing Samples')
    if not isdir(USER_FASTQ_FOLDER):
        print('Specified Directory with FASTQ files not present')
        print('Exiting')
        exit(1)
    else:
        process_samples()
elif SAMPLES_PROCESS_STEP == 'NO':
    print('Skipping Processing of Samples')

if ASV_CREATION_STEP:
    print('Creating ASVs')
    if not isdir(USER_FASTQ_FOLDER):
        print('Specified Directory with FASTQ files not present')
        print('Exiting')
        exit(1)
    else:
        create_ASVs()
