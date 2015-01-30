# Different strategies of Read [Pairs]
#
# 1. Read and mate mapped to same chromosome
# 2. Read and mate mapped to different chromosome
# 3. Read is mapped but mate is not mapped ( it could be either R1 or R2 )
# 4. Read is singleton ( It could be R1 or R2)
# Usage: python merge_read_pairs.py <input bam> < output sam>


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

def write_to_bam():
	pass


filename = sys.argv[1]
outfile_name=sys.argv[2]
reads = pysam.Samfile(filename)


header=reads.header

outfile = pysam.AlignmentFile(outfile_name, "wh", header=header)
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
	


for read in reads:
	if read.is_paired and read.is_read1:
	
		#This will work if read 1 is mapped but read2 is unmapped.
		if  read.mate_is_unmapped: 
			write_bam(read.qname,handleSingletons(read.seq),read.flag,read.tid,read.reference_start,read.mapping_quality,read.cigartuples)
			
		pos = reads.tell()
		try:
			mate = reads.mate(read)
		except ValueError:
			continue
		finally:
			reads.seek(pos)

			#Strategy 1 when both the read and mate mapped to same CHR. Sometimes, insert length may be less than the read length, discard them
		if (read.tid == mate.tid) and abs(read.tlen)>len(read.seq):
			if read.is_reverse:
				write_bam(read.qname,
						mergeReadPairs(mate.seq,read.seq,read.tlen),
						read.flag,read.tid,
						mate.reference_start,
						read.mapping_quality,
						read.cigartuples)
			elif mate.is_reverse:
				write_bam(read.qname,
						mergeReadPairs(read.seq,mate.seq,read.tlen),
						read.flag,read.tid,
						read.reference_start,
						read.mapping_quality,
						read.cigartuples)



			#Strategy 2 when the mate mapped to different chromosome
		elif read.tid != mate.tid:
			write_bam(read.qname,
						handleSingletons(read.seq),
						read.flag,
						read.tid,
						read.reference_start,
						read.mapping_quality,
						read.cigartuples)
						
			write_bam(mate.qname,
						handleSingletons(mate.seq),
						mate.flag,
						mate.tid,
						mate.reference_start,
						mate.mapping_quality,
						mate.cigartuples)
			
	elif not read.is_paired:
		write_bam(read.qname,
					handleSingletons(read.seq),
					read.flag,
					read.tid,
					read.reference_start,
					read.mapping_quality,
					read.cigartuples)

	#This will work if read 2 is mapped but read 1 is unmapped.
	if read.is_paired and read.is_read2 and read.mate_is_unmapped:
		write_bam(read.qname,
					handleSingletons(read.seq),
					read.flag,
					read.tid,
					read.reference_start,
					read.mapping_quality,
					read.cigartuples)		
		
outfile.close()
