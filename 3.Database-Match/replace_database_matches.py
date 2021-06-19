from sys import argv
from os import system


# return list with each line an element, clear of whitespace
def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


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


DOUBLE_NOT_MATCHED = argv[1]
LTP_SEQUENCES = argv[2]
SILVA_SEQUENCES = argv[3]
LTP_MATCHES = argv[4]
SILVA_MATCHES = argv[5]
REPLACEMENT_OUT_FILE = argv[6]


def replace_LTP_matches():
    out_file = open('3.Database-Match/double_replaced.fasta', 'w+')
    replacement_contents = read_file(LTP_MATCHES)
    LTP_dict = fasta_to_dict(LTP_SEQUENCES)
    for line in replacement_contents:
        tokens = line.split('\t')
        query = tokens[0]
        target = tokens[1].split(';')[0]
        out_file.write('>' + query + '\n')
        out_file.write(LTP_dict[target] + '\n')
    out_file.close()


def replace_SILVA_matches():
    out_file = open('3.Database-Match/double_replaced.fasta', 'a')
    replacement_contents = read_file(SILVA_MATCHES)
    SILVA_dict = fasta_to_dict(SILVA_SEQUENCES)
    for line in replacement_contents:
        tokens = line.split('\t')
        query = tokens[0]
        target = tokens[1].split(';')[0]
        out_file.write('>' + query + '\n')
        out_file.write(SILVA_dict[target] + '\n')
    out_file.close()


def append_not_matched():
    cmd = 'cat 3.Database-Match/double_replaced.fasta 3.Database-Match/not_matched_SILVA.fasta>> ' + REPLACEMENT_OUT_FILE
    system(cmd)


replace_LTP_matches()
replace_SILVA_matches()
append_not_matched()
