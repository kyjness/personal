#!/usr/bin/env python3

import sys

assem = sys.argv[1]

D={}
for line in open(assem):
	line = line.strip()
	if line.startswith('>'):
		info = line
		D[info] = []
	else: 
	 	D[info].append(line)

D = {k: v for k, v in D.items() if len(''.join(v)) >= 1000}

for k,v in D.items():
	print("{0}\n{1}".format(k,v))
