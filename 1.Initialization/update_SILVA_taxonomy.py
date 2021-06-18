from os import system


# return list with each line an element, clear of whitespace
def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


SILVA_contents = read_file('clean_SILVA_DNA_compressed.fasta')
out_file = open('t.fasta', 'w+')
for line in SILVA_contents:
    if line[0] == '>':
        tokens = line.split()
        new_line = tokens[0] + ';tax=' + '_'.join(tokens[1:]) + ';\n'
        out_file.write(new_line)
    else:
        out_file.write(line + '\n')
out_file.close()

system('mv t.fasta clean_SILVA_DNA_compressed.fasta')
