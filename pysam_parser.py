#This is basic script to show the usage of pysam to fetch all possible read pairs.

# Different strategies of Read [Pairs]
#
# 1. Read and mate mapped to same chromosome
# 2. Read and mate mapped to different chromosome
# 3. Read is mapped but mate is not mapped ( it could be either R1 or R2 )
# 4. Read is singleton ( It could be R1 or R2)


import pysam,sys



filename = sys.argv[1]
reads = pysam.Samfile(filename)

for read in reads:
	if read.is_paired and read.is_read1:
	
		#This will work if read 1 is mapped but read2 is unmapped.
		if  read.mate_is_unmapped: 
			print "The mate is unmapped: ",read.qname
			
		pos = reads.tell()
		try:
			mate = reads.mate(read)
		except ValueError:
			continue
		finally:
			reads.seek(pos)

			#Strategy 1 when both the read and mate mapped to same CHR
		if read.tid == mate.tid:
			print "Both reads mapped to same Chr: ", read.qname			
				
			#Strategy 2 when the mate mapped to different chromosome
		elif read.tid != mate.tid:
			print "Mates mapped to different chr: ",read.qname,mate.qname
			
	elif not read.is_paired:
		print "Singleton: ",read.qname
	
	#This will work if read 2 is mapped but read1 is unmapped.
	if read.is_paired and read.is_read2 and read.mate_is_unmapped:
		print "The mate is unmapped: ",read.qname
