#!/usr/bin/env python3

import sys

assem = sys.argv[1]

D={}
for line in open(assem):
	line = line.strip()
	if line.startswith('>'):
		line = line[1:]
		col = line.split(' ')
		name = col[0]
		D[name] = []
	else: 
	 	D[name] = len(line)
print("The number of total sequences:",len(D))

total_length = sum([v for v in D.values()])
print("Total length of sequences:",total_length)

longest = max([v for v in D.values()])
print("The length of the longest sequence:",longest)

shortest = min([v for v in D.values()])
print("The length of the shortest sequence:",shortest)

sorted_D = sorted(D.keys(), key=lambda x: D[x],reverse=True)
s=0
for name in sorted_D:
	value = D[name]
	s += value
	if s >= total_length/2:
		break
print("N50:",value)

print("<Distribution of sequence lengths>")
G=[]
gap = (longest-shortest)/10
for i in range(10):
	G.append(shortest+gap*i)
C=[0]*len(G)
for num in D.values():
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

print("{:<9}\t{:<6}\t{}".format("seq범주(10구간)", "seq개수", "비율시각화"))
for n in range(len(G)):
	print("{:<9.2f}\t{:<6}\t{}".format(G[n], C[n], S[n]))


