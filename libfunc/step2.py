import sys
import config,output,mysqlout


"""
step 2: seqreads output.
Outputs the id and sequence from the seqreads table in the MySQL database.
"""

def run():
    file_step1 = './02-pipeline/step1.csv'

    """Retrieve seqreads table entries from the SQLite DB"""
    seqreads = []
    for l in mysqlout.seqreads():
        seqreads.append([str(l[0]),str(l[1]),str(l[2])])


    """Output to csv file"""
    filename='./02-pipeline/step2.csv'
    header=['seqreads id','sequence','profile-HMM name']
    output.csv(filename,header,seqreads)
    print 'The hits (MySQL id and sequence) have been written to the file {}.\n'.format(filename)
