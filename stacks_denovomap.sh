ncores=4

#the process_radtags program takes a barcode file i.e 5bp internal barcode and 6bp illumina adapter sequence in a tab delimited file format.
#See the example file 'barcodes.txt'

#STEP 1: Run the process_radtags using the barcode files and input samples.
#STEP 2:
#keep all the sample names in a text file. see the 'sample_names.txt'
#To rename the process_radtags output file to original sample names, run the following four commands.
while read line; do cp `echo $line | awk '{ print $2".1.fq.gz " $1".1.fq.gz"}'` ; done < sample_names.txt
while read line; do cp `echo $line | awk '{ print $2".2.fq.gz " $1".2.fq.gz"}'` ; done < sample_names.txt
while read line; do cp `echo $line | awk '{ print $2".rem.1.fq.gz " $1".rem.1.fq.gz"}'` ; done < sample_names.txt
while read line; do cp `echo $line | awk '{ print $2".rem.2.fq.gz " $1".rem.2.fq.gz"}'` ; done < sample_names.txt

#STEP 3: If you would like to merge all the 1.fq.gz ,2.fq.gz ,1.rem.fq.gz and 2.rem.fq.gz run the following command.
while read line; do echo zcat `echo $line | awk '{ print  $1}'`.*.gz" > "`echo $line | awk '{ print  $1".fastq"}'`; done < sample_names.txt > combine_samples.sh
sh combine_samples.sh 
# OR if you have parallel installed
cat combine_samples.sh | parallel --jobs $ncores

#STEP 4: get the list of samples into an a string using the followin python one liner. Assuming that the Sample name ends with .fq
samples=`python -c 'import os; print " -s "+" -s ".join([x for x in os.listdir(".") if x.endswith(".fq")])'`

#STEP 5: Run stacks denovo_map.pl
denovo_map.pl $samples -b 1 -o ouputFolder -S -T $ncores -O popMap.txt
