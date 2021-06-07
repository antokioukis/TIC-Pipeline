from tqdm import tqdm


def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content

crashed_dict = dict()
crashed_csv = read_file('total_crashed_LTP_SILVA_aligned.csv')[1:]
for i in tqdm(range(len(crashed_csv))):
    curr_line = crashed_csv[i]
    total_name, new_taxonomy = curr_line.split(' ', 1)
    total_name_no_tax = total_name.split('tax=')[0]
    crashed_dict[total_name_no_tax] = new_taxonomy


filepath = 'trimmed_crashed.fasta'
out_fasta = open('trimmed_crashed_new_taxonomy.fasta', 'w+')
with open(filepath) as fp:
    line = fp.readline()
    while line:
        if line[0] == '>':
            total_name_no_tax = line.split('tax=')[0][1:]
            out_fasta.write('>' + total_name_no_tax + 'tax=' + crashed_dict[total_name_no_tax] + '\n')
        else:
            new_line = line.replace('-','')
            new_line = new_line.replace('U','T')
            out_fasta.write(new_line)
        line = fp.readline()


out_fasta.close()

big_dict = dict()
big_csv = read_file('total_no_matches_LTP_SILVA_aligned.csv')[1:]
for i in tqdm(range(len(big_csv))):
    curr_line = big_csv[i]
    total_name, new_taxonomy = curr_line.split(' ', 1)
    total_name_no_tax = total_name.split('tax=')[0]
    big_dict[total_name_no_tax] = new_taxonomy


filepath = 'trimmed_big.fasta'
out_fasta = open('trimmed_big_new_taxonomy.fasta', 'w+')
with open(filepath) as fp:
    line = fp.readline()
    while line:
        if line[0] == '>':
            total_name_no_tax = line.split('tax=')[0][1:]
            out_fasta.write('>' + total_name_no_tax + 'tax=' + big_dict[total_name_no_tax] + '\n')
        else:
            new_line = line.replace('-','')
            new_line = new_line.replace('U','T')
            out_fasta.write(new_line)
        line = fp.readline()


out_fasta.close()

filepath = 'trimmed_replaced.fasta'
out_fasta = open('trimmed_replaced_new_taxonomy.fasta', 'w+')
with open(filepath) as fp:
    line = fp.readline()
    while line:
        if line[0] == '>':
            total_name_no_tax = line.split('tax=')[0][1:]
            out_fasta.write(line)
        else:
            new_line = line.replace('-','')
            new_line = new_line.replace('U','T')
            out_fasta.write(new_line)
        line = fp.readline()


out_fasta.close()