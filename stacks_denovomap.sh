#get the list of samples into an a string using the followin python one liner.

#Assuming that the Sample name ends with .fq
samples=`python -c 'import os; print " -s "+" -s ".join([x for x in os.listdir(".") if x.endswith(".fq")])'`

ncores=4

#Run stacks denovo_map.pl

denovo_map.pl $samples -b 1 -o ouputFolder -S -T $ncores -O popMap.txt
