

"""
PeptideMiner
Neuropeptide search pipeline

Pipeline requirements:
1. Config.txt file must be in the working directory

2. Correct paths to required programs must be provided in libfunc/config.txt

3. Output files will be directed to the working directory.

"""

import sys,os
import sqlite3
from sqlite3 import Error
from libfunc import step0,step1,step2,step3,step4,step5,step6,step7,step8
from libfunc import config,mydb,output,mature,known_NP,blast,mysqlout,matseq_cont


"""
Create the 01-hmmsearch directory for the hmmsearch output and
create the 02-pipeline directory for the pipeline output
"""
output.check_dir_exists()



"""
Populate the known_NP and neuropeptide_family table in the sqlite database
"""
known_NP.known_pop()



"""
Step 0
hmmsearch 
"""
if not output.check_hmm_has_run():
    print 'Running step 0'
    step0.run()


   
"""
Step 1
Loops through hmmsearch output files and populates the SQLite DB.
Returns a list of hmmid per transcriptome database in output folder.
"""
if not output.check_step_has_run('step1'):
    print 'Running step 1'
    step1.run()



"""
Step 2
Output seqreads table to .csv file.
"""
if not output.check_step_has_run('step2'):
    print 'Running step 2'
    step2.run()



"""
Step 3
Identification of protein coding sequences (CDS) in hmmsearch hits.
Outputs a .csv file of the CDS table.
"""
if not output.check_step_has_run('step3'):
    print 'Running step 3'
    step3.run()



"""
Step 4
Predicts signal peptides in CDS using SignalP.
"""
if not output.check_step_has_run('step4'):
    print 'Running step 4'
    step4.run()



"""
Step 5
Predicts mature peptides in CDS.
User is given the option to change the mature e-value cut-off after step 5 has run.
"""
if not output.check_step_has_run('step5'):
    print 'Running step 5'
    step5.run(config.C['mature_evalue_cutoff'])
    matseq_cont.question()


"""
Step 6
Populates the sqlite3 mature table.
Populates the sqlite3 noduplicates table.
"""
if not output.check_step_has_run('step6'):
    print 'Running step 6'
    step6.run()



"""
Step 7
Annotates mature peptides using BLASTp.
"""
if not output.check_step_has_run('step7.'):
    print 'Running step 7'
    step7.run()



"""
Step 8
Final results output.
""" 
if not output.check_step_has_run('step8'):
    print 'Running step 8'
    step8.run()

print 'PeptideMiner search is complete'



