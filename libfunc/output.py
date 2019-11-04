import os
import config


"""
Output module
At the beginning of each step in the pipeline: Checks whether the output
directory exists.

At the end of each step in the pipeline: Functions to direct output to either a
fasta, csv or txt file.
"""

"""Checking output exists"""
def check_dir_exists():
    hmmsearch_dir = './01-hmmsearch'
    pipeline_dir = './02-pipeline'
    if not os.path.exists(hmmsearch_dir):
        os.makedirs(hmmsearch_dir)
    if not os.path.exists(pipeline_dir):
        os.makedirs(pipeline_dir)


def check_hmm_has_run():
    if [f for f in os.listdir('./01-hmmsearch') if f.endswith('csv')]:
         return True
    return False


def check_step_has_run(step):
    if [f for f in os.listdir('./02-pipeline') if f.startswith('{}'.format(step))]:
        return True
    return False


"""Output functions"""
def fasta(filename,seq):
    with open(filename,'w') as out:
        for l in seq:
            i=l[0]
            seq=l[1]
            out.write('>{}\n{}\n'.format(i,seq))


def csv(filename,header,lines):
    with open(filename,'w') as out:
        out.write(','.join(header))
        out.write('\n')
        for l in lines:
            out.write(','.join(l))
            out.write('\n')


def txt(filename,lines):
    with open(filename,'w') as out:
        for l in lines:
            out.write(l)
            out.write('\n')
    
