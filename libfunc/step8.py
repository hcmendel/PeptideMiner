import os
import datetime
import config,mysqlout,output

"""
step 8
Output results from the SQLite DB.
"""
now = datetime.datetime.now()
date = now.strftime("%d/%m/%Y")

def parse(file):
    First_line = True
    out = []
    with open(file) as f:
        for l in f:
            ll = l.strip().split(',')
            if First_line is True:
                First_line = False
                continue
            out.append(ll)
    return out


def analysis():

    """pHMMs searched with"""
    hmm_dir = '{}/data/02-pHMM'.format(config.C['path'])
    hmms = []
    for h in os.listdir(hmm_dir):
        if h.startswith(str(config.C['neuropeptide_family'])):
            hmms.append(h)

    """Query databases searched"""
    query_path = config.C['query_path']
    queries = []
    for q in os.listdir(query_path):
        if q.endswith('.fna'):
            queries.append(q)

    """Number of hmmsearch hits"""
    hmmsearch = './02-pipeline/step2.csv'
    hmmout = parse(hmmsearch)
    n_hmmsout = len(hmmout)


    """info from SQLite DB output"""
    file_step8 = './02-pipeline/step8.csv'
    step8 = parse(file_step8)

    PeptideMinerhits = set(l[0] for l in step8)
    querydb = set(l[3] for l in step8)
    phmm = set(l[2] for l in step8)
    unique_matseq = set(l[8] for l in step8)
    unique_pre = set(l[6] for l in step8)
    

    """number of different reads per profile-HMM"""
    precursors_phmm = {}
    for p in phmm:
        p_phmm = set(pre[1] for pre in step8 if pre[2]==p)
        precursors_phmm[p] = len(p_phmm)

    """Reads per pHMM csv file output"""
    with open('./02-pipeline/step8_readsperphmm.csv','w') as out:
        out.write('number reads per profile-HMM.\nprofile-HMM,number of reads\n')
        for r in precursors_phmm:
            out.write('{},{}\n'.format(r,precursors_phmm[r]))

    """Summart txt output"""
    with open('./02-pipeline/step8_output_summary.txt','w') as out:
        out.write('Summary PeptideMiner peptide search\n')
        out.write('Date: {}\n'.format(date))
        out.write('\n')
        out.write('Number of profile-HMMs used: {}\n'.format(len(hmms)))
        out.write('\t{}\n'.format(','.join(hmms)))
        out.write('Number of databases searched: {}\n'.format(len(queries)))
        out.write('\t{}\n\n'.format(','.join(queries)))
        out.write('Output:\n')
        out.write('hmmsearch hits: {}\n'.format(n_hmmsout))
        out.write('PeptideMiner hits: {}\n'.format(len(PeptideMinerhits)))
        out.write('\tNumber of unique CDS: {}\n'.format(len(unique_pre)))
        out.write('\tNumber of unique mature peptides: {}\n'.format(len(unique_matseq)))
    
        
def run():
    filename = './02-pipeline/step8.csv'
    fields = mysqlout.final(config.C['neuropeptide_family'])
    output.csv(filename,fields[0],fields[1:])
    analysis()
    print 'The output files have been written.'
