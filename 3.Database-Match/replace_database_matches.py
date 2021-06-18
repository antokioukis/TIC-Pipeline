import argparse


# return list with each line an element, clear of whitespace
def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


# read arguments for the three levels of similarity
# as well as the absolute path of the MAIN_DIR
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", required=True, help="Mode: LTP or SILVA", type=str)
args = parser.parse_args()

if not (args.mode == 'LTP') and not(args.mode == 'SILVA'):
    print('Mode not used by program, available options (LTP, SILVA)')
    exit()

MODE = str(args.mode)

LTP_dict = dict()
LTP_contents = read_file('../1.Initialization/LTP_archaea_compressed.fasta')
for i in range(0, len(LTP_contents), 2):
    header = LTP_contents[i][1:]
    sequence = LTP_contents[i+1]
    LTP_dict[header] = sequence


SILVA_dict = dict()
SILVA_contents = read_file('../1.Initialization/SILVA_archaea_compressed.fasta')
for i in range(0, len(SILVA_contents), 2):
    header = SILVA_contents[i][1:]
    sequence = SILVA_contents[i+1]
    SILVA_dict[header] = sequence


if MODE == 'LTP':
    file_m2 = 'archaea_LTP.m2'
    curr_dict = LTP_dict
    out_file = open('archaea_replaced_LTP.fasta', 'w+')
elif MODE == 'SILVA':
    out_file = open('archaea_replaced_SILVA.fasta', 'w+')
    curr_dict = SILVA_dict
    file_m2 = 'archaea_SILVA.m2'

m2_content = read_file(file_m2)
for line in m2_content:
    original_header, match_header = line.split('\t')[:2]
    out_file.write('>' + original_header + '\n')
    out_file.write(curr_dict[match_header] + '\n')

out_file.close()