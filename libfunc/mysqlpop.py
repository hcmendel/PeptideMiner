import sys
from sys import argv, stderr
import config,mydb

"""
SQLite DB population module.
There is a separate population function for each table in the SQLite DB.
Most modules take a 'fields' argument which should be a list. 
"""


def seqreads(fields):
        m = config.m
        
        hmm=fields[1]
        transcriptome_name=fields[2]

        hmmid_hmm = m.onevalue('id','hmm',{'name':hmm})
        
        if hmmid_hmm is None:
                m.insert('hmm',{'name':hmm})
                hmmid_hmm = m.onevalue('id','hmm',{'name':hmm})
                print 'The pHMM "{}" has been added to the SQLite hmm table with ID "{}".'.format(hmm,hmmid_hmm)

        readid = m.onevalue('id','seqreads',{'name':fields[0],'hmmid':hmmid_hmm})

        """If the read already exists and was found with the same pHMM, then it will not be added again"""
        if readid:
                print 'The read "{}" already exists in the SQLite seqreads table with the pHMM id "{}" and readid "{}"'.format(fields[0],hmmid_hmm,readid)
                return int(0)
        else:
                m.insert('seqreads',{'name':fields[0],'hmmid':hmmid_hmm,'transcriptome':transcriptome_name,'evalue':fields[3],'signalseq_length':0,'precursor':fields[4]})
                readname = m.onevalue('name','seqreads',{'name':fields[0]})
                hmmid_seqread = m.onevalue('hmmid','seqreads',{'hmmid':hmmid_hmm})
                return int(1)

def cds(fields):
        m = config.m
        
        seqreadsid = fields[0]
        cds = fields[2]

        cdsid_cds = m.onevalue('id','cds',{'sequence':cds})
        
        if cdsid_cds is None:
                m.insert('cds',{'sequence':cds})
                cdsid_cds = m.onevalue('id','cds',{'sequence':cds})
                count = (1)
        else:
                count = int(0)

        m.update('seqreads',{'cds_id':cdsid_cds},'id={}'.format(seqreadsid))
        return count

def signalp(cdsid,pos):
        m = config.m
        
        m.update('seqreads',{'signalseq_length':pos},'cds_id={}'.format(cdsid))


def matseq(cdsid,seq):
        m = config.m
        
        mature_unique = m.onevalue('id','mature',{'cds_id':cdsid,'matseq':seq})
        
        """Check if the entry hasn't been entered before with the specified cds id and mature sequence"""
        if mature_unique:
                print 'The mature sequence {} already exists in the mature table with readid {}.'.format(seq,cdsid)
                return int(0)
        else:
                m.insert('mature',{'cds_id':cdsid,'matseq':seq})
                return int(1)


def nodups(cdsid,seq):
        m = config.m
        
        transc_seqreads = m.onevalue('transcriptome','seqreads',{'cds_id':cdsid})
        hmmid_seqreads = m.onevalue('hmmid','seqreads',{'cds_id':cdsid})

        id_unique = m.onevalue('id','noduplicates',{'transcriptome':transc_seqreads,'matseq':seq})

        if id_unique:
                print 'The read {} already exists in noduplicates with transcriptome {} and matseq {}.'.format(cdsid,transc_seqreads,seq)

                """update 'mature' table with existing id from 'noduplicates' table"""
                m.update('mature',{'noduplicates_id':id_unique},'matseq="{}"'.format(seq))
                print 'The read {} in the mature table has been updated with the noduplicates_id {}.'.format(cdsid,id_unique)
                return int(0)
        else:
                m.insert('noduplicates',{'hmm_id':hmmid_seqreads,'transcriptome':transc_seqreads,'matseq':seq})
                """update 'mature' table with new id from 'noduplicates' table"""
                noduplicates_ID = m.onevalue('id','noduplicates',{'matseq':seq})
                m.update('mature',{'noduplicates_id':noduplicates_ID},'matseq="{}"'.format(seq))
                return int(1)

def knownseq(fields,neuropeptide_family):#fields = [species,accession,name,seq]
        m = config.m
        
        familyid = m.onevalue('id','neuropeptide_family',{'name':neuropeptide_family})
        
        if familyid is None:
                print 'Insert new family id'
                m.insert('neuropeptide_family',{'name':neuropeptide_family})
                familyid = m.onevalue('id','neuropeptide_family',{'name':neuropeptide_family})

        known_unique = m.onevalue('id','known_NP',{'familyid':familyid,'accession':fields[1],'name':fields[2]})

        if known_unique:
            print 'The sequence {} for the neuropeptide family {} already exists.'.format(fields[1],neuropeptide_family)
            return int(0)
        else:
            m.insert('known_NP',{'name':fields[2],'familyid':familyid,'species':fields[0],'sequence':fields[3],'accession':fields[1]})
            return int(1)


def annotated(fields):
        m = config.m
        
        hit = fields[0]
        known = fields[1]
        PID = fields[2]
        Evalue = fields[4]
        length = fields[3]

        annotated_unique = m.onevalue('id','annotated',{'novel_id':hit,'knownNP_id':known})

        if annotated_unique:
                print 'The hit with id {} has already been entered in the annotated table with the knownNP_id {}.'.format(hit,known)
                return int(0)
        else:
                m.insert('annotated',{'novel_id':hit,'knownNP_id':known,'pid':PID,'evalue':Evalue,'length_alignment':length})
                return int(1)

        
