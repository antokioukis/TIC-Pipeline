import wget
from os.path import isfile
from os import system, remove, chdir
from sys import argv


# return list with each line an element, clear of whitespace
def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


def download_LTP(version):
    LTP_URL = 'https://www.arb-silva.de/fileadmin/silva_databases/previous_living_tree/LTP_release_' + version
    LTP_URL_FASTA = LTP_URL + '/LTPs' + version + '_datasets.fasta.tar.gz'
    try:
        wget.download(LTP_URL_FASTA, out='../0.Template-Data')
    except BaseException:
        return 1
    LTP_SSU_URL = LTP_URL + '/LTPs' + version + '_SSU.csv'
    try:
        wget.download(LTP_SSU_URL, out='../0.Template-Data')
    except BaseException:
        return 1
    return 0


def download_SILVA(version):
    SILVA_URL = 'https://www.arb-silva.de/fileadmin/silva_databases/release_' + version
    SILVA_URL += '/Exports/SILVA_' + version + '_SSURef_NR99_tax_silva.fasta.gz'
    try:
        wget.download(SILVA_URL, out='../0.Template-Data')
    except BaseException:
        return 1
    return 0


def unzip_LTP(version):
    LTP_File = '../0.Template-Data/LTPs' + version + '_datasets.fasta.tar.gz'
    if not isfile(LTP_File):
        print('LTP Not present in 0.Template-Data Directory.')
        print('Please check that your config file has the correct LTP Version')
        return 1
    cmd = 'tar -xzf ' + LTP_File
    try:
        system(cmd)
    except BaseException:
        return 1
    return 0


def unzip_SILVA(version):
    SILVA_File = '../0.Template-Data/SILVA_' + version + '_SSURef_NR99_tax_silva.fasta.gz'
    if not isfile(SILVA_File):
        print('SILVA Not present in 0.Template-Data Directory.')
        print('Please check that your config file has the correct SILVA Version')
        return 1
    cmd = 'gunzip -c ' + SILVA_File + ' > SILVA_' + version + '_SSURef_NR99_tax_silva.fasta'
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
    csv_contents = read_file('../0.Template-Data/LTPs' + version + '_SSU.csv')
    out_file_1 = open('LTP_info.csv', 'w+')
    for line in csv_contents:
        tokens = line.split('\t')
        out_line = tokens[0] + '\t' + tokens[-1] + '\n'
        out_file_1.write(out_line)
    out_file_1.close()
    out_file_2 = open('LTP_species_identifiers.txt', 'w+')
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
    LTP_file_aligned = 'LTPs' + version + '_SSU_aligned.fasta'
    LTP_file_compressed = 'LTPs' + version + '_SSU_compressed.fasta'
    LTP_file_blast = 'LTPs' + version + '_SSU_blastdb.fasta'
    out_file_aligned_name = 'clean_LTP_DNA_aligned.fasta'
    out_file_compressed_name = 'clean_LTP_DNA_compressed.fasta'
    replace_spaces(LTP_file_aligned, out_file_aligned_name)
    replace_spaces(LTP_file_compressed, out_file_compressed_name)
    remove(LTP_file_aligned)
    remove(LTP_file_compressed)
    remove(LTP_file_blast)
    extract_full_taxonomy_information(version)
    top_directory = '..'
    system("python3 update_LTP_taxonomy.py")
    status = create_UDB('clean_LTP_DNA_compressed.fasta', '../3.Database-Match/LTP_compressed.udb')
    if status:
        return 1
    chdir(top_directory)
    remove('./1.Initialization/' + out_file_compressed_name)
    remove('./1.Initialization/LTP_info.csv')
    remove('./1.Initialization/LTP_species_identifiers.txt')
    return 0


def process_SILVA(version):
    SILVA_file_initial = 'SILVA_' + version + '_SSURef_NR99_tax_silva.fasta'
    SILVA_file_compressed_name = 'clean_SILVA_DNA_compressed.fasta'
    replace_spaces(SILVA_file_initial, SILVA_file_compressed_name)
    top_directory = '..'
    system("python3 update_SILVA_taxonomy.py")
    status = create_UDB('clean_SILVA_DNA_compressed.fasta', '../3.Database-Match/SILVA_compressed.udb')
    if status:
        return 1
    chdir(top_directory)
    return 0


CLUSTERING_TOOL = argv[1]
LTP_DOWNLOAD = argv[2]
LTP_UNZIP = argv[3]
LTP_PROCESS = argv[4]
LTP_VERSION = argv[5]
SILVA_DOWNLOAD = argv[6]
SILVA_UNZIP = argv[7]
SILVA_PROCESS = argv[8]
SILVA_VERSION = argv[9]


chdir('1.Initialization')
if LTP_DOWNLOAD == 'YES' and LTP_UNZIP == 'YES' and LTP_PROCESS == 'YES':
    print('LTP VERSION specified:' + LTP_VERSION)
    print('Downloading LTP')
    status = download_LTP(LTP_VERSION)
    if status == 0:
        print('\nLTP Download: Complete')
    else:
        print('\nLTP Download: Failed')
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
