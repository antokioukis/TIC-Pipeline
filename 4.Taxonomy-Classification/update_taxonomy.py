from tqdm import tqdm


def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


sina_dict = dict()
sina_csv = read_file('sina_output.csv')[1:]
for i in tqdm(range(len(sina_csv))):
    curr_line = sina_csv[i]
    line_tokens = curr_line.split(',')
    original_header = line_tokens[0]
    new_taxonomy = line_tokens[6]
    sina_dict[original_header] = new_taxonomy


#filepath = 'dataset_extracted.fasta'
filepath = 'sina_output.fasta'
out_fasta = open('dataset_extracted_new_taxonomy.fasta', 'w+')
with open(filepath) as fp:
    line = fp.readline()
    while line:
        if line[0] == '>':
            new_header = line[:-1] + ';tax=' + sina_dict[line[1:-1]].replace(' ', '') + '\n'
            out_fasta.write(new_header)
        else:
            out_fasta.write(line)
        line = fp.readline()


out_fasta.close()
