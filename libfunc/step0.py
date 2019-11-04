import os
import subprocess as sub
import fasta_parse,config,output


"""
hmmsearch

Input = neuropeptide family of interest in config.txt
Current options: Natriureticpeptide*,Oxytocin*,Insulin*, and Tachykinin*

"""

def outcsv(filename,header,lines):
    with open(filename,'w') as out:
        out.write(','.join(header))
        out.write('\n')
        for l in lines:
            out.write(l)
            out.write('\n')


def hmmsearch(out_path,hmm_path,q_path): 
    search = '{0}/hmmsearch --tblout {1}.tbl {2} {3}'.format(
        config.C['hmmer_path'],out_path,hmm_path,q_path)

    run = sub.Popen(search,shell=True,stdout=sub.PIPE,stderr=sub.PIPE)
    
    stdout,stderr = run.communicate()

    return [stdout,stderr]

def combine(out_path,query):
    tbl = '{}.tbl'.format(out_path)
    csv = '{}.csv'.format(out_path)

    
    out = []
    for l in open(tbl, "r").readlines():
        if l.startswith("#"):
            pass
        else:
            ll = l.replace(',','').strip().split()

            for ID, fastaseq in query:
                """if ID in .tbl matches an ID in fastaDict, then print"""
                if str(ID).startswith(str(ll[0])):
            
                    line = ",".join(ll[:18]) + "," + " ".join(ll[18:]) + "," + str(fastaseq)
                    out.append(line)
                else:
                    pass

    header =["ID", "accession", "query_name", "accession", "full_E-value", "full_score", "full_bias", 
     "dom_E-value", "dom_score", "dom_bias", "exp", "reg", "clu", "ov", "env", "dom", "rep", 
     "inc", "desc_target", "sequence"]
    outcsv(csv,header,out) 
    return out


def run():
    """Set up paths to profile-HMMs, query database and output"""
    query_path = config.C['query_path']
    hmm_dir = '{}/data/02-pHMM'.format(config.C['path'])
    out_dir = './01-hmmsearch'
    hmmsearchout = './01-hmmsearch/00-step0_hmmsearchoutput.txt'

    """Get a list of the profile-HMMs available for the desired neuropeptide family"""
    hmms = []
    for h in os.listdir(hmm_dir):
        if h.startswith(str(config.C['neuropeptide_family'])):
            hmms.append('{}/{}'.format(hmm_dir,h))

    """Retrieve query db and profile-HMMs and do hmmsearch"""
    print 'Running hmmsearch...'
    search = []
    csv = []
    for q in os.listdir(query_path):
        if q.endswith('.fna'):
            q_path = '{}/{}'.format(query_path,q)
            print 'The query is {}'.format(q_path)
            query = ''.join(q.split('.')[:1])
            
            with open(q_path,'r') as f:
                seq = f.read().split('\n')
                fastaDict = fasta_parse.fna(seq)
            
            for h in hmms:
                hmm = h.strip().split('/')[-1].split('.')[0]
                hmm_path = '{}/{}.hmm'.format(hmm_dir,hmm)
                print 'The pHMM path is {}\n'.format(hmm_path)
                out_path = "{}/{}.{}".format(out_dir,hmm,query)

                """hmmsearch"""
                search.append(hmmsearch(out_path,hmm_path,q_path))
                
                """Add read sequence to output file"""
                csv = combine(out_path,fastaDict)

    """Output hmmsearch stdout and stderr to text file"""
    out = []
    for l in search:
        ll = "\n".join(l)
        lll = ll.replace('\n',"\n")
        out.append(lll)

    output.txt(hmmsearchout,out)


