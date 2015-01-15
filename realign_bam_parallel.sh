# This script should be placed in a folder where the bam files resides and then run `sh realign_bam_parallel.sh`
#This script 1) adds read group information 2)index the bam files 3) create interval files 4) realign the bam files

#Add readgroup information
parallel java -Xmx8g -jar picard-tools-1.106/AddOrReplaceReadGroups.jar I={} O=`echo {.} | awk '{ print \$1"_RG.bam"}'` RGID=`echo {.} | awk '{ print \$1 }'` RGLB=lib1 RGPL=illumina RGPU=unit1 RGSM=`echo {.} | awk '{ print \$1 }'` ::: *.bam

#index bam
parallel samtools index {} ::: sorted*_RG.bam

#Create Interval File
parallel java -Xmx8g -jar ~/softs/GenomeAnalysisTK.jar -T RealignerTargetCreator -R ~/ddRAD_data/Genome/ref_PanTig1.0_chrUn.fa -I {} -o `echo {.} | awk '{ print $1".intervals"}'` ::: sorted*_RG.bam
wait 

#realign bases around indels
parallel  java -Xmx8g -jar GenomeAnalysisTK.jar -T IndelRealigner -R ~/ddRAD_data/Genome/ref_PanTig1.0_chrUn.fa -I {} -targetIntervals `echo {.} | awk '{ print $1".intervals"}'`  -o `echo {.} | awk '{ print $1"_realigned.bam"}'` ::: sorted*_RG.bam

#index realigned files
parallel samtools index {} ::: sorted*_realigned.bam
