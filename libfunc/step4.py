import signalp,config,mysqlpop,output


"""
step4

Runs SignalP on step 3 output (CDS).
Outputs results to .csv file and updates the seqreads table in the SQLite DB.
"""


def CDS(file):
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


def signal(seq,cutoff,min_length):
    nosignalpep=[]
    
    """Run signalp """
    pos = signalp.find(seq[1],str(config.C['signalp_path']),cutoff)

    """Update SQLite seqreads table with signalp signal peptide length"""
    mysqlpop.signalp(seq[0],pos)
    print 'Updated reads with cds_id {} with signalseq length {} in the SQLite seqreads table'.format(seq[0],pos)

    """Remove signal peptide in CDS where signal peptide was identified; return all sequences"""
    if pos == 0:
        nosignalpep.append([seq[0],str(pos),seq[1]])

    else:
        nseq = seq[1][int(pos):]
        if len(nseq) < int(min_length):
            nosignalpep.append([seq[0],str(pos),seq[1]])
        else:
            nosignalpep.append([seq[0],str(pos),nseq])
    return nosignalpep


def run():
    file_step3 = './02-pipeline/step3.csv'

    print 'Running SignalP...\n'

    """Retrieve sequences from Step3 output and run SignalP"""
    nosignalpep = []
    for c in CDS(file_step3):
        s = signal(c,config.C['sp_cutoff'],config.C['sp_min_length'])[0]
        nosignalpep.append(s)

    """Output to csv file"""
    filename = './02-pipeline/step4.csv'
    header = ['cds_id','signal peptide position','nosignalpeptide']
    output.csv(filename,header,nosignalpep)
    print '\nSignalP results have been written to the file {}.\n'.format(filename)
