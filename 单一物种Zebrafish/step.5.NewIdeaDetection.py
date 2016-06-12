#coding:utf-8

import commonFunctions as cf
import datetime
import yaml
import json

#获得concept在领域中第一次出现的时间
def generateConceptHistory(date_sort,conceptsInFile,conceptsInfo,Cas9category='NONE',Cas9concept='NONE'):
    conceptHis={}
    category_list=cf.CATEGORYs
    #Cas9第一次出现时间
    cutofftime=datetime.datetime(2013,1,1)
    for item in date_sort:
        pmid=item[0]
        date=item[1]
        format_date=datetime.datetime(int(date[:4]),int(date[4:6]),int(date[6:]))
        #必须在Cas9第一次发表之后计算newidea
        if (format_date-cutofftime).days>0:
            if conceptsInFile.has_key(pmid):
                for cate in category_list:
                    CUIs=conceptsInFile[pmid][cate]
                    for CUI in CUIs:
                        #如果该类别内无concept，则跳过
                        if CUI=='none':
                            continue
                        #通过CUI获取concept的CUI等信息
                        cInfo=conceptsInfo[CUI]
                        
                        concept=cInfo['concept']
                        semanticType=cInfo['semanticType']
                        category=cInfo['category']
                        count_document=cInfo['count_document']
                        #if Cas9category!='NONE':
                        #    if category!=Cas9category:
                        #        break
                        
                        if Cas9concept!='NONE':
                            if concept!=Cas9concept:
                                break
                        
                        sub={'date':format_date,'pmid':pmid,'concept':concept,'count_document':count_document}
                        if conceptHis.has_key(CUI):
                            #如果历史里已经有了该概念，则判断，若距离最早的时间不超过6个月，则append到conceptHis
                            first_date=conceptHis[CUI][0]['date']
                            month=float((format_date-first_date).days)/30
                            #不考虑重复项，只考虑第一次
                            #没有6个月限制
                            #if month<=6:
                            conceptHis[CUI].append(sub)
                        else:
                            conceptHis[CUI]=[sub]                    
            
    return conceptHis

def main(conceptsInFile_path,conceptSummary_path,out_path,date_path='..\\knol\\PMID_data_2014.06.10.txt'):
    #获取pmid对应的date信息
    date=cf.getDate(date_path)
    #对date按照时间排序
    date_sort=sorted(date.iteritems(),key=lambda x:x[1],reverse=False)
    
    #根据数据获得每个文件里每个category的CUI list
    conceptsInFile=cf.parseConceptsInFile(conceptsInFile_path)
    
    #根据数据获得每个concept的CUI,首选词,semanticType,category. 以CUI为key
    conceptsInfo=cf.getCUIInfo_CUIAsKey(conceptSummary_path)
    
    #选定的Cas9目标category
    #Cas9category='Disease_pathologic'
    
    #选定的Cas9目标species
    Cas9concept='Zebrafish'
    
    #以时间顺序遍历文献，获取每个concept第一次出现的时间，对应的文章等信息
    conceptHis=generateConceptHistory(date_sort,conceptsInFile,conceptsInfo,'NONE',Cas9concept)
    
    #将conceptHis转为可视化所需要的json格式
    conceptHis_json=cf.conceptHis2Json(conceptHis)
    
    #将conceptHis输出到json文件
    outfile=open(out_path,'w')
    data=json.dumps(conceptHis_json,sort_keys=True,indent=4)
    outfile.write(data)
    outfile.close()    
    
if __name__=='__main__':
    conceptsInFile_path='..\\data\\result\\method2acknow_merged\\conceptsInFile.txt'
    conceptSummary_path='..\\data\\result\\method2acknow_merged\\conceptSummary.txt'
    out_path='..\\data\\result\\method2acknow_merged\\conceptHistory.json'
    main(conceptsInFile_path,conceptSummary_path,out_path)