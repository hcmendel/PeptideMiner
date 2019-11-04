import config,mature,output

"""
Step 5
Identifies mature peptides from step 4 output.
"""

"""Set path to fasta36 program """
def path_fasta():
    p = config.C['fasta_path']
    return p

"""Retrieve step 4 output"""
def sp(file):
    First_line = True
    signalp = []
    with open(file) as f:
        for l in f:
            ll = l.strip().split(',')
            if First_line is True:
                First_line = False
                continue
            signalp.append([ll[0],ll[2]])
    signalp.sort()
    return signalp


def run(evaluecutoff):
    file_step4 = './02-pipeline/step4.csv'
    matseq = []

    """Find mature sequences"""
    for s in sp(file_step4):
        mat = mature.findmat(s,path_fasta(),float(evaluecutoff),
                             config.C['mature_min_length'],config.C['mature_max_length'])
        if mat is not None:
            matseq.append(mat)

    """Output to csv file """
    filename = './02-pipeline/step5.csv'
    header = ['cdsid_mature#','mature sequence']
    out = []
    for m in matseq:
        for mm in m:
            out.append(mm)

    output.csv(filename,header,out)
    print 'The mature peptides were written to the file {}.\n'.format(filename)
