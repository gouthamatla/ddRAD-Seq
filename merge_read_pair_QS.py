#This script takes a query name sorted bam file and merges read pairs or extends to double the read length if there is no mate.

import pysam,sys

read_length=80

insert_cutoff=2*read_length #Double the number of read length

# Merge the paired end reads. if there is overlap, ( logic to find overlap is if the insert length is less than the sum of read lengths of two reads), stitch them.

def mergeReadPairs(read,mate,insertlength):
	insertlength=abs(insertlength) # To get the positive number for insert_length
	if (insertlength>=insert_cutoff):
		return read+mate

	if (insertlength<insert_cutoff):
		overlap=insert_cutoff-insertlength
		pad_seq="N"*overlap
		return read+mate[overlap:]+pad_seq
		

def handleSingletons(read):
	pad_seq="N"*read_length
	return read+pad_seq

BAM = pysam.Samfile(sys.argv[1])

header=BAM.header
outfile = pysam.AlignmentFile("tmpfilename.sam", "wh", header=header)
a = pysam.AlignedSegment()

def write_bam(query_name,query_seq,query_flag,query_ref_name,query_ref_start,query_mapping_qual,query_cigar):
	a.query_name=query_name
	a.query_sequence=query_seq
	a.flag=query_flag
	a.reference_id=query_ref_name
	a.reference_start=query_ref_start
	a.mapping_quality=query_mapping_qual
	a.cigar=[(0,160)]
	a.next_reference_id=0
	a.next_reference_start=0
	a.template_length=0
	a.query_qualities="N"*160
	outfile.write(a)


for read in BAM: #??Iterate over each read in the BAM.?
	pos=BAM.tell()
	next_read=BAM.next()
	
	if read.qname==next_read.qname and read.tid==next_read.tid and abs(read.tlen)>len(read.seq):
		if read.is_reverse:
			write_bam(read.qname,
					mergeReadPairs(next_read.seq,read.seq,read.tlen),
					read.flag,read.tid,
					next_read.reference_start,
					read.mapping_quality,
					read.cigartuples)
		elif next_read.is_reverse:
			write_bam(read.qname,
					mergeReadPairs(read.seq,next_read.seq,read.tlen),
					read.flag,read.tid,
					read.reference_start,
					read.mapping_quality,
					read.cigartuples)
					
					
	elif  read.qname==next_read.qname and  not read.tid==next_read.tid:
		write_bam(read.qname,
					handleSingletons(read.seq),
					read.flag,
					read.tid,
					read.reference_start,
					read.mapping_quality,
					read.cigartuples)
						
		write_bam(next_read.qname,
					handleSingletons(next_read.seq),
					next_read.flag,
					next_read.tid,
					next_read.reference_start,
					next_read.mapping_quality,
					next_read.cigartuples)


	if read.qname != next_read.qname:
		write_bam(read.qname,
					handleSingletons(read.seq),
					read.flag,
					read.tid,
					read.reference_start,
					read.mapping_quality,
					read.cigartuples)
		BAM.seek(pos)
		
		
outfile.close()
