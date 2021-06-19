import argparse
from tqdm import tqdm


def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


def check_valid_names(input_taxonomy):
    taxo_tokens = input_taxonomy.split(';')
    valid_names_list = list()
    phylum = ''
    class_s = ''
    order_o = ''
    family = ''
    genus = ''
    if len(taxo_tokens) >= 1:
        try:
            domain = taxo_tokens[0].split()[0]
        except BaseException:
            domain = ''
    if len(taxo_tokens) >= 2:
        try:
            phylum = taxo_tokens[1].split()[0]
        except BaseException:
            phylum = ''
    if len(taxo_tokens) >= 3:
        try:
            class_s = taxo_tokens[2].split()[0]
        except BaseException:
            class_s = ''
    if len(taxo_tokens) >= 4:
        try:
            order_o = taxo_tokens[3].split()[0]
        except BaseException:
            order_o = ''
    if len(taxo_tokens) >= 5:
        try:
            family = taxo_tokens[4].split()[0]
        except BaseException:
            family = ''
    if len(taxo_tokens) >= 6:
        try:
            genus = taxo_tokens[5].split()[0]
        except BaseException:
            genus = ''
    if domain:
        valid_names_list.append(domain)
    else:
        return('other.fasta')
    if phylum:
        valid_names_list.append(phylum)
    else:
        return('_'.join(valid_names_list) + '.fasta')
    if class_s:
        valid_names_list.append(class_s)
    else:
        return('_'.join(valid_names_list) + '.fasta')
    if order_o:
        valid_names_list.append(order_o)
    else:
        return('_'.join(valid_names_list) + '.fasta')
    if family:
        valid_names_list.append(family)
    else:
        return('_'.join(valid_names_list) + '.fasta')
    if genus:
        valid_names_list.append(genus)
    return('_'.join(valid_names_list) + '.fasta')


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--data_dir", required=True, help="Data Directory")
parser.add_argument("-i", "--input", required=True, help="Input File")

args = parser.parse_args()
MAIN_DIR = args.data_dir + '/'
input_file = args.input

input_contents = read_file(input_file)
for i in tqdm(range(0, len(input_contents), 2)):
    header = input_contents[i]
    sequence = input_contents[i+1]
    curr_taxonomy = header.split('tax=')[1]
    out_file_name = check_valid_names(curr_taxonomy)
    out_file = open(MAIN_DIR + out_file_name, 'a+')
    new_header = header.split('tax=')[0] + 'tax=' + out_file_name.split('.')[0].replace('_', ';') + ';'
    out_file.write(new_header + '\n')
    out_file.write(sequence + '\n')
    out_file.close()
