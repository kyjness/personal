#!/usr/bin/env python3

import sys
import math

normal = sys.argv[1]
patient = sys.argv[2]
gtf = sys.argv[3]

D={}
for line in open(gtf):
	line=line.strip()
	if line.startswith('chr'):
		col=line.split('\t')
		col8=col[8].split(';')
		if col[2] == 'gene':
			genelength = int(col[4])-int(col[3])+1
			geneid = [x.split('"')[1] for x in col8 if 'gene_id' in x][0]
			genename = [x.split('"')[1] for x in col8 if 'gene_name' in x]
			genename = genename[0] if genename else ' '
			D[geneid]=[col[0],col[3],col[4],genelength,genename]	

C={}
for line in open(normal):
	line = line.strip()
	col = line.split('\t')
	geneid = col[0]
	if geneid in D and int(col[1])>0:
		rpk = int(col[1])*1000/(D[geneid][3])
		C[geneid] = [D[geneid][4],D[geneid][0],D[geneid][1],D[geneid][2],rpk]

for line in open(patient):
	line = line.strip()
	col = line.split('\t')
	geneid = col[0]
	if geneid in D and int(col[1])>0 and geneid in C:
		rpk = int(col[1])*1000/(D[geneid][3])
		C[geneid].append(rpk)

C = {k: v for k, v in C.items() if len(v) > 5}
sn = sum([v[4] for v in C.values()]) 
sp = sum([v[5] for v in C.values()])

for geneid in C:
	C[geneid][4] = C[geneid][4]/sn*1000000 if sn>0 else 0 
	C[geneid][5] = C[geneid][5]/sp*1000000 if sp>0 else 0

for line in open(normal):
	line = line.strip()
	col = line.split('\t')
	geneid = col[0]
	if geneid in C:
		rpk = int(col[1])
		C[geneid].append(rpk)
for line in open(patient):
	line = line.strip()
	col = line.split('\t')
	geneid = col[0]
	if geneid in C:
		rpk = int(col[1])
		C[geneid].append(rpk)

NL=[];PL=[]
for geneid in C:
	geomean = (C[geneid][6]*C[geneid][7])**0.5
	NL.append(C[geneid][6]/geomean)
	PL.append(C[geneid][7]/geomean)

NL.sort();PL.sort()
nl = len(NL);pl = len(PL)
if nl % 2 == 1: medn = NL[nl // 2] 
else: medn = (NL[nl // 2 - 1] + NL[nl // 2]) / 2.0
if pl % 2 == 1: medp = PL[pl // 2]
else: medp = (PL[pl // 2 - 1] + PL[pl // 2]) / 2.0

for geneid in C:
	C[geneid][6] = C[geneid][6]/medn
	C[geneid][7] = C[geneid][7]/medp

for geneid in C:
	C[geneid].append(math.log2(C[geneid][5]/C[geneid][4]))
	C[geneid].append(math.log2(C[geneid][7]/C[geneid][6]))

#for key,value in C.items():
#	print(key,value)

sorted_genename = sorted(C.keys(), key=lambda gid: C[gid][0])

print("Gene name\tchromosome\tstart\tend\tTPM_patient\tTPM_normal\tlog2FC_TPM\tMR_patient\tMR_normal\t log2FC_MR")

for geneid in sorted_genename:
	genename = C[geneid][0]
	chrmo = C[geneid][1]
	start = C[geneid][2]
	end = C[geneid][3]
	tpm_p = C[geneid][5]
	tpm_n = C[geneid][4]
	log2fc_tpm = C[geneid][8]
	mr_p = C[geneid][7]
	mr_n = C[geneid][6]
	log2fc_mr = C[geneid][9]
	
	print("{}\t{}\t{}\t{}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}".format(
				genename, chrmo, start, end, tpm_p, tpm_n, log2fc_tpm, mr_p, mr_n, log2fc_mr
				))

print("총 유전자 개수:",len(C))
