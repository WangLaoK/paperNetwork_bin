#coding:utf-8

import os,sys,re,string
import re
import commonFunctions as cf

class noiseFilter():
    def __init__(self,input_path,subtitle_candidate,txt_cleaned_dir,subtitle_knowledge={},peak_dir='..\\data\\peaks\\'):
        
        self.input_path=input_path
        self.subtitle_candidate=subtitle_candidate
        self.subtitle_knowledge=subtitle_knowledge
        self.peak_dir=peak_dir
        self.txt_cleaned_dir=txt_cleaned_dir
        self.filename=input_path.split('\\')[-1]
        
        self.short_cutoff=5
        self.txt_first_cleaned={}
        
        self.checkOutDir()
        #第一步清洁后的字典，行号为key，行为内容
        self.kicklengthlessthan()
        self.cutoff=self.generatePeakFile()
        self.window_filter()
        
    def window_filter(self):
        cutoff=self.cutoff
        #window 删除成片短行
        window_path=os.path.join(self.txt_cleaned_dir,self.filename)
        window_write=open(window_path,'w')
        line_len=0
        for line_no in sorted(self.txt_first_cleaned.keys()):
            shortline,longline=0,0
            line=self.txt_first_cleaned[line_no]
            if line_no+2<=len(self.txt_first_cleaned)-1 and line_no-2>=0:
                for window_no in range(line_no-2,line_no+3):
                    #current_line=self.txt_first_cleaned[window_no]
                    #2016.04.27修改,因为self.txt_first_cleaned存储的是保留下来的原文本，所以计算长度前需要cf.clean
                    current_line=cf.clean(self.txt_first_cleaned[window_no])
                    ##############如果句尾是句号，给他加上一个cutoff的长度
                    if current_line[-1]=='.': 
                        #current_line=re.sub(r'[^a-zA-Z0-9]','',current_line)   marked at 2016.04.27
                        line_len=len(current_line)+cutoff[1]
                    else:
                        ##############把非字符的换成空计算此行的长度
                        #current_line=re.sub(r'[^a-zA-Z0-9]','',current_line)   marked at 2016.04.27
                        line_len=len(current_line)
                    if line_len<cutoff[1]:
                        shortline+=1
                    else:
                        longline+=1
                if longline>shortline:
                    cf.writeToFile(window_write,line)
                else:       
                    #line_clean=line    modified at 2016.04.27
                    line_clean=cf.clean(line)
                                
                    ##########若判断为短行，根据subtitle知识，判断该行是否为subtitle。如果是则保留，开始判断下一行
                    is_subtitle_flag=False
                    for subtitle_name in self.subtitle_knowledge:
                        for pattern in self.subtitle_knowledge[subtitle_name]:
                            line_letter=re.sub('[^a-zA-Z\s]','',line_clean).strip().lower()
                            if line_letter==pattern:
                                cf.writeToFile(window_write,line)
                                is_subtitle_flag=True
                                break
                    if is_subtitle_flag:
                        continue
                
                    ##########若为短行，且不是已经存在的subtitle，若符合subtitle条件则添加进subtitle_candidate中
                    '''
                    subtitle候选的规则
                    1.所有字符数不超过25
                    2.字母数量大于5并且数字小于3个
                    3.句尾不是句号
                    '''
                    letter=self.count_letter(line_clean)
                    digit=self.count_digit(line_clean)
                    if len(line_clean)<=25 and letter>5 and digit<3 and line_clean[-1]!='.':
                        line_letter=re.sub('[^a-zA-Z\s]','',line_clean).strip().lower()
                        if self.subtitle_candidate.has_key(line_letter):
                            self.subtitle_candidate[line_letter]+=1
                        else:
                            self.subtitle_candidate[line_letter]=1
                        #cf.writeToFile(window_write,line)
                    
            else:
                cf.writeToFile(window_write,line)
        window_write.close()
    
    def generatePeakFile(self):
        #找到peak和cutoff,生成peak文件
        line_length_count={}
        ########file_length里把每一行的长度添加进去
        file_length=[]
        ############创造行数和行长度对应关系的字典，行长度为key，行数为值
        for i in sorted(self.txt_first_cleaned.keys()):
            #line_len=len(self.txt_first_cleaned[i])
            #2016.04.27修改,因为self.txt_first_cleaned存储的是保留下来的原文本，所以计算长度前需要cf.clean
            line_len=len(cf.clean(self.txt_first_cleaned[i]))
            if not line_length_count.has_key(line_len):
                line_length_count[line_len]=1
            else:
                line_length_count[line_len]+=1
            file_length.append(line_len)
        if len(file_length)!=0:
            cutoff=self.cuttoff_find(file_length)
        else:
            cutoff=[0,0]
        
        peak_path=os.path.join(self.peak_dir,'peak_'+self.filename)
        peak_write=open(peak_path,'w')
        for line_len in sorted(line_length_count.keys()):
            peak_write.write('%s\t%s\n'%(line_len,line_length_count[line_len]))
        peak_write.close()    
        
        return cutoff
        
    def processSpecialChar(self,raw_txt,specialChar=''):
        new_raw_txt=[]
        for line in raw_txt:
            line=line.split(specialChar)
            new_raw_txt+=line
        return new_raw_txt
    
    def kicklengthlessthan(self):
        #删除短行，初筛
        #非短行规则：1.长度大于self.short_cutoff  2.以“.”结尾，大于2的字符   3.cf.clean()处理后的上一行大于self.short_cutoff，保留，可能出现段尾短行，需要判断上一行。   
        #2016.04.27改动，判断时使用line_cleaned，如果判断需要保留，则保留原始文本
        txt_notclean=open(self.input_path,'r')
        raw_txt=txt_notclean.readlines()
        raw_txt=self.processSpecialChar(raw_txt,'')
        line_no=0
        
        ########k是他原先的行号
        for k in range(0,len(raw_txt)):
            line=cf.changeCode2Ascii(raw_txt[k]).strip() 
            line_clean=cf.clean(line)
            if line_clean:
                if (len(line_clean))>self.short_cutoff :
                    self.txt_first_cleaned[line_no]=line
                    line_no+=1
                elif line_clean[-1]=='.' and len(line_clean)>2:
                    self.txt_first_cleaned[line_no]=line
                    line_no+=1
                elif (len(cf.clean(raw_txt[k-1]).strip()))>self.short_cutoff:
                    self.txt_first_cleaned[line_no]=line
                    line_no+=1
        txt_notclean.close()

    def peak_find(self,line_perWindow):
        max_peak_index=0
        while(max_peak_index<=10):
            if line_perWindow.has_key(max_peak_index):
                del line_perWindow[max_peak_index]
            sorted_items=sorted(line_perWindow.iteritems(),key=lambda d:d[1],reverse=True)
            max_peak=sorted_items[0][1]
            max_peak_index=sorted_items[0][0]
        return max_peak_index 
    
    def cuttoff_find(self,line_length_list,window_len=5):
        #line_perWindow存储的是每个window中的行数，以window的右边界为key
        line_perWindow={}
        window_num=max(line_length_list)/window_len+1
        for i in range(0,window_num):
            #计算window的左右边界，且以其右边界为键
            window_start=window_len*i
            window_end=window_len*i+window_len
            
            if not line_perWindow.has_key(window_end):
                line_perWindow[window_end]=0
            for length in line_length_list:
                if length>window_start and length<=window_end:
                    line_perWindow[window_end]+=1
                    
        max_peak_index=self.peak_find(line_perWindow)
        last_5=0
        #根据peak的数值，获得第一个cutoff候选
        cutoff=[max_peak_index*3/5]
        #根据peak的分布，获得第二个cutoff候选
        for key in sorted(line_perWindow.keys(),reverse=True):
            if key<=max_peak_index:
                if line_perWindow[key]<last_5 or last_5==0:
                    last_5=line_perWindow[key]
                else:
                    if 2*line_perWindow[key]<line_perWindow[max_peak_index]:
                        cutoff.append(key)
                        break
                    else:
                        last_5=line_perWindow[key]
                    
        if len(cutoff)==1:
            cutoff.append(cutoff[0]*3/5)
        return cutoff   
            
    def count_letter(self,line):
        line=line.lower()
        letter_count=0
        for i in [chr(x) for x in range(97,123)]:
            letter_count+=line.count(i)
        return letter_count
        
    def count_digit(self,line):
        line=line.lower()
        digit_count=0
        for i in range(10):
            digit_count+=line.count(str(i))
        return digit_count
    
    def checkOutDir(self):
        if not os.path.exists(self.peak_dir):
            os.mkdir(self.peak_dir)
        if not os.path.exists(self.txt_cleaned_dir):
            os.mkdir(self.txt_cleaned_dir)
            