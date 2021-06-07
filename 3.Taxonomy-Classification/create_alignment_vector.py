import argparse


# return list with each line an element, clear of whitespace
def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


def find_differences(s):
    alphabet = ['A', 'G', 'T', 'C', 'a', 'g', 't', 'c']
    positions = list()
    for i, letter in enumerate(s):
        if letter in alphabet:
            positions.append(i)
    return positions


def create_vector(input_file):
    position_vector = [0] * 50000
    content = read_file(input_file)
    position_vector_file = open("alignment_vector.csv", "w+")
    for i in range(len(content)):
        if(">" not in content[i]):
            align_pos = find_differences(content[i])
            for j in align_pos:
                position_vector[j] = position_vector[j] + 1
    ready_vec = ','.join(str(e) for e in position_vector)
    position_vector_file.write(ready_vec + '\n')
    position_vector_file.close()


# read arguments for the three levels of similarity
# as well as the absolute path of the MAIN_DIR
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_file", required=True, help="Input FASTA file", type=str)
args = parser.parse_args()

input_file = str(args.input_file)

create_vector(input_file)