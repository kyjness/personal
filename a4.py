#!/usr/bin/env python3

import sys

fpath = sys.argv[1]

a=0;b=0;c=0;d=0
print("[log2FC_TPM>1]")
for line in open(fpath):
	line = line.strip()
	col = line.split('\t')
	if float(col[6]) > 1:
		print(line)
		a += 1
print("개수:",a)
print("[log2FC_TPM<-1]")
for line in open(fpath):
	line = line.strip()
	col = line.split('\t')
	if float(col[6]) < -1:
		print(line)
		b += 1
print("개수:",b)
print("[log2FC_MR>1]")
for line in open(fpath):
	line = line.strip()
	col = line.split('\t')
	if float(col[9]) > 1:
		print(line)
		c += 1
print("개수:",c)
print("[log2FC_MR<-1]")
for line in open(fpath):
	line = line.strip()
	col = line.split('\t')
	if float(col[9]) < -1:
		print(line)
		d += 1
print("개수:",d)
