from libfunc import output,config,cds,mysqlpop,mysqlout


"""
step 3
Identifies and extracts the protein coding sequence (CDS).
Uses step2 output as input.
"""


"""Retrieve sequences from Step2 output."""
def sequence(file):
    First_line = True
    seqs = []
    with open(file) as f:
        for l in f:
            ll = l.strip().split(',')
            if First_line is True:
                First_line = False
                continue
            seqs.append([ll[0],ll[1]])
    return seqs


def run():
    file_step2 = './02-pipeline/step2.csv'
    seqs = sequence(file_step2)
    out = []
    
    print 'Populating the CDS table in the SQLite DB... '
    CDS = []
    for s in seqs:
        """Find CDS"""
        c = cds.find(s,config.C['cds_min_length'])
        if c is not None:
            CDS.append(c)
        else:
            CDS.append([s[0],0,s[1]])
            
    """Populate SQLite DB CDS table"""
    count = 0
    for c in CDS:
        d = mysqlpop.cds(c)
        count += d
        l = mysqlout.cds(c)
        ll = l[0].split(',')
        if ll not in out:
            out.append([ll[0],ll[1]])
        else:
            continue

    """Output to csv"""
    filename = './02-pipeline/step3.csv'
    header = ['CDS ID','CDS']
    output.csv(filename,header,out)
    
    print 'The CDS have been written to the file {}.'.format(filename)
    print '{} CDS have been added to the CDS table in the SQLite DB\n'.format(count)
