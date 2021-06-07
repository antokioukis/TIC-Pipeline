from os import system
from os.path import isfile
import argparse

# read arguments for the three levels of similarity
# as well as the absolute path of the MAIN_DIR
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tool", help="usearch or vsearch", required=True, type=str)
parser.add_argument("-n", "--threads", help="Number of threads", required=True, type=int)
parser.add_argument("-d", "--dataset", required=True, help="Full path of dataset", type=str)
parser.add_argument("-b", "--base", required=True, help="Full path of base", type=str)
parser.add_argument("-o", "--out_file_prefix", required=True, help="Out files prefix", type=str)
parser.add_argument("-m", "--mode", required=True, help="Mode: LTP or SILVA", type=str)
args = parser.parse_args()

if not (args.tool == 'usearch') and not(args.tool == 'vsearch'):
    print('Matching tool not used by program, available options (usearch, vsearch)')
    exit()
if not (args.mode == 'LTP') and not(args.mode == 'SILVA'):
    print('Mode not used by program, available options (LTP, SILVA)')
    exit()
if not isfile(args.dataset):
    print('Dataset FASTA file not present')
    exit()
if not isfile(args.base):
    print('Base UDB file not present')
    exit()

TOOL = args.tool
THREADS = str(args.threads)
DATASET = str(args.dataset)
DB_BASE = str(args.base)
OUT_FILE_PREFIX = str(args.out_file_prefix)
MODE = str(args.mode)

if TOOL == 'usearch':
    USEARCH_BIN = 'usearch -threads 6 -usearch_global '
elif TOOL == 'vsearch':
    VSEARCH_BIN = 'vsearch -threads 6 -usearch_global '

if MODE == 'LTP':
    out_file_m2 = OUT_FILE_PREFIX + '_LTP.m2'
    out_file_fasta = OUT_FILE_PREFIX + '_not_matched_LTP.fasta'
elif MODE == 'SILVA':
    out_file_m2 = OUT_FILE_PREFIX + '_SILVA.m2'
    out_file_fasta = OUT_FILE_PREFIX + '_not_matched_SILVA.fasta'

cmd = USEARCH_BIN + DATASET + ' -strand both -db ' + DB_BASE + ' -id 0.98 -notmatched ' + out_file_fasta
cmd += ' -userout ' + out_file_m2 + ' -userfields query+target+id >/dev/null 2>/dev/null '
system(cmd)
