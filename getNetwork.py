# =-= coding:utf-8  =-=

import os,sys,re,yaml,datetime
import copy

class get_Network():
    def __init__(self,ConceptInFile,pubmed_date={},network_path='..\\result\\Network_file.txt',direction_choice='F2L'):
        #F2L表示先发表的指向后发表的，L2F则反之
        self.ConceptInFile=ConceptInFile
        self.network_path=network_path
        self.pubmed_date=pubmed_date
        self.direction_choice=direction_choice
        
        self.rankDict={
        '1111':'S+',
        '1110':'S',
        '1100':'A',
        '1011':'B+',
        '0111':'B+',
        '1010':'B',
        '0110':'B',
        '1000':'C',
        '0100':'C'
        }
        self.weightDict={'S+':0.9999,'S':0.9999,'A+':0.75,'A':0.75,'B+':0.50,'B':0.50,'C+':0.25,'C':0.25}
        
        self.write_file()
        
    def general_detect(self,dic1,dic2,category):
        overlap={'determine':0}
        #判断两篇文章是否在给定的category中相连，并给予overlap的concept（key），和在两个文件中出现的次数（值），和一个detemine（和concept一样是key）做判断
        if dic1.has_key(category) and dic2.has_key(category):
            for cui in dic1[category]:
                if dic2[category].has_key(cui):
                    overlap[cui]={'semanticType':dic1[category][cui]['semanticType'],'file1_count':dic1[category][cui]['count_concept'],'file2_count':dic2[category][cui]['count_concept']}
                    overlap['determine']=1
        return overlap
    
    def OTC_detect(self,dic1,dic2,category):
        overlap={'determine':0}
        #要判断Organ，tissue和cell是否相连，首先要看是否是同一个物种
        species_overlap=self.general_detect(dic1,dic2,'Material_species')
        if species_overlap['determine']==1:
            if dic1.has_key(category) and dic2.has_key(category):
                for cui in dic1[category]:
                    if dic2[category].has_key(cui):
                        overlap[cui]={'semanticType':dic1[category][cui]['semanticType'],'file1_count':dic1[category][cui]['count_concept'],'file2_count':dic2[category][cui]['count_concept']}
                        overlap['determine']=1
        return overlap

    def decision(self,time1,time2,dic1,dic2):
        #direction=0表示file1后于file2, =1表示file1先于file2
        gene=self.general_detect(dic1,dic2,'Material_gene')
        disease=self.general_detect(dic1,dic2,'Disease_pathologic')
        d1=datetime.datetime(int(time1[:4]),int(time1[4:6]),int(time1[6:]))
        d2=datetime.datetime(int(time2[:4]),int(time2[4:6]),int(time2[6:]))
        month=(d1-d2).days
        if self.direction_choice=='F2L':
        #发表时间早的文献指向发表时间晚的文献
            if int(month)>0:
                direction=0 
            else:
                direction=1
        else:
        #发表时间晚的文献指向发表时间早的文献
            if int(month)>0:
                direction=1 
            else:
                direction=0
        month=abs(float(month)/30)
        #如果基因和疾病有相连的concept，两篇文献的发表时间超过6个月。则认为两篇文献相关
        if gene['determine']==0 and disease['determine']==0:
            connect=0
        elif month<=6:
            connect=0
        else:
            connect=1
        return connect,direction
    
    def concept_overlap(self,dic,category,rank):
        if len(dic)!=1:
            for concept in dic:
                if concept!='determine':
                    rank[category].append(concept)
        return rank
        
    def rank_write(self,dic1,dic2):
        rank={}
        
        gene_overlap=self.general_detect(dic1,dic2,'Material_gene')
        gene=gene_overlap['determine']
        
        disease_overlap=self.general_detect(dic1,dic2,'Disease_pathologic')
        disease=disease_overlap['determine']
        
        species_overlap=self.general_detect(dic1,dic2,'Material_species')
        species=species_overlap['determine']
        
        organ=self.OTC_detect(dic1,dic2,'Material_organ')
        tissue=self.OTC_detect(dic1,dic2,'Material_tissue')
        cell=self.OTC_detect(dic1,dic2,'Material_cell')
        if organ['determine']==1 or tissue['determine']==1 or cell['determine']==1:
            OTC=1
        else:
            OTC=0
            
        string=str(gene)+str(disease)+str(species)+str(OTC)
        rank['linklevel'],rank['resourse']=self.rankDict[string],string
        
        rank['gene'],rank['disease'],rank['species'],rank['OTC']=[],[],[],[]
        rank=self.concept_overlap(gene_overlap,'gene',rank)
        rank=self.concept_overlap(disease_overlap,'disease',rank)
        rank=self.concept_overlap(species_overlap,'species',rank)
        rank=self.concept_overlap(organ,'OTC',rank)
        rank=self.concept_overlap(tissue,'OTC',rank)
        rank=self.concept_overlap(cell,'OTC',rank)
        
        return rank
        
    def write_file(self):
        filelist=sorted(self.ConceptInFile.keys())
        aloneFile=copy.deepcopy(filelist)  #存储的是未与其它节点相连的节点。初始为所有节点，若某两节点相连，则尝试从aloneFile中将其删除。输出在网络文件的最后
        network_write=open(self.network_path,'w')
        network_write.write('#file1\tfile2\trankLevel\tweight_level\tweight_overlap\tgene\tdisease\tspecies\tOTC\n')
        for filename1 in filelist:
            for filename2 in filelist:
                if filename1!=filename2:
                    time_file1,time_file2=self.pubmed_date[filename1],self.pubmed_date[filename2]
                    #direction=0表示file1后于file2, =1表示file1先于file2
                    connect,direction=self.decision(time_file1,time_file2,self.ConceptInFile[filename1],self.ConceptInFile[filename2])
                    #connect会判断两个文献是否相连，而direction还看了两篇文献的时间先后，这里取file1先于file2
                    if connect==1 and direction==1:
                        rank=self.rank_write(self.ConceptInFile[filename1],self.ConceptInFile[filename2])
                        rank['gene']='||'.join(rank['gene'])
                        rank['disease']='||'.join(rank['disease'])
                        rank['species']='||'.join(rank['species'])
                        rank['OTC']='||'.join(rank['OTC'])
                        overlap_concept=rank['gene']+'\t'+rank['disease']+'\t'+rank['species']+'\t'+rank['OTC']
                        weight=self.weightDict[rank['linklevel']]
                        network_write.write('%s\t%s\t%s\t%s\t%s\t%s\n'%(filename1,filename2,rank['linklevel'],weight,'0',overlap_concept))
                        
                        #从aloneFile中删除这两个file
                        for fn in [filename1,filename2]:
                            if fn in aloneFile:
                                aloneFile.remove(fn)
        #将aloneFile中剩下的File写入网络文件
        for fn in aloneFile:
            network_write.write(fn+'\n')
        network_write.close()