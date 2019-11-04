Readme.txt file for hpipeline


Requirements
Programs that need to be installed for NPpip to run include: signal-4.1, NCBI (makeblastdb and blastp), fasta36, HMMER 3.0, and Python.

Run-in NPpip
1) The user creates a directory from where the program will run (working directory). All output files will be directed to the working directory

2) Copy the config.txt file into this directory and update the config.txt file with the user PATHS and search variables.
	User has to add path to signalp 4.1
	User has to add path to NCBI.
	User has to add path to fasta36
	User has to add path to HMMER3

3) Run the program from the command line from the working directory: $ python PATH/TO/NPpip/main.py

profile-HMMs currently available:
#Choose from:
	test_OTVP
	insulin
	natriureticpeptides
	oxytocin
	tachykinin

To run a test run. 
1. Copy the config.txt file with the updated PATHs and searching variable to the 01-hpipeline/test-output directory

2. In config.txt set query database path to /PATH/TO/01-hpipeline/data and neuropeptide family to test.

3. run main.py from 01-hpipeline/test-output






