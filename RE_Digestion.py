import re,os,sys

Str = "AGAATTCTCGTGCGAATTCGGATTTAAGCTAAGGCTGGCTGGAATTCAGTCGGCTGAGCGTAGGCTTAAGCGGCTGAGGCTGAGGTTAAAGGCGGATGCGCGTAGGCTGGATCGATCCCGGTGACGAATTCGTGCGGATGCGGCTGAAAGCTGGAATTCAGTCGGCTGAGCGTAGGCTTAAGCGGCTGAGGCTGAGGTTAAAGGCGGATGCGCGTAGGCTGGATCG"

fname = "ref_PanTig1.0_chrUn.fa"

def fraglen_from_seq(seqName,seq,e1,e2):
    sites_by_pos = sorted(reduce(lambda x,y:x+y,[[(m.start(),e) for m in re.finditer(e,seq)] for e in [e1,e2]]))
    #print sites_by_pos
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
    fraglen_from_seq(key[0],key[1],"CATG","AATT")
