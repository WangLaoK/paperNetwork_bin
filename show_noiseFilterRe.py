#coding:utf-8

import os
import commonFunctions as cf

def deleteBlankLines(lines):
    newLines=[]
    for l in lines:
        l=l.strip()
        if l!='':
            newLines.append(l)
    return newLines

def main():
    original_dir='..\\data\\txt_from_pdf'
    cleaned_dir='..\\data\\txt_cleaned\\'
    line_number_path='..\\data\\result\\show_noiseFilterRe_lineNumber.txt'
    noies_line_length_path='..\\data\\result\\show_noiseFilterRe_NoiseLineLength.txt'
    cleaned_line_length_path='..\\data\\result\\show_noiseFilterRe_CleanedLineLength.txt'
    
    line_number={}  #存储每个文件的行数
    lines={'noise':[],'cleaned':[]}
    
    original_fns=os.listdir(original_dir)
    cleaned_fns=os.listdir(cleaned_dir)

    #获取所需数据
    if set(original_fns)!=set(cleaned_fns):
        print "Two directory are not the same!!!"
    else:
        for fn in original_fns:
            oriPath=os.path.join(original_dir,fn)
            clePath=os.path.join(cleaned_dir,fn)
            
            oriFile=open(oriPath,'r')
            cleFile=open(clePath,'r')
            
            oriLines=oriFile.readlines()
            cleLines=cleFile.readlines()
            
            #去空行和strip
            oriLines=deleteBlankLines(oriLines)
            cleLines=deleteBlankLines(cleLines)
            if not (set(cleLines)<set(oriLines)):
                print fn
                print len(set(oriLines))-len(set(cleLines))
                print len(set(oriLines)-set(cleLines))
                print '====================='
            noiseLines=list(set(oriLines)-set(cleLines))
            
            line_number[fn]={'original':str(len(oriLines)),'cleaned':str(len(cleLines)),'noise':str(len(noiseLines))}
            lines['noise']+=noiseLines
            lines['cleaned']+=cleLines
            
            oriFile.close()
            cleFile.close()
    
    #将所需数据输出到结果
    file=open(line_number_path,'w')
    for fn in line_number:
        file.write(fn+'\t'+line_number[fn]['original']+'\t'+line_number[fn]['cleaned']+'\t'+line_number[fn]['noise']+'\n')
    file.close()
    
    file=open(noies_line_length_path,'w')
    for line in lines['noise']:
        line=cf.clean(line)
        #file.write(str(len(line))+'\n')
        file.write(str(len(line))+'\t'+line+'\n')
    file.close()
    
    file=open(cleaned_line_length_path,'w')
    for line in lines['cleaned']:
        line=cf.clean(line)
        #file.write(str(len(line))+'\n')
        file.write(str(len(line))+'\t'+line+'\n')
    file.close()
main()