#!/usr/bin/env python

import sys

fpath = sys.argv[1]

ln=0
D={}
q=0
seq=[]
prev=''

#print("번호\tseq길이\tA개수\tC개수\tG개수\tT개수\tN개수")
for line in open(fpath):
	ln+=1
	line=line.strip().upper()
	if prev.startswith('@') and (not set(line)-set('ACGTN')):
		q+=1;seq.append(len(line))
		a=0;c=0;g=0;t=0;n=0
		for i in range(len(line)):
			if line[i] == 'A':
				a+=1
			elif line[i] == 'C':
				c+=1
			elif line[i] == 'G':
				g+=1
			elif line[i] == 'T':
				t+=1
			else: n+=1
		D[q]=[a,c,g,t,n]
	prev=line
#		print(q,len(line),a,c,g,t,n,sep='\t')

M=[];V=[]
for j in range(5):
	s=0;v=0
	for i in D:
		s+=D[i][j]
	M.append(s/q)
	for i in D:
		v+=(D[i][j]-M[j])**2
	V.append(v)

print("<통계>")
print("총line 수:",ln)
print("sequence개수:",q)
print("총sequence길이:",sum(seq))
svar=sum((x - sum(seq)/q)**2 for x in seq)
print("sequence: 평균길이={:.2f},모표준편차={:.2f},표본표준편차={:.2f}".format(sum(seq)/q,(svar/q)**0.5,(svar/(q-1))**0.5))
L='ACGTN'
for k in range(5):
	print("{}: 평균길이={:.2f},모표준편차={:.2f},표본표준편차={:.2f}".format(L[k],M[k],V[k]/q,V[k]/(q-1)))


print("<그래프>")
G=[]
gap = int((max(seq)-min(seq))/10)
for i in range(10):
	G.append(min(seq)+gap*i)
C=[0]*len(G)
for num in seq:
	placed = False
	for i in range(len(G)-1):
		if num<G[i+1]:
			C[i]+=1
			placed=True
			break
	if not placed:
 		C[-1]+=1
	max_val = max(C)
S=[]
for val in C:
	star_count = round((val/max_val)*50)
	S.append('*'*star_count)

if gap == 0:
	print("All reads are {}bp long!".format(max(seq)))
else:
	print("{:<9}\t{:<6}\t{}".format("seq범주(10구간)", "seq개수", "비율시각화"))
	for n in range(len(G)):
			print("{:<9}\t{:<6}\t{}".format(G[n], C[n], S[n]))
	
