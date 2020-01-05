# PeptideMiner
PeptideMiner neuropeptide mining pipeline



Readme.txt file for PeptideMiner

PeptideMiner is a pipeline that uses profile hidden Markov models (profile-HMMs) of neuropeptide families to search query datasets for neuropeptide homologues. This document outlines the program requirements (section 1), how to do a test run (section 2) and the profile-HMMs it comes with (section 3). 


# 1. PeptideMiner running requirements
1.1. Programs that need to be installed for PeptideMiner to run include:

- signal-4.1

-	NCBI (makeblastdb and blastp)

- fasta36

- HMMER 3.0

- Python2.7 (PeptideMiner is not compatible with Python 3.5+)

1.2. Running PeptideMiner

1) The user creates a directory from where the program will run (working directory). All output files will be directed to the working directory

2) Copy the config.txt file into this directory and update the config.txt file with the user PATHS and search variables.

- User has to add path to signalp 4.1

-	User has to add path to NCBI.

-	User has to add path to fasta36

-	User has to add path to HMMER3

3) Query databases must be in amino acids, fasta format and have the .fna extension. You can search multiple query databases in one search by putting them in the same directory.

4) Run the program from the command line from the working directory: $ python PATH/TO/PeptideMiner/main.py


# 2. Test run
1) Copy the config.txt file to chosen working directory

2) Adjust the variables in the config.txt:

query_path =  /PATH/TO/PeptideMiner/data/03-trial_query 

neuropeptide_family = test_OTVP

CDS variable:

- cds_min_length = 50

SignalP variables:

- sp_cutoff = 0.41

- sp_min_length = 8

Mature variables

- mature_min_length = 7

- mature_max_length = 15

- mature_evalue_cutoff = 1

3) Run main.py from chosen working directory

4) Compare output to output in PeptideMiner/data/04-trial-OTVP


# 3. Profile-HMMs
3.1. Available profile-HMMs

PeptideMiner comes with profile-HMMs for insulin, natriuretic peptide, oxytocin, somatostatin, and tachykinin. 

profile-HMMs currently available:

Choose from:
	
  - test_OTVP
	
  - insulin
	
  - natriureticpeptides
	
  - oxytocin
	
  - tachykinin

It can search multiple query databases with more than one profile-HMM for the same neuropeptide family. To achieve this, PeptideMiner splits the file names of each profile-HMM in the data/02-pHMM directory at '_'. It matches the phrase preceding the first '_' to the  "neuropeptide_family" name provided in the config.txt and uses the profile-HMMs that match.

3.2. Using your own profile-HMM

When using your own profile-HMM the first word in the file name needs to match the "neuropeptide_family" specified in the config.txt file. The same applies to the directory where the known mature peptide sequences are stored in the data/01-known_seq directory. 

