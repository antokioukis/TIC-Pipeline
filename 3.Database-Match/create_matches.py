from os import system, chdir
from sys import argv


def create_LTP_matches():
    out_file_m2 = 'match_LTP.m2'
    out_file_fasta = 'not_matched_LTP.fasta'
    cmd = MATCHING_TOOL + ' -usearch_global ' + ASV_FILE + ' -threads ' + THREADS + ' -strand both -db ' + LTP_UDB_DB
    cmd += ' -id ' + MATCH_IDENTITY + ' -notmatched ' + out_file_fasta
    cmd += ' -userout ' + out_file_m2 + ' -userfields query+target+id >/dev/null 2>/dev/null'
    system(cmd)


def create_SILVA_matches():
    out_file_m2 = 'match_SILVA.m2'
    out_file_fasta = 'not_matched_SILVA.fasta'
    cmd = MATCHING_TOOL + ' -usearch_global not_matched_LTP.fasta -threads ' + THREADS + ' -strand both -db '
    cmd += SILVA_UDB_DB + ' -id ' + MATCH_IDENTITY + ' -notmatched ' + out_file_fasta
    cmd += ' -userout ' + out_file_m2 + ' -userfields query+target+id >/dev/null 2>/dev/null'
    system(cmd)


ASV_FILE = argv[1]
LTP_UDB_DB = argv[2]
SILVA_UDB_DB = argv[3]
MATCHING_TOOL = argv[4]
THREADS = argv[5]
MATCH_IDENTITY = argv[6]

chdir('3.Database-Match/')
create_LTP_matches()
create_SILVA_matches()