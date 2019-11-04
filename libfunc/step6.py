import config,mysqlpop,output,mysqlout

"""
Step 6
Populates the mature table in the SQLite DB.
Populates the noduplicates table in the SQLite DB.
"""

def mature(file):
    First_line = True
    seqs = []
    with open(file) as f:
        for l in f:
            ll = l.strip().split(',')
            if First_line is True:
                First_line = False
                continue
            seqs.append(ll)
    return seqs

def mysql_pop(file):
    matseq_count = 0
    nodups_count = 0
    for m in mature(file):
        cdsid = m[0].split('_')[0]
        seq = m[1]
        m = mysqlpop.matseq(cdsid,seq)
        matseq_count += m
        
        n = mysqlpop.nodups(cdsid,seq)
        nodups_count += n
        
    print '\nThe MySQL mature table has been populated.'
    print '{} mature peptides have been added to the SQLite DB mature table.'.format(
        matseq_count)
    print '{} unique mature peptides have been added to the SQLite DB noduplicates\
table.'.format(nodups_count)


def hmmid(file):
    First_line = True
    hmmid = []
    with open(file) as f:
        for l in f:
            ll = l.strip().split(',')
            if First_line is True:
                First_line = False
                continue
            if ll[1] not in hmmid:
                hmmid.append(ll[1])
    return hmmid


"""Retrieve hmm ids from step 1 output """
def nodup():
    total = []
    file_step1 = './02-pipeline/step1.csv'
    for i in hmmid(file_step1):
        D = mysqlout.noduplicates(i)
        total.append(D)
    return total


def run():
    file_step5 = './02-pipeline/step5.csv'
    
    print 'Populating the mature and noduplicates table in MySQL...\n'
    mysql_pop(file_step5)

    header = ['id','hmm_id','transcriptome','matseq']
    filename = './02-pipeline/step6.fna'
    seq = []

    """Output mature sequences to a fasta file """
    for n in nodup():
        for nn in n:
            nn = nn[0].strip().split(',')
            seq.append([nn[0],nn[3]])

    output.fasta(filename,seq)
    print 'The unique mature sequences have been written to the file {}.\n'.format(filename)
    
    
