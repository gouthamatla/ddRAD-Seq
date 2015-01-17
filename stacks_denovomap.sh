#the process_radtags program takes a barcode file i.e 5bp internal barcode and 6bp illumina adapter sequence in a tab delimited file format.
#See the example file 'barcodes.txt'

#keep all the sample names in a text file. see the 'sample_names.txt'

#To rename the process_radtags output file to original sample names, run the following four commands.
while read line; do cp `echo $line | awk '{ print $2".1.fq.gz " $1".1.fq.gz"}'` ; done < sample_names.txt
while read line; do cp `echo $line | awk '{ print $2".2.fq.gz " $1".2.fq.gz"}'` ; done < sample_names.txt
while read line; do cp `echo $line | awk '{ print $2".rem.1.fq.gz " $1".rem.1.fq.gz"}'` ; done < sample_names.txt
while read line; do cp `echo $line | awk '{ print $2".rem.2.fq.gz " $1".rem.2.fq.gz"}'` ; done < sample_names.txt



#get the list of samples into an a string using the followin python one liner.

#Assuming that the Sample name ends with .fq
samples=`python -c 'import os; print " -s "+" -s ".join([x for x in os.listdir(".") if x.endswith(".fq")])'`

ncores=4

#Run stacks denovo_map.pl

denovo_map.pl $samples -b 1 -o ouputFolder -S -T $ncores -O popMap.txt
