#coding:utf-8
from splitta import sbd
import os
import yaml
from getsection import getSection

def main(txt_dir,txt_selected_dir,metamapRe_dir,sub_start='materials and methods',sub_end='acknowledgments',subtitle_knowledge_path='..\\knol\\subtitle.yaml',senSplit=False,outputSubtitleInFile=True):
    
    subtitle_knowledge={}
    subtitleNames=['abstract','introduction','materials and methods','results','discussion','supplementary','acknowledgments','author contributions','funding','references']
    log_subtitleInFile=[]
    log_subtitleInFile.append('filename\t'+'\t'.join(subtitleNames))
    
    #如果知识文件存在，则读取知识文件获得subtitle_knowledge
    if os.path.exists(subtitle_knowledge_path):
        f=open(subtitle_knowledge_path,'r')
        subtitle_knowledge=yaml.load(f)
        f.close()

    #挑选目标正文
    for root,dirs,fns in os.walk(txt_dir):
        for fn in aaa:
            path=os.path.join(root,fn)
            
            #根据目标的subtitle获取目标正文,写入txt_selected_dir
            gs=getSection(path,subtitle_knowledge=subtitle_knowledge,selected_dir=txt_selected_dir,start_subtitle=sub_start,end_subtitle=sub_end)
            string=[fn]
            for sb in subtitleNames:
                line_no=str(gs.subtitle_location[sb])
                string.append(line_no)
            string.append(gs.subtitle_location['finalRange'])
            log_subtitleInFile.append('\t'.join(string))
            
            #如果senSplit为True,则利用splitta进行分句，分句结果为句子构成的list。可自定义应该写入何处
            if senSplit:
                sents=sbd.BinyangUse(path)
    
    #如果outputSubtitleInFile为True，则把每份文档里是否找到各个subtitle输出
    if outputSubtitleInFile:
        log_path='..\\data\\result\\subtitleInFile.txt'
        log=open(log_path,'w')
        log.write('\n'.join(log_subtitleInFile))
        log.close()
    
    #运行metamap
    for root,dirs,fns in os.walk(txt_selected_dir):
        for fn in fns:
            in_path=os.path.join(root,fn)
            pmid=fn.split('.')[0]
            out_path=os.path.join(metamapRe_dir,pmid)
            if not os.path.exists(out_path):
                #cmd = 'C:\\HuBY\\metamap14\\public_mm\\bin\\metamap14 -y --XMLf {input_path} {output_path}'.format(input_path=in_path,output_path=out_path)
                cmd = 'C:\\HuBY\\metamap14\\public_mm\\bin\\metamap14 -y -I {input_path} {output_path}'.format(input_path=in_path,output_path=out_path)
                print cmd
                os.system(cmd)
    
if __name__=='__main__':
    txt_dir='..\\data\\txt_cleaned'
    txt_selected_dir='..\\data\\txt_selected\\metmethod2acknow_merged'
    metamapRe_dir='..\\data\\MetamapRe\\method2acknow_merged'
    
    if not os.path.exists(txt_selected_dir):
        os.mkdir(txt_selected_dir)
    if not os.path.exists(metamapRe_dir):
        os.mkdir(metamapRe_dir)
        
    main(txt_dir,txt_selected_dir,metamapRe_dir,outputSubtitleInFile=False)