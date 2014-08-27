#This program 
from __future__ import print_function
import random


missing_samples=24
file_name="file4"

sample_names=[]
population_info=[]
locus_names=[]
main_array=[]

temp_array=[]

num_samples=0
for line in open(file_name,'r'):
    if line.startswith("\t"):
        locus_names.append(line)
        
    if not line.startswith("\t"):
        splitted=line.split("\t")
        data_columns = (len(splitted[2].strip().split()))
        sample_names.append(splitted[0])
        population_info.append(splitted[1])
        num_samples+=1


for i in range(0,data_columns):
    for line in open(file_name,'r'):
        if not line.startswith("\t"):
            splitFile=line.split("\t")
            snp_data=splitFile[2].strip().split()     
            temp_array.append(snp_data[i])
    for x in random.sample(range(1,num_samples,2),missing_samples):
        temp_array[x]=0
        temp_array[x-1]=0
    main_array.append(temp_array)
    temp_array=[]

main_array.insert(0,sample_names)
main_array.insert(1,population_info)

for locus in locus_names:
    print (locus)

x_MAX=num_samples
y_MAX=data_columns+2

for x in range(0,x_MAX):
    for y in range(0,y_MAX):
        if y<=1:
            print (main_array[y][x],end="\t")
        else:
            print (main_array[y][x],end=" ")
    print ()
