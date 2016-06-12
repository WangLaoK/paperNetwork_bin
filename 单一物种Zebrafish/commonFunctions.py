#coding:utf-8

import chardet
import re 

CATEGORYs=['Material_gene','Material_species','Disease_pathologic','Disease_Symptom','Material_organ','Material_cell','Material_tissue','Method_Activity','Method_device','Method_Health','Method_procedure']

def getDate(date_path):
    #get date for every paper
    date_dict={}
    date_file=open(date_path,'r')
    date_data=date_file.readlines()
    date_file.close()
    
    for line in date_data:
        if not line.startswith('#'):
            line=line.strip().split('\t')
            if len(line)==2:
                pmid=line[0]
                date=line[1]
                date_dict[pmid]=date
    
    return date_dict
    
#根据数据获得每个文件里每个category的concept首选词
def parseConceptsInFile(filePath,header=True):
    res={}  #存储结果，以第一列filename为key，存储该文件的日期，concept个数，及每个category下的CUI list
    file=open(filePath,'r')
    data=file.readlines()
    file.close()
    
    if header and data[0].startswith('#'):
        heads=data[0][1:].strip().split('\t')    #去除#号

    for line in data:
        if line.strip()!='' and (not line.startswith('#')):
            line=line.strip().split('\t')
            filename=line[0]
            date=line[1]
            concept_num=line[2]
            res[filename]={'date':date,'concept_num':concept_num}
            for col in range(3,len(line)):
                res[filename][heads[col]]=line[col].split('||')
    
    return res

#获取CUI,首选词,semanticType, category的映射信息。此方法返回的结果是以首选词为key。且因为有可能一个term对应多个concept，所以concept对应的信息为list
def getCUIInfo_termAsKey(filePath,header=True):
    conceptsInfo={}
    file=open(filePath,'r')
    data=file.readlines()
    file.close()
    
    if header and data[0].startswith('#'):
        heads=data[0][1:].strip().split('\t')    #去除#号
    
    for line in data:
        if line.strip()!='' and (not line.startswith('#')):
            line=line.strip().split('\t')
            CUI=line[0]
            concept=line[1]
            semanticType=line[2]
            category=line[3]
            count_total=line[4]
            count_document=line[5]
            sub={'CUI':CUI,'semanticType':semanticType,'category':category,'count_document':count_document,'concept':concept}
            
            if conceptsInfo.has_key(concept):
                conceptsInfo[concept].append(sub)
            else:
                conceptsInfo[concept]=[sub]
    
    return conceptsInfo

#获取CUI,首选词,semanticType, category的映射信息。此方法返回的结果是以CUI为key
def getCUIInfo_CUIAsKey(filePath,header=True):
    conceptsInfo={}
    file=open(filePath,'r')
    data=file.readlines()
    file.close()
    
    if header and data[0].startswith('#'):
        heads=data[0][1:].strip().split('\t')    #去除#号
    
    for line in data:
        if line.strip()!='' and (not line.startswith('#')):
            line=line.strip().split('\t')
            CUI=line[0]
            concept=line[1]
            semanticType=line[2]
            category=line[3]
            count_total=line[4]
            count_document=line[5]
            sub={'CUI':CUI,'semanticType':semanticType,'category':category,'count_document':count_document,'concept':concept}
            
            conceptsInfo[CUI]=sub
    
    return conceptsInfo

#根据输入的concept及其category，从conceptsInfo中找到其相关信息。需要给category是以防一个term有多个意思及对应的CUI
def getInfoByTerm(concept,conceptsInfo,category=None):
    res=[]
    if not conceptsInfo.has_key(concept):
        print "[EROOR.CF]cannot find the term '"+concept+"' in conceptsInfo!"
        return []
    candidates=conceptsInfo[concept]
    if category==None:
        res=candidates
    else:
        for item in candidates:
            if item['category']==category:
                res.append(item)
    
    if len(res)>1:
        print "[WARNING.CF]More than one candidate concepts for term :'"+concept+"'!"
    elif len(res)<1:
        print "[WARNING.CF]No candidate concepts for term :'"+concept+"'!"
    return res    

def changeCode2Ascii(string):
    if chardet.detect(string)['encoding']!='ascii':
        code=chardet.detect(string)['encoding']
        string=string.decode('utf-8')
    return string

def writeToFile(file,line):
    try:
        file.write('%s\n'%(line))
    except:
        pass

#将conceptHis转为可视化所需要的json格式
def conceptHis2Json(conceptHis):
    json_re=[]
    for cui in conceptHis:
        i=0
        for index in range(len(conceptHis[cui])):
            sub={}
            i+=1
            sub['id']=str(cui)+','+str(i)
            #sub['id']=str(cui)
            sub['title']=conceptHis[cui][index]['pmid']
            #sub['title']=conceptHis[cui][index]['concept']
            sub['description']=cui+'\t'+conceptHis[cui][index]['count_document']+'\t'+conceptHis[cui][index]['pmid']
            sub['startdate']=str(conceptHis[cui][index]['date'])
            sub['high_threshold']=50
            #sub['importance']=int(int(conceptHis[cui][index]['count_document'])**0.5)*10
            sub['importance']=50
            
            sub['date_display']='da'
            sub['icon']='red_shu.png'
            json_re.append(sub)
    return json_re

#对一行的内容进行clean，去除数字百分比等
def clean(line):
    ####清除百分比，连续碱基
    pattern1='\d+(\.\d+)*\%'
    line=re.sub(pattern1,'',line)
    
    pattern2='\s\d+(\.\d+)*'
    line=re.sub(pattern2,' ',line)
    
    line=re.sub('[ATCGUatcgu\s]{6,}','',line)
    
    line=re.sub('\s+',' ',line)
    return line