# This script should be placed in a folder where the bam files resides and then run `sh realign_bam_parallel.sh`
#This script 1) adds read group information 2)index the bam files 3) create interval files 4) realign the bam files

ncores=4 #Change this parameter depending on number of cores in your computer

#Add readgroup information
parallel --jobs $ncores java -Xmx8g -jar picard-tools-1.106/AddOrReplaceReadGroups.jar I={} O={.}_RG.bam RGID={.} RGLB=lib1 RGPL=illumina RGPU=unit1 RGSM={.} ::: *.bam

#index bam
parallel --jobs $ncores samtools index {} ::: sorted*_RG.bam

#Create Interval File
parallel --jobs $ncores java -Xmx8g -jar GenomeAnalysisTK.jar -T RealignerTargetCreator -R Genome.fa -I {} -o {.}.intervals ::: sorted*_RG.bam

#realign bases around indels
parallel --jobs $ncores java -Xmx8g -jar GenomeAnalysisTK.jar -T IndelRealigner -R Genome.fa -I {} -targetIntervals {.}.intervals  -o {.}_realigned.bam ::: sorted*_RG.bam

#index realigned files
parallel --jobs $ncores samtools index {} ::: sorted*_realigned.bam

#call SNP using samtools 
#parallel --jobs $ncores "samtools mpileup -E -uf Genome.fa {} | bcftools view -cg - | vcfutils.pl varFilter -d 3 > {.}.vcf" ::: sorted*_realigned.bam
