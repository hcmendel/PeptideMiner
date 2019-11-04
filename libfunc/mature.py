from libfunc import proregion,config

"""
Step 5 support module.
Identifies the mature peptides in peptide precursors based on proregions and
cleavage sites.
"""

def findmat(sequence,fasta,ecutoff,min_length,max_length):
    dir_known = '{}/data/01-known_seq/{}'.format(
        config.C['path'],config.C['neuropeptide_family'])
    sequences = proregion.find_regions(
        sequence[1],fasta,dir_fasta=dir_known,ecutoff=ecutoff)

    if len(sequences) == 0:
        pass

    matures = []
    for seq in sequences:
        nterm = proregion.Nterm(seq[0])
        cterm = proregion.Cterm(seq[2])
        matures.append(nterm['sequence']+seq[1]+cterm['sequence'])

    matures = list(set(matures))
    output = []

    for i,seq in enumerate(matures):
        if len(seq) <= int(min_length) or len(seq) >= int(max_length):
            continue
        else:
            output.append(['{}_{}'.format(sequence[0],i),seq])

    return output
