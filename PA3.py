#!/usr/bin/env python3

import sys

fpath = sys.argv[1]

D={}
for line in open(fpath):
	line=line.strip()
	if line.startswith('chr'):
		col=line.split('\t')
		col4=col[4].split(',')
		col7=col[7].split(';')
		dp_value = float([x.split('=')[1] for x in col7 if x.startswith('DP=')][0])
		af_value = float([x.split('=')[1] for x in col7 if x.startswith('AF=')][0])
		if len(col4)==1 and float(col[5])>=20 and dp_value>=20 and af_value==1:
			if col[0] not in D:
				D[col[0]] = []
			D[col[0]] += [(col[3],col[4])]

#print(D)

print("{The number and length for each chromosome}")
print()
ssubn=0;sinsn=0;sdeln=0;ssubl=0;sinsl=0;sdell=0
for key in D:
	subn=0;insn=0;deln=0;subl=0;insl=0;dell=0
	for value in D[key]:
		vr=value[0].lower()
		va=value[1].lower()
		if len(vr)==len(va):
			for i in range(len(vr)):
				if vr[i] != va[i]: subl += 1
			subn+= 1
		elif len(vr)>len(va):
			dell+=len(vr)-len(va)
			deln += 1
		elif len(vr)<len(va):
			insl+=len(va)-len(vr)
			insn += 1
	ssubn+=subn;sinsn+=insn;sdeln+=deln;ssubl+=subl;sinsl+=insl;sdell+=dell
	if subn>0: print(key,'substitution number:',subn)
	if subl>0: print(key,'substitution length:',subl)
	if insn>0: print(key,'insertion number:',insn)
	if insl>0: print(key,'insertion length:',insl)
	if deln>0: print(key,'deletion number:',deln)
	if dell>0: print(key,'deletion length:',dell)
	print('-----------------------------')

print()
print("{Total number and length}")
print()
print("Total substitution number:",ssubn)
print("Total substitution length:",ssubl)
print("Total insertion number:",sinsn)
print("Total insertion length:",sinsl)
print("Total deletion number:",sdeln)
print("Total deletion length:",sdell)


