import mydb

"""
Step 2 support module.
Loops through hmmsearch output .csv file and extracts, for each read id, the
hits with the lowest e-value and its corresponding readname, transcriptome,
hmmid, e-value, and precursor sequence.
"""

def filt(input_file):
    E=[]
    csv_file = str(input_file).split('/')[-1]
    hmm = str(csv_file).split('.')[0]
    transcriptome_name = '.'.join(str(csv_file).split('.')[1:-1])

    first_line = True
    with open(input_file) as f:
        for l in f:
            fields = l.strip().split(',')
            if first_line:
                first_line = False 
                continue
            E.append([fields[0],hmm,transcriptome_name,fields[4],fields[19]])

    """Isolate readnames in the table and keep only the unique ones"""
    nodup = set([i[0] for i in E])
    
    S = []
    for r in nodup:
        """Isolate lines where the r == readname"""
        b = [i for i in E if i[0] == r]
        
        """Sort list accroding to evalue"""
        b.sort(key=lambda i:float(i[3]))
        S.append(b[0])
    return S


