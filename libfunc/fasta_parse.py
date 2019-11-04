
"""
Parses fasta files into a list
"""

def fna(file):
    S = []
    for l in file:
        if l.startswith('>'):
            S.append([l.strip()[1:],''])
        else:
            S[-1][1] += l.strip()
    return S
