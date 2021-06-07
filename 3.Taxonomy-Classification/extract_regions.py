import argparse
from os.path import isfile


def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


def count_seq(input_file):
    out_file = open('dataset_extracted.fasta', 'w+')
    ali_contents = read_file(input_file)
    for line in ali_contents:
        if line[0] == '>':
            header = line
        else:
            trimmed_sequence = line[START_REGION: END_REGION]
            collapsed_sequence = trimmed_sequence.replace('-', '').replace('.', '')
            if len(collapsed_sequence) >= BASES_LOW_LIMIT:
                out_file.write(header + '\n')
                out_file.write(collapsed_sequence + '\n')
    out_file.close()


# read arguments for the three levels of similarity
# as well as the absolute path of the MAIN_DIR
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="Input File", type=str)
parser.add_argument("-s", "--start", required=True, help="Start Region", type=int)
parser.add_argument("-e", "--end", required=True, help="End Region", type=int)
parser.add_argument("-l", "--limit", required=True, help="Aligned Bases Limit", type=int)

args = parser.parse_args()

if int(args.start) <= 0 or int(args.end) >= 50000 or int(args.start) >= int(args.end):
    print('Start or End region over the limits of 0, 50000')
    exit()
if not isfile(str(args.input)):
    print('Input file not present')
    exit()


input_file = str(args.input)
START_REGION = int(args.start)
END_REGION = int(args.end)
BASES_REQ = int(args.limit)
BASES_LOW_LIMIT = BASES_REQ * 0.8
count_seq(input_file)
