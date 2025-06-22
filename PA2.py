#!/usr/bin/env python3

import sys

fpath = sys.argv[1]

FT=[]
for line in open(fpath):
	line=line.strip()
	if line[0]!='@':
		col=line.split('\t')
		FT.append((int(col[1]),int(col[3]),int(col[7]),int(col[8])))

def rem(x,n):
	for i in range(n-1): x=x//2
	return x%2

SR=[];PR=[]
for c in FT:
	if rem(c[0],1)==1: PR.append(c)
	elif rem(c[0],1)==0: SR.append(c)

PAR=[];NPA=[]
for c in PR:
	if rem(c[0],2)==1 and rem(c[0],3)==0 and rem(c[0],4)==0: PAR.append(c)
	else: NPA.append(c)

FR1PE=[];FR1MP=[];RR1PE=[];RR1MP=[];FR2PE=[];FR2MP=[];RR2PE=[];RR2MP=[];NN=[]
for c in PAR:
	if rem(c[0],8)==0 and rem(c[0],7)==1 and rem(c[0],6)==1 and rem(c[0],5)==0:
		if c[3]>0:  FR1PE.append(c)
		elif c[3]<0:  FR1MP.append(c)
	elif rem(c[0],8)==0 and rem(c[0],7)==1 and rem(c[0],6)==0 and rem(c[0],5)==1:
		if c[3]>0:  RR1MP.append(c)
		elif c[3]<0:  RR1PE.append(c)
	elif rem(c[0],8)==1 and rem(c[0],7)==0 and rem(c[0],6)==1 and rem(c[0],5)==0:
		if c[3]>0:  FR2PE.append(c)
		elif c[3]<0:  FR2MP.append(c)
	elif rem(c[0],8)==1 and rem(c[0],7)==0 and rem(c[0],6)==0 and rem(c[0],5)==1:
		if c[3]>0:  RR2MP.append(c)
		elif c[3]<0:  RR2PE.append(c)
	else: NN.append(c)

pairs = {'GP':(FR1PE,RR2PE),'BP':(FR2PE,RR1PE),'GM':(RR1MP,FR2MP),'BM':(RR2MP,FR1MP)}
SP=0;SM=0;NNTP=[];NNTM=[];pe=0;mp=0
for key,(list1,list2) in pairs.items():
	dict2 = {}
	for j in list2:
	    dict_key = (j[2], j[1],-j[3])
	    if dict_key in dict2: dict2[dict_key].append(j)
	    else: dict2[dict_key] = [j]
	for i in list1:
		search = (i[1], i[2],i[3])
		if search in dict2 and dict2[search]:
			dict2[search].pop()
			if key in ['GP', 'BP']: SP += abs(i[3]); pe += 1
			elif key in ['GM', 'BM']: SM += abs(i[3]); mp += 1
		else:
			if key in ['GP', 'BP']: NNTP.append(i)
			elif key in ['GM', 'BM']: NNTM.append(i)

npa =  int(len(NPA)/2 if len(NPA)%2==0 else len(NPA)//2+1)
nn = int(len(NN)/2 if len(NN)%2==0 else len(NN)//2+1)

print('Single-end read 개수:',len(SR),'\t','Pair-end read 개수:',len(PR))
print('Properly aligned pair read 개수:',len(PAR),'\t','Properly alinged되지 않은 pair read 개수:',len(NPA))
print('정상PE,드문 PE,정상MP,드문MP:',(len(FR1PE),len(RR2PE)),(len(FR2PE),len(RR1PE)),(len(RR1MP),len(FR2MP)),(len(RR2MP),len(FR1MP)))
print('Properly aligned 되었지만 짝이 PE와MP 둘 다 아닌 read개수:',len(NN))
#print('NN:',NN)
print('PE,MP지만 짝이 없는pair read개수:',len(NNTP)+len(NNTM))
#print('NNTP:',NNTP);print('NNTM:',NNTM)
#Q=[]
#for line in open(fpath):
#	line=line.strip()
#	if line[0]!='@':
#		col=line.split('\t')
#		Q.append(col[0])
#D={}
#for q in Q:
#	if q not in D: D[q]=1
#	elif q in D: D[q]+=1
#c=0
#for value in D.values():
#	if value==2: c+=1
#print('Qname 개수:',len(D))
#print('Qname이 2번 등장한 read pair 수:',c)

print('[1]')
print('-the number of  read pairs:',npa+pe+mp+len(NNTP)+len(NNTM)+nn)
print('-the number of properly aligned read pairs:',pe+mp+nn)

print('[2]')
if pe>0:
	PTML=SP/pe
	print('-the number of properly PE:',pe)
	print('-PE TLEN mean:{:.2f}'.format(PTML))
	print('-PE Fraction:{:.4f}'.format(pe/(pe+mp)))
elif pe==0:
	print('-the number of properly PE: 0')
	print('-PE TLEN mean: 0')
	print('-PE Fraction: 0')

print ('[3]')
if mp>0:
	MTML=SM/mp
	print('-the number of properly MP:',mp)
	print('-MP TLEN mean:{:.2f}'.format(MTML))
	print('-MP Fraction:{:.4f}'.format(2*mp/(2*pe+2*mp)))
elif mp==0:
	print('-the number of properly MP: 0')
	print('-MP TLEN mean: 0')
	print('-MP Fraction: 0')

print('[4]')
if (pe/(pe+mp))>(mp/(pe+mp)): eit='PE'
elif (mp/(pe+mp))>(pe/(pe+mp)): eit='MP'
elif (pe/(pe+mp))==(mp/(pe+mp)): eit='PE와 MP 비율 동일'
print('-Estimated insert type:',eit)
if eit=='PE': tml=PTML
elif eit=='MP': tml=MTML
elif eit=='PE와 MP 비율 동일': tml=(PTML+MTML)/2
print('-mean length:{:.2f}'.format(tml))







