#coding:utf-8

from concept_stat import conceptStat 
from getNetwork import get_Network
import commonFunctions as cf
import yaml
import os

def outputConceptSummary(conceptSummary,outpath):
    #输出conceptSummary，用于人工review挑选general wrods
    #格式：CUI	concept	semantic_type	category	count_total	count_document	expressions
    file=open(outpath,'w')
    file.write('#CUI\tconcept\tsemanticType\tcategory\tcount_total\tcount_document\texpressions\n')
    for CUI in conceptSummary:
        sub=conceptSummary[CUI]
        concept=sub['concept']
        semanticType=sub['semanticType']
        category=sub['category']
        count_total=sub['count_total']
        count_document=sub['count_document']
        expressions='||'.join(sub['string'])
        file.write('\t'.join([CUI,concept,semanticType,category,str(count_total),str(count_document),expressions])+'\n')
    file.close()    
    
def outputConceptsInFile(conceptsInFile,date,outpath,option='cui'):
    #option 可以为 'cui' 或 'term', cui表示输出概念的唯一id, term表示输出概念的首选词
    category_list=cf.CATEGORYs

    #输出conceptsInFile,作为网络节点的属性
    #格式：filenames	0date	0concept_num	及各个category下的concept
    file=open(outpath,'w')
    file.write('#filename\tdate\tconcept_num\t'+'\t'.join(category_list)+'\n')
    for filename in conceptsInFile:
        d=date[filename]
        concept_num=0
        line=[]
        for cat in category_list:
            concepts=[]
            if conceptsInFile[filename].has_key(cat):
                for cui in conceptsInFile[filename][cat]:
                    concept=conceptsInFile[filename][cat][cui]['concept']
                    if option=='cui':
                        concepts.append(cui)
                    elif option=='term':
                        concepts.append(concept)
                    else:
                        print '[ERROR,step3]: wrong option in outputConceptsInFile!'
            if concepts==[]:
                content='none'
            else:
                concept_num+=len(concepts)
                content='||'.join(concepts)
            line.append(content)
        line=[filename,d,str(concept_num)]+line
        line='\t'.join(line)
        file.write(line+'\n')
        
    file.close()
    
def groupConceptInFile(conceptInFile):
    ConceptInFile_groupbycat={}
    for filename in conceptInFile:
        ConceptInFile_groupbycat[filename]={}
        #每一个concept为一个sample
        for CUI in conceptInFile[filename].keys():
            sample=conceptInFile[filename][CUI]
            category=sample['category']
            semanticType=sample['semanticType']
            count=sample['count']
            concept=sample['concept']
            if not ConceptInFile_groupbycat[filename].has_key(category):
                ConceptInFile_groupbycat[filename][category]={CUI:{'concept':concept,'semanticType':semanticType,'count_concept':count}}
            else:
                ConceptInFile_groupbycat[filename][category][CUI]={'concept':concept,'semanticType':semanticType,'count_concept':count}
                
    return ConceptInFile_groupbycat

def main(metamapRe_dir,generalConcepts_path,generalStrings_path,targetSemanticType_path,output_dir,date_path='..\\knol\\cas9_PMID_date.txt'): 
    conceptSummary_path=os.path.join(output_dir,'conceptSummary.txt')
    conceptsInFile_path=os.path.join(output_dir,'conceptsInFile.txt')
    network_path=os.path.join(output_dir,'Network_file.txt')
    
    #获取pmid对应的date信息
    date=cf.getDate(date_path)
    
    #统计metamap结果：统计每个concept所属的Semantic Type,计算其共出现多少次，在多少个文档中出现；统计每个文档出现过的concept及其所属的semantic type和出现次数。
    cs=conceptStat(metamapRe_dir,Concerned_Semantic_type_path=targetSemanticType_path,generalConcepts_path=generalConcepts_path,generalStrings_path=generalStrings_path)
    conceptsInFile=cs.conceptsInFile
    conceptSummary=cs.conceptSummary
    '''
    #输出conceptSummary，用于人工review挑选general wrods
    outputConceptSummary(conceptSummary,conceptSummary_path)
    
    #将conceptsInFile进行一定程度的格式转换，用于生成网络
    conceptsInFile=groupConceptInFile(conceptsInFile)
    
    #输出conceptsInFile，作为网络节点的属性
    outputConceptsInFile(conceptsInFile,date,conceptsInFile_path)
    
    #根据metamap统计结果，生成网络
    network=get_Network(conceptsInFile,date,network_path,direction_choice='L2F')
    '''
if __name__=='__main__':
    metamapRe_dir='..\\data\\MetamapRe\\method2acknow_merged'
    generalConcepts_path='..\\knol\\generalConcepts.txt'
    generalStrings_path='..\\knol\\generalStrings.txt'
    targetSemanticType_path='..\\knol\\target_semanticType.txt'
    output_dir='..\\data\\result\\method2acknow_merged'
    
    main(metamapRe_dir,generalConcepts_path,generalStrings_path,targetSemanticType_path,output_dir)