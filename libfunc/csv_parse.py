"""
Parses csv files into list
"""

def llist(infile,col1,col2):
    S = []
    First_line = True
    with open(infile) as f:
        for l in f:
            l = l.strip().split(',')
            if First_line is True:
                First_line = False
                continue
            S.append([l[col1],l[col2]])
    return S

