#coding:utf-8

import os,sys,re,string
import yaml
import re
import commonFunctions as cf

class getSection():
    def __init__(self,input_path,subtitle_knowledge={},selected_dir='..\\data\\txt_selected\\',start_subtitle='introduction',end_subtitle='acknowledgments'):
        
        self.input_path=input_path 
        self.subtitle_knowledge=subtitle_knowledge
        self.start_subtitle=start_subtitle
        self.end_subtitle=end_subtitle
        self.filename=input_path.split('\\')[-1]
        self.selected_dir=selected_dir
        self.subtitle_order=['abstract','introduction','materials and methods','results','discussion','supplementary','acknowledgments','author contributions','funding','references']
        
        #建议原始文档的原文，存入list，不希望这个被改动
        self.original_file_list=open(input_path,'r').readlines()
        #建立一个和subtitle_knowledge键一样的字典，值变为该篇文章subtitle所在行
        self.subtitle_location={}
        for subtitle_name in self.subtitle_knowledge:
            self.subtitle_location[subtitle_name]=[]
            
        self.determine_subtitle()
        self.postProcess()
        self.file_cut()

    def postProcess(self):
        for subtitle in ['abstract','introduction','materials and methods','results','discussion']:
            if self.subtitle_location[subtitle]==[]:
                self.subtitle_location[subtitle]=None
            else:
                self.subtitle_location[subtitle]=min(self.subtitle_location[subtitle])
        for subtitle in ['supplementary','acknowledgments','author contributions','funding','references']:
            if self.subtitle_location[subtitle]==[]:
                self.subtitle_location[subtitle]=None
            else:
                self.subtitle_location[subtitle]=max(self.subtitle_location[subtitle])
    
    #若一行的末尾是‘-’,则将下一行拼上来
    def mergeLines(self,line_list):
        lines_new=[]
        i=0
        while i<len(line_list)-1:
            line=line_list[i].strip()
            if line.endswith('-'):
                line=line[:-1]+line_list[i+1].strip()
                i+=1
            lines_new.append(line+'\n') #\n是为了于原结构保持一致
            i+=1
        if i==len(line_list)-1:
            lines_new.append(line_list[i]+'\n')
        return lines_new
        
    def determine_subtitle(self):
        #遍历每个subtitle的candidate，找到符合的subtitle后输入相应行数。
        
        #通过全行匹配subtitle
        for line_no in range(0,len(self.original_file_list)):
            line=self.original_file_list[line_no].strip()
            #把那些subtitle中的数字点杠下划线清洁掉
            line=cf.clean(line)
            line=re.sub('[^a-zA-Z\s]','',line).strip().lower()
            for subtitle_name in self.subtitle_knowledge:
                for candidate in self.subtitle_knowledge[subtitle_name]:
                    if line==candidate:
                        self.subtitle_location[subtitle_name].append(line_no)
                        
        #通过行首匹配
        for line_no in range(0,len(self.original_file_list)):
            line=self.original_file_list[line_no].strip()
            #把那些subtitle中的数字点杠下划线清洁掉
            line=cf.clean(line)
            line=re.sub('[^a-zA-Z\s]','',line).strip()
            for subtitle_name in self.subtitle_knowledge:
                if self.subtitle_location[subtitle_name]==[]:
                    for candidate in self.subtitle_knowledge[subtitle_name]:
                        pattern=re.compile('^'+candidate+'\W')
                        if pattern.findall(line.lower()) and line[0].isupper():
                            self.subtitle_location[subtitle_name].append(line_no)
    
    def getPreviousSectionStart(self,subtitle):
        previous_location=None
        #index=self.subtitle_order.index(self.start_subtitle)
        index=self.subtitle_order.index(subtitle)
        while (index>=1):
            index=index-1
            previous_subtitle=self.subtitle_order[index]
            previous_location=self.subtitle_location[previous_subtitle]
            if previous_location!=None:
                break
        return previous_location
        
    def getLaterSectionStart(self,subtitle):
        later_location=None
        index=self.subtitle_order.index(subtitle)
        while (index<len(self.subtitle_order)-1):
            index=index+1
            later_subtitle=self.subtitle_order[index]
            later_location=self.subtitle_location[later_subtitle]
            if later_location!=None:
                break
        return later_location
    
    def file_cut(self):
        #根据给予的开始和结束的subtitle，找到相应开始和结束的行数
        
        #如果目标start subtitle未找到
        if self.subtitle_location[self.start_subtitle]==None:
            previous_location=self.getPreviousSectionStart(self.start_subtitle)
            if previous_location==None:
                start_line=0
            else:
                start_line=previous_location
        else:
            #找到了目标start subtitle，但其行号比order中的下一个subtitle还大，则往前取subtitle
            next_subtitle_line=self.getLaterSectionStart(self.start_subtitle)
            if next_subtitle_line!=None and self.subtitle_location[self.start_subtitle]>next_subtitle_line:
                #start_line=next_subtitle_line
                previous_location=self.getPreviousSectionStart(self.start_subtitle)
                if previous_location==None:
                    start_line=0
                else:
                    start_line=previous_location
            else:
                start_line=self.subtitle_location[self.start_subtitle]
        
        #需找end subtitle的开始行
        if self.subtitle_location[self.end_subtitle]==None:
            later_location=self.getLaterSectionStart(self.end_subtitle)
            if later_location==None:
                end_line=len(self.original_file_list)
            else:
                end_line=later_location
        else:
            end_line=self.subtitle_location[self.end_subtitle]
            
        #若end_line比references还后，取references的位置作为end_line
        if self.subtitle_location['references']!=None:
            if end_line>self.subtitle_location['references']:
                end_line=self.subtitle_location['references']
        
        if start_line>=end_line:
            print '[WARNING]section start line bigger than end line: '+self.input_path
            start_line=0            
        self.subtitle_location['finalRange']=str(start_line)+'-'+str(end_line)
        
        selected_content=self.original_file_list[start_line:end_line]
        selected_content=self.mergeLines(selected_content)
        #######end的subtitle是不要的，所以不加1
        selected_path=os.path.join(self.selected_dir,self.filename)
        selected_file_write=open(selected_path,'w')
        for line in selected_content:
            selected_file_write.write(line)
        selected_file_write.close()    