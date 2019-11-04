import sys

"""
Step 3 support module.
Extracts the CDS from the hmmsearch hits.
sequence = amino acid sequence
min_size = minimum length the sequence has to be to be included as CDS.
"""

def find(seq,min_size):
        ncds = 1
        for seg in seq[1].split('*'):
                if len(seg) < int(min_size):
                        continue
                if 'M' not in seg:
                        continue
                s = seg[seg.index('M'):]
                if len(s) < int(min_size):
                        continue
                n = [seq[0],str(ncds),s]
                ncds += 1
                return n

