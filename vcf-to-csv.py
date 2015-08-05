#First convert the vcf file to tab format using vcf-to-tab

# cat test.vcf | vcf-to-tab | grep -v "^#" > tab.out

with open("tab.out") as f:
  for line in f:
      snps=line.strip().split()
      id="_".join(snps[:2])
      print id+","+",".join([snp.replace('./', 'N') for snp in snps[3:]]) #index starts with 3 because we have to ignore the reference allele.
