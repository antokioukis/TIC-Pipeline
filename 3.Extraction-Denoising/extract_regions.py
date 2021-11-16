from sys import argv


def count_seq():
    out_file = open(OUTPUT_FASTA_EXTRACTION, 'w+')
    with open(INPUT_FASTA_EXTRACTION) as file_one:
        for line in file_one:
            if line[0] == '>':
                out_file.write(line)
            else:
                trimmed_sequence = line[EXTRACTION_REGION_START: EXTRACTION_REGION_END]
                collapsed_sequence = trimmed_sequence.replace('-', '').replace('.', '')
                out_file.write(collapsed_sequence + '\n')
    out_file.close()


print('>>> Extracting regions based on user input...')
INPUT_FASTA_EXTRACTION = argv[1]
EXTRACTION_REGION_START = int(argv[2])
EXTRACTION_REGION_END = int(argv[3])
EXTRACTION_REGION_LIMIT = int(argv[4])
BASES_LOW_LIMIT = EXTRACTION_REGION_LIMIT * 0.8
OUTPUT_FASTA_EXTRACTION = argv[5]

count_seq()

print('\tDone')
