#!/opt/bin/python

import os,sys
import pdf2txt

def pdfminer(loadpath,writepath):
    Findnames=os.listdir(loadpath)
    for i in Findnames:
        if i.endswith('.pdf'):
            cmd = 'pdf2txt.py '+ os.path.join(loadpath,i) + ' > ' + os.path.join(writepath,i[:-4]) + '.txt'
            os.system(cmd)

def pdfbox(loadpath,writepath,jarpath='tools/pdfbox-app-2.0.0-RC1.jar'):
    Findnames=os.listdir(loadpath)
    if i.endswith('.pdf'):
        for i in Findnames:
            cmd = 'java -jar '+jarpath+' ExtractText '+ os.path.join(loadpath,i) + ' '+ os.path.join(writepath,i[:-4]) + '.txt'
            os.system(cmd)
    
def test():
    loadpath=r'../data/pdf/'
    writepath=r'../data/txt_from_pdf/'
    if not os.path.exists(writepath):
        os.mkdir(writepath)
    #pdfminer(loadpath,writepath)
    pdfbox(loadpath,writepath)