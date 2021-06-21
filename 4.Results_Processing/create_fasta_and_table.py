from sys import argv
from os import mkdir, system
from glob import glob


def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


def fasta2dict(fil):
    dic = {}
    cur_scaf = ''
    cur_seq = []
    for line in open(fil):
        if line.startswith(">") and cur_scaf == '':
            cur_scaf = line[1:].rstrip()
        elif line.startswith(">") and cur_scaf != '':
            dic[cur_scaf] = ''.join(cur_seq)
            cur_scaf = line[1:].rstrip()
            cur_seq = []
        else:
            cur_seq.append(line.rstrip())
    dic[cur_scaf] = ''.join(cur_seq)
    new_dict = dict()
    for key, value in dic.items():
        new_key = key.split(';')[0]
        new_dict[new_key] = value
    return new_dict


OUTPUT_FOLDER = argv[1]
OUTPUT_ASV_FASTA_WITH_TAXONOMY = argv[2]
OUTPUT_ASV_TABLE = argv[3]
CLUSTERING_DIRECTORY = argv[4]
INPUT_FASTA_CLUSTERING = argv[5]
KRONA_TOOL = argv[6]

INPUT_FASTA_EXTRACTION = argv[7]
OUTPUT_FASTA_EXTRACTION = argv[8]
CLUSTERING_DIRECTORY = argv[9]

mkdir(OUTPUT_FOLDER)
zotus_seqs_dict = fasta2dict(INPUT_FASTA_CLUSTERING)
all_stats = glob(CLUSTERING_DIRECTORY + '/species_stats/**/*.stats', recursive=True)
output_fasta = open(OUTPUT_FOLDER + '/' + OUTPUT_ASV_FASTA_WITH_TAXONOMY, 'w+')
for curr_stats in all_stats:
    stats_contents = read_file(curr_stats)
    for line in stats_contents:
        if not line:
            continue
        zotu_with_taxonomy = line.split('\t')[1]
        clean_zotu_name = zotu_with_taxonomy.split(';')[0]
        output_fasta.write('>' + zotu_with_taxonomy + '\n')
        output_fasta.write(zotus_seqs_dict[clean_zotu_name] + '\n')
output_fasta.close()

zotus_with_taxonomy_contents = read_file(OUTPUT_FOLDER + '/' + OUTPUT_ASV_FASTA_WITH_TAXONOMY)
zotus_taxonomy_dict = dict()
for line in zotus_with_taxonomy_contents:
    if line[0] == '>':
        tokens = line.split('tax=')
        zotu_name = tokens[0][1:-1]
        taxonomy = tokens[1]
        zotus_taxonomy_dict[zotu_name] = taxonomy


tab_contents = read_file('1.ASV-Creation/ZOTUs-Table.tab')
out_tab = open(OUTPUT_FOLDER + '/' + OUTPUT_ASV_TABLE, 'w+')
for line in tab_contents:
    if line[0] == '#':
        new_line = line + '\tTaxonomy\n'
    else:
        clean_zotu_name = line.split('\t')[0]
        new_line = line + '\t' + zotus_taxonomy_dict[clean_zotu_name] + '\n'
    out_tab.write(new_line)
out_tab.close()


taxonomy_counters_dict = dict()
for value in zotus_taxonomy_dict.values():
    if value not in taxonomy_counters_dict.keys():
        taxonomy_counters_dict[value] = 1
    else:
        taxonomy_counters_dict[value] += 1

out_file = open(OUTPUT_FOLDER + '/for_krona.tab', 'w+')
for key, value in taxonomy_counters_dict.items():
    out_file.write(str(value) + '\t' + key.replace(';', '\t') + '\n')
out_file.close()

system('0.Setup_and_Testing/' + KRONA_TOOL + ' ' + OUTPUT_FOLDER + 'for_krona.tab')
system('mv text.krona.html ' + OUTPUT_FOLDER + '/krona_plot.html')
system('rm ' + OUTPUT_FOLDER + 'for_krona.tab')


file_list = ['1.ASV-Creation/good_ZOTUS.log', '1.ASV-Creation/good_ZOTUS.fa', '1.ASV-Creation/denoising.tab',
             '1.ASV-Creation/other_ZOTUS.fa', '1.ASV-Creation/ZOTUs-Table.tab',
             '2.Taxonomy-Classification/alignment_vector.csv', INPUT_FASTA_EXTRACTION,
             OUTPUT_FASTA_EXTRACTION, CLUSTERING_DIRECTORY]

for i in file_list:
    print(i)
    system('rm -r ' + i)