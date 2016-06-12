#coding:utf-8
import pdfConversion
import sys
import os
import yaml
from noiseFilter import noiseFilter

def main(pdf_dir,txt_dir,out_dir,method='pdfminer',subtitle_candidate_path='..\\knol\\subtitle_candidate.txt',subtitle_knowledge_path='..\\knol\\subtitle.yaml'):
    '''
    #conversion
    if method=='pdfbox':
        pdfConversion.pdfbox(pdf_dir,txt_dir)
    else:
        pdfConversion.pdfminer(pdf_dir,txt_dir)
    '''
    #clean,去除短行,同时获取subtitle_cadidates
    subtitle_candidate={}
    subtitle_knowledge={}
    #如果知识文件存在，则读取知识文件获得subtitle_knowledge
    if os.path.exists(subtitle_knowledge_path):
        f=open(subtitle_knowledge_path,'r')
        subtitle_knowledge=yaml.load(f)
        f.close()
    for root,dirs,fns in os.walk(txt_dir):
        for fn in fns:
            path=os.path.join(root,fn)
            nf=noiseFilter(path,subtitle_candidate,txt_cleaned_dir=out_dir,subtitle_knowledge=subtitle_knowledge)
            subtitle_candidate=nf.subtitle_candidate
    
    sub_file=open(subtitle_candidate_path,'w')
    for word in subtitle_candidate:
        sub_file.write(word+'\t'+str(subtitle_candidate[word])+'\n')
    sub_file.close()
    
if __name__=='__main__':
    argvs=sys.argv
    if '-pdfbox' in argvs:
        method='pdfbox'
    else:
        method='pdfminer'
    
    pdf_dir='..\\data\\pdf'
    #txt_dir='..\\data\\txt_from_pdf'
    txt_dir='..\\data\\txt_from_pdf'
    out_dir='..\\data\\txt_cleaned\\'
    main(pdf_dir,txt_dir,out_dir,method=method)