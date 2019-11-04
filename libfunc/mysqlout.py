import sys
import config

"""
SQLite DB output module.
"""

def hmmid(hmmname):
        m = config.m
        
        for res in m.selectall(('id'),'hmm',("name='{}'".format(hmmname))):
            return str(res[0])


def seqreads():
        m = config.m
        
        out = []
        for res in m.selectall(('id','precursor','hmmid'),'seqreads s'):
                out.append([res[0],res[1],res[2]])
        return out


def cds(fields):
        m = config.m
        
        out = []

        seqreadsid = fields[0]
        cds = fields[2]
        for res in m.selectall(('c.id','c.sequence'),
                               ('cds c','seqreads s'),
                               ("s.id='{}' and c.id=s.cds_id".format(seqreadsid))):
                l = str(res[0]) + ',' + str(res[1])
                out.append(l)
        return out


def noduplicates(hmmid):
        m = config.m
        
        out = []
        
        for res in m.selectall(('id','hmm_id','transcriptome','matseq'),'noduplicates',('hmm_id={}'.format(hmmid))):
                l = str(res[0]) + ',' + str(res[1]) + ',' + str(res[2]) + ',' + str(res[3])
                out.append([l])
        return out


def familyid(NP_family):
        m = config.m
        
        for res in m.selectall(('id'),'neuropeptide_family',("name='{}'".format(NP_family))):
                return str(res[0])


def known_NP(NPfamilyid):
        m = config.m
        
        out = []
        header = ['knownseq_id','sequence']
        out.append(header)
        
        for res in m.selectall(('id','sequence'),'known_NP',('familyid={}'.format(NPfamilyid))):
                l = str(res[0]) + ',' + str(res[1])
                out.append([l])
        return out


def final(NPfamilyname):
        m = config.m
        
        NPfamilyid = familyid(NPfamilyname)
        out = []
        header = ['hit id','hit name','pHMM name','hit query DB','hmmsearch evalue','hit sequence','hit CDS','hit signal peptide length',
                  'hit mature sequence','pBLAST known sequence accession','pBLAST known sequence','pBLAST %ID','pBLAST length','pBLAST evalue']
        out.append(header)
 
        for res in m.selectall(('s.id','s.name','h.name','s.transcriptome','s.evalue','s.precursor','c.sequence','s.signalseq_length',
                                'o.matseq','k.accession','k.sequence','a.pid','a.length_alignment','a.evalue'),
                               ('known_NP k','neuropeptide_family n','annotated a','noduplicates o','seqreads s',
                                'cds c','mature m','hmm h'),
                               ("n.id='{}' and n.id=k.familyid and k.id=a.knownNP_id and a.novel_id=o.id \
                                and o.id=m.noduplicates_id and m.cds_id=s.cds_id and s.cds_id=c.id and s.hmmid=h.id".format(NPfamilyid))):

                l = str(res[0]) + ',' + str(res[1]) + ',' + str(res[2]) + ',' + str(res[3]) + ',' + str(res[4]) + ',' + \
                    str(res[5]) + ',' + str(res[6]) + ',' + str(res[7]) + ',' + str(res[8]) + ',' + str(res[9]) + ',' + \
                    str(res[10]) + ',' + str(res[11]) + ',' + str(res[12]) + ',' + str(res[13])
                out.append([l])
        return out
