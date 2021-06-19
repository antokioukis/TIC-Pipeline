from sys import argv


def fasta_to_dict(fil):
    dic = {}
    cur_scaf = ''
    cur_seq = []
    for line in open(fil):
        if line.startswith(">") and cur_scaf == '':
            cur_scaf = line.split(' ')[0]
        elif line.startswith(">") and cur_scaf != '':
            dic[cur_scaf] = ''.join(cur_seq)
            cur_scaf = line.split(' ')[0]
            cur_seq = []
        else:
            cur_seq.append(line.rstrip())
    dic[cur_scaf] = ''.join(cur_seq)
    new_dict = dict()
    for key, value in dic.items():
        new_key = key.split(';')[0][1:]
        # print(new_key)
        new_dict[new_key] = value
    return new_dict


def count_seq():
    out_file = open(OUTPUT_FASTA_EXTRACTION, 'w+')
    ali_contents = fasta_to_dict(INPUT_FASTA_EXTRACTION)
    for key, value in ali_contents.items():
        trimmed_sequence = value[EXTRACTION_REGION_START: EXTRACTION_REGION_END]
        collapsed_sequence = trimmed_sequence.replace('-', '').replace('.', '')
        if len(collapsed_sequence) >= BASES_LOW_LIMIT:
            out_file.write('>' + key)
            out_file.write(collapsed_sequence + '\n')
    out_file.close()


INPUT_FASTA_EXTRACTION = argv[1]
EXTRACTION_REGION_START = int(argv[2])
EXTRACTION_REGION_END = int(argv[3])
EXTRACTION_REGION_LIMIT = int(argv[4])
BASES_LOW_LIMIT = EXTRACTION_REGION_LIMIT * 0.8
OUTPUT_FASTA_EXTRACTION = argv[5]

count_seq()