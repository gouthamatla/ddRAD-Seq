# This script gives the double digest restriction fragments in a BED file format. This script has been adopted from Peterson et.al pipeline for ddRAD-Seq data analysis.
# 'bedtools getfasta' can be used to extract the corresponding sequences from a genome.fa file
# This script does not consider the reverse compliment
# Usage: RE_Digestion.py > RE_Sites.bed

import re,os,sys

RE_Site1="CATG"
RE_Site2="AATT"

fname = "Genome.fa"

def fraglen_from_seq(seqName,seq,e1,e2):
    sites_by_pos = sorted(reduce(lambda x,y:x+y,[[(m.start(),e) for m in re.finditer(e,seq)] for e in [e1,e2]]))
    fraglens = []
    fragPos = ()
    lastpos = None
    lastsite = None
    for pos,site in sites_by_pos:
        if lastpos and lastsite and lastsite != site:
            print seqName,lastpos,pos
            fragPos = (lastpos,pos)
            fraglens.append(fragPos)
        lastpos = pos
        lastsite = site


def getFastaRec(fname):
    seq = ""
    ids = []
    seqRec = []
    for line in open(fname,'r'):
        if (line.startswith(">")):
            ID = line.strip()
            if ( len(seq) > 0 ):
                seqRec.append(seq.strip().upper())
                seq = ""
            ids.append(ID[1:])
        else:
            seq = seq + line.rstrip()
            
    seqRec.append(seq.strip().upper())
    
    return zip(ids, seqRec)

for key in  getFastaRec(fname):
    fraglen_from_seq(key[0],key[1],RE_Site1,RE_Site2)
