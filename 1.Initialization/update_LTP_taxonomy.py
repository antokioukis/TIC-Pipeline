from os import system


def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


ltp_info = read_file('LTP_info.csv')
ltp_species = read_file('LTP_species_identifiers.txt')

ltp_dict = dict()
for line in ltp_info:
    tokens = line.split('\t')
    ltp_dict[tokens[0]] = tokens[1]


species_dict = dict()
for line in ltp_species:
    tokens = line.split('\t')
    species_dict[tokens[0]] = tokens[1].replace(' ', '_')


ltp_file = read_file('clean_LTP_DNA_aligned.fasta')
out_file = open('LTP_clean_ready.fasta', 'w+')
for line in ltp_file:
    if line[0] == '>':
        seq_name = line.split('\t')[0][1:]
        new_line = '>' + seq_name + ';tax=' + ltp_dict[seq_name] + ';' + species_dict[seq_name] + ';\n'
        out_file.write(new_line)
    else:
        out_file.write(line + '\n')
out_file.close()

system('mv LTP_clean_ready.fasta clean_LTP_DNA_aligned.fasta')


compressed_file = read_file('clean_LTP_DNA_compressed.fasta')
out_file = open('t.fasta', 'w+')
for line in compressed_file:
    if line[0] == '>':
        seq_name = line.split('\t')[0][1:]
        new_line = '>' + seq_name + ';tax=' + ltp_dict[seq_name] + ';' + species_dict[seq_name] + ';\n'
        out_file.write(new_line)
    else:
        out_file.write(line.replace('-', '').replace('U', 'T') + '\n')
out_file.close()
system('mv t.fasta clean_LTP_DNA_compressed.fasta')