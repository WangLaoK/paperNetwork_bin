#coding:utf-8

import re 

medline_path='..\\network_approach\\materials\\cas9_researchRe\\fromPUBMED_2015.1.22\\cas9_medline.txt'
out_dir='..\\network_approach\\literature\\abs\\'
f=open(path,'r')
data=f.readlines()
f.close()

ab_dict={}

pmid=''
ab=''
ab_start=0
for i in range(0,len(data)):
    line=data[i]
    
    if line.startswith('PMID- '):
        if len(ab)!=0 and pmid!='':
            ab_dict[pmid]=ab
            
        pmid=line[6:].strip()
        ab=''
        ab_start=0

    if line.startswith('AB  - '):
        ab=line[6:].strip()
        ab_start=1
    else:
        if ab_start==1 and line.startswith('    '):
            ab+=' '+line.strip()
        if ab_start==1 and line[0]!=' ':
            ab_start=0
        
for key in ab_dict:
    p=out_dir+key+'.txt'
    f=open(p,'w')
    f.write(ab_dict[key])
    f.close()