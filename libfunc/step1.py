import os
from libfunc import config,evalue,mysqlpop,mysqlout,output


def step1a(input_file):
    csv_file = str(input_file).split('/')[-1]
    hmm = str(csv_file.split('.')[0])
    return hmm


def step1b(input_file):
    csv_file = str(input_file).split('/')[-1]
    name = str(csv_file).split('.')[1]
    return name


def loop():
    files=[]
    hmmoutput_dir = './01-hmmsearch'

    for file in os.listdir(hmmoutput_dir):
        if file.endswith('.csv'):
            files.append('{}/{}'.format(hmmoutput_dir,file))
        else:
            continue

    return files


def pop():
    count = 0
    hmmids=[]

    """loop through the files in the hmmsearch directory"""
    for file in loop():
        
        """Get hmm name from filename"""
        hmmname=step1a(file)

        """Get transcriptome name from filename"""
        transcriptomename=step1b(file)

        """Filter according to lowest evalue per readname and populate seqreads"""
        print 'Populating the SQLite seqreads table with hmmsearch hits...'
        for e in evalue.filt(file):
            s = mysqlpop.seqreads(e)
            count += s

        """Return the listof HMM IDs from the sqlite DB"""
        hmmid=mysqlout.hmmid(hmmname)
        if hmmid not in hmmids:
            hmmids.append([transcriptomename,hmmid,hmmname])

    print 'Data entry into the SQLite seqreads table is complete.'
    print '{} hits have been added to the SQLite seqreads table.\n'.format(count)
    return hmmids


def run():
    
    """Populate SQLite database with hmmsearch output"""
    l=pop()

    """Output the name of hmmids to a .csv file"""
    filename='02-pipeline/step1.csv'
    header=['transcriptome','hmmid','hmmname']
    output.csv(filename,header,l)
