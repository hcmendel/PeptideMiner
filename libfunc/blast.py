import os
import config,output

"""
BLAST module.
Support module for Step 7.
"""

def make(knownseqfile):
    """Create a ncbi db of knownseqfile"""
    blastdb = os.popen('{0}/makeblastdb -in {1} -dbtype prot -hash_index -out {1}'.format(
        config.C['ncbi_path'],knownseqfile))


def check(knownseqfile):
    """Check if an NCBI db of the knownseqfile already exists"""
    query = '{}'.format(knownseqfile)

    if os.path.isfile('{}.phd'.format(knownseqfile)) is True:
        print 'Yay, there is already an NCBI database for {}!\n'.format(knownseqfile)
    else:
        print 'Making an NCBI database for {0} in {1}.\n'.format(
            knownseqfile,config.C['neuropeptide_family'])
        make('{}'.format(knownseqfile))
    return query


def blastp(blastdb,queryfile,outfile):
    print 'Running BLASTp...'
    blastp = os.popen('{0}/blastp -db {1} -query {2} -outfmt 10 -out {3}'.format(
        config.C['ncbi_path'],blastdb,queryfile,outfile))
    print 'BLASTp complete.'

    return blastp


def file(file):
    First_line = True
    F = []
    with open(file) as f:
        for l in f:
            ll = l.strip().split(',')
            if First_line is True:
                First_line = False
                continue
            F.append(ll)

    return F


def parse(blastoutput):
    """Parsing the blast outfmt 10 file"""
    B = []
    blastout = file(blastoutput)
    for b in blastout:
        B.append([int(b[0]),b[1],b[2],b[3],b[10]])#[hit,known sequence,PID,length,evalue]

    """Create list of unique query id's"""
    query = set([i[0] for i in B])
    U = []
    for q in query:
        """Loop through blastp output and group query ID's"""
        b = [i for i in B if i[0] == q]
        
        """For each query ID, sort group according to evalue"""
        b.sort(key=lambda i:float(i[4]))

        """For each group, keep only the hit with the lowest evalue"""
        U.append(b[0])
    U.sort()
    
    return U
