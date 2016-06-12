# =-= coding:utf-8  =-=

import os,sys,re,yaml


class conceptStat():
    def __init__(self,Metamap_dir,Concerned_Semantic_type_path='..\\knol\\target_semanticType.txt',generalConcepts_path='..\\knol\\generalConcepts.txt',generalStrings_path='..\\knol\\generalStrings.txt'):
        self.Metamap_dir=Metamap_dir
        self.Concerned_Semantic_type=self.get_semanticType(Concerned_Semantic_type_path)
        self.generalConcepts=self.get_generalKnol(generalConcepts_path)
        self.generalStrings=self.get_generalKnol(generalStrings_path)

        self.Filenames=[]   #
        self.File_all_info={}   #根据metamap结果，将所有文件的结果，以文件名为key，存储为字典 
        self.conceptsInFile={}  #以文件名为key，统计每份文件里出现的target_concept,计算次数、semanticType、category等
        self.conceptSummary={}     #以CUI为key，统计每个concept出现的总次数，以及出现过的文档数
        
        self.get_filename()
        self.make_dic() #解析结果，生成File_all_info
        self.count_concept_inFile() #生成self.conceptsInFile
        self.conceptSummary=self.get_concept_detail()   #生成self.conceptSummary
        
    def get_filename(self):
        self.Filenames=os.listdir(self.Metamap_dir)
    
    #得到语义类型的字典
    def get_semanticType(self,Concerned_Semantic_type_path):
        Concerned_Semantic_type={}
        ST_file=open(Concerned_Semantic_type_path,'r')
        ST_data=ST_file.readlines()
        for i in range(0,len(ST_data)):
            line=ST_data[i].strip().split('\t')
            if len(line)==4:
                if not line[0].startswith('#'):
                    Concerned_Semantic_type[line[1]]={'id':line[0],'name':line[1],'parentid':line[2],'category':line[3]}
        ST_file.close()
        return Concerned_Semantic_type
        
    def get_generalKnol(self,knolPath):
        generalConcepts=[]
        
        file=open(knolPath,'r')
        data=file.readlines()
        file.close()
        
        for line in data:
            line=line.strip()
            if line.startswith('#') or len(line)==0:
               continue
            else:
                generalConcepts.append(line)
        return generalConcepts

    def locateConcept(self,line):
        #通过数括号，定位concept的内容范围
        start_pos=line.rfind('[')
        #初始化
        concept_ind1,concept_ind2=line.rfind('('),line.rfind(')')
        if concept_ind1!=-1:
            count=0
            for pos in range(start_pos,0,-1):
                if line[pos]==')' and count==0:
                    concept_ind2=pos
                if line[pos]==')':
                    count+=1
                if line[pos]=='(':
                    start_pos=pos
                    break
            for pos in range(start_pos,0,-1):
                if line[pos]=='(':
                    count+=-1
                if count==0:
                    concept_ind1=pos
                    break
        
        return concept_ind1,concept_ind2
        
    #######  Add category   ############
    def add_category(self,dic1,dic2):
        if dic2.has_key(dic1['term']):
            dic1['category']=dic2[dic1['term']]['category']
        else:
            dic1['category']='NA'
        return dic1
    
    #   Assign every words into dictionary 
    def classify(self,line,dics):
        # Find terms 
        term_ind1,term_ind2=line.find('['),line.rfind(']')
        if term_ind1!=-1:
            dics['term']=line[term_ind1+1:term_ind2]
        # Find concept 
        #concept_ind1,concept_ind2=line.rfind('('),line.rfind(')')
        concept_ind1,concept_ind2=self.locateConcept(line)
        if concept_ind1!=-1:
            dics['concept']=line[concept_ind1+1:concept_ind2]
        # Find CUI    
        CUI_ind1,CUI_ind2=line.find(' ',4)+3,line.find(':')
        if CUI_ind2!=-1:
            dics['CUI']=line[CUI_ind1:CUI_ind2]
        # Find string ,nottice!!! some line didn't get ther concept!!!!
        string_ind=CUI_ind2+1
        if concept_ind1==-1:
            dics['string']=line[string_ind:term_ind1].strip()
        else:
            dics['string']=line[string_ind:concept_ind1].strip()
        return dics
        #   Score can be classified by the split function  
    
    def make_dic(self):
        for filename in self.Filenames:
            #####   Every file makes a new list to store ########
            infile_lists,jump_ind=[],0
            input_filename=os.path.join(self.Metamap_dir,filename)
            input_filename_rawtxt=open(input_filename,'r').readlines()
            for line_no in range(0,len(input_filename_rawtxt)):
                line=input_filename_rawtxt[line_no]
                ########  Store the Sentences  ##############
                if line[:4]=='Proc':
                #########   Find the sentences ,sample like "Processing 00000000.tx.1: Mutations in mitochondrial genes.....",take the ":" index  #############
                    sentences=line[line.find(':')+1:-2]
                    jump_ind=0
                else:
                    ##########   Store  the  Phrases ,sample like Phrase: "Mutations in mitochondrial genes"###########
                    if line[:4]=='Phra':
                        ############    +3,-3 kick the space and quotes    ##########
                        phrase=line[line.find('"')+1:line.rfind('"')]
                        jump_ind=0
                    elif line[5:12]=='Mapping':
                        #########  Find the mapping score,sample like Meta Mapping (783): ##########
                        meta_score=line[line.find('(')+1:line.find(')')]
                        mapping={'sentence':sentences,'phrase':phrase,'meta_score':meta_score,'result':[]}
                        infile_lists.append(mapping)
                        jump_ind=1
                    else:
                        line=line.split()
                        ###########  Skip the blank,only take the line behind the Metamapping      ##############
                        if line!=[] and jump_ind==1:
                            if line[0].isdigit():
                                ############   Use split to store the score,for term & concept,use classify function to assign; Sometimes the concept may not exist,so give a NA  #########
                                sample={'score':line[0],'CUI':'','term':'','concept':''}    #'term' refers to Semantic Type
                                sample=self.classify(input_filename_rawtxt[line_no],sample)
                                sample=self.add_category(sample,self.Concerned_Semantic_type)
                                if sample['string']=="Goes":
                                    print filename
                                    print sentences
                                    print phrase
                                    print input_filename_rawtxt[line_no]
                                    print '==============='
                                infile_lists[len(infile_lists)-1]['result'].append(sample)
            self.File_all_info[filename]=infile_lists
    
    def count_concept_inFile(self):
        for filename in self.File_all_info:
            self.conceptsInFile[filename]={}
            for phrase_index in range(0,len(self.File_all_info[filename])):
                #print phrase_index,self.File_all_info[filename][phrase_index]
                phrase=self.File_all_info[filename][phrase_index]
                for result_index in range(0,len(phrase['result'])):
                    sample=phrase['result'][result_index]
                    #如果concept为空，即metamap中出现“573   C0013546:Ecology [Occupation or Discipline]”的情况，则将string视为concept,即将“Ecology”作为concept
                    if sample['concept']=='':
                        sample['concept']=sample['string']
                    #只要我们关心的catagory
                    if not sample['category']=='NA':
                        #去除generalConcepts和generalStrings, generalStrings添加于2016.4.29
                        if not (sample['concept'] in self.generalConcepts or sample['string'] in self.generalStrings):
                            #目标concept的CUI号，判断是否
                            key_concept=sample['CUI']
                            if self.conceptsInFile[filename].has_key(key_concept):
                                self.conceptsInFile[filename][key_concept]['count']+=1
                                #保留下concept的表达方式string,不保留重复的
                                if not sample['string'] in self.conceptsInFile[filename][key_concept]['string']:
                                    self.conceptsInFile[filename][key_concept]['string'].append(sample['string'])
                            else:
                                self.conceptsInFile[filename][key_concept]={'count':1,'semanticType':sample['term'],'category':sample['category'],'concept':sample['concept'],'string':[sample['string']]}
        
    def get_concept_detail(self):
        conceptSummary={}
        for fileName in self.conceptsInFile:
            for CUI in self.conceptsInFile[fileName]:
                if not conceptSummary.has_key(CUI):
                    conceptSummary[CUI]={'concept':'','count_total':0,'count_document':0,'semanticType':'','category':'','string':[]}
                    conceptSummary[CUI]['concept']=self.conceptsInFile[fileName][CUI]['concept']
                    conceptSummary[CUI]['semanticType']=self.conceptsInFile[fileName][CUI]['semanticType']
                    conceptSummary[CUI]['category']=self.conceptsInFile[fileName][CUI]['category']
                conceptSummary[CUI]['count_document']+=1
                conceptSummary[CUI]['count_total']+=self.conceptsInFile[fileName][CUI]['count']
                conceptSummary[CUI]['string']+=self.conceptsInFile[fileName][CUI]['string']
        for CUI in conceptSummary:
            conceptSummary[CUI]['string']=list(set(conceptSummary[CUI]['string']))
                
        return conceptSummary