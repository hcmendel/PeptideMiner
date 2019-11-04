import mysqlpop,config,mysqlout,output,blast


"""
Step 7
BLAST unique mature peptides (in the noduplicates table of the SQLite DB)
against the known mature peptides (in the known_seq tableof the SQLite DB).
"""


def nodup(file):
    First_line = True
    nodup = []
    with open(file) as f:
        for l in f:
            ll = l.strip().split(',')
            if First_line is True:
                First_line = False
                continue
            nodup.append(ll)
    return nodup


def known():
    familyid = mysqlout.familyid(config.C['neuropeptide_family'])
    K = mysqlout.known_NP(str(familyid))

    filename = './02-pipeline/step7_knownseq.fna'

    out = []
    for n in K[1:]:
        for nn in n:
            nn = nn.strip().split(',')
            out.append([nn[0],nn[1]])

    output.fasta(filename,out)
    return filename


def run():
    file_step1 = './02-pipeline/step6.fna'

    """Retrieve known sequences"""
    knownseqfile = known()

    """Check if a BLAST DB of step7_knownseq already exists; Make BLAST DB if it doesn't"""
    blastdb = blast.check(knownseqfile)

    """BLAST unique mature peptides against known sequences"""
    blastoutfile = './02-pipeline/step7_blastp.csv'
    blast.blastp(blastdb,file_step1,blastoutfile)

    """Parse the BLASTp output file"""
    print 'Parsing BLASTp output...\n'
    blastout = []
    for b in blast.parse(blastoutfile):#[cds_id, known sequence, %ID, length, evalue]
        blastout.append([str(b[0]),b[1],b[2],b[3],b[4]])

    """Populate the SQLite Annotated table with BLASTp results"""
    print 'Populating the Annotated table in the SQLite DB.'
    count = 0
    for b in blastout:
        c = mysqlpop.annotated(b)
        count += c
    print '{} hits have been entered in the SQLite annotated table.'.format(
        count)
    print 'DATA ENTRY INTO MYSQL ANNOTATED TABLE IS COMPLETE'

    filename = './02-pipeline/step7.csv'
    header = ['cds_id','knownNP id','PID','length','evalue']
    output.csv(filename,header,blastout)
    print 'The BLASTp results have were written to {}.\n'.format(filename)
