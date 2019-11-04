import datetime,os,sys

"""
This script runs when config.py is imported into main.py

Reads the config.txt file and stores the variables
Sets up the sqlite database
"""

now = datetime.datetime.now()
date = now.strftime("%Y%m%d")

configfile = 'config.txt'

"""Stores variables from config.txt in the dictionary C"""
C = {}
with open(configfile) as f:
    for l in f:
        l = l.strip()
        if not l: continue
        if l.startswith('#'): continue
        ele = l.split('=')
        C[ele[0].strip()] = ele[1].strip()


"""Create the sqlite3 database"""
if not [f for f in os.listdir('./') if f.endswith('.db')]:
    print 'Creating the SQLite database'
    sqlite3_path = C['sqlite3_path']
    structure = '{}/data/nppip.sql'.format(C['path'])
    os.popen('{0} sqlite.db < {1}'.format(sqlite3_path,structure))

"""Set up the sqlite interface"""
import mydb
m = mydb.mysql()
