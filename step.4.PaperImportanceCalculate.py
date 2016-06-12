#coding:utf-8

import os
import numpy as np
import LeaderRank
import LeaderRank_weight
import HITs

def getNodeList(network):
    node_list=[]
    
    for line in network:
        line=line.strip()
        if (not line.startswith('#')) and len(line)!=0:
            line=line.split('\t')
            if len(line)>=2:
                node1=line[0]
                node2=line[1]
                node_list.append(node1)
                node_list.append(node2)
            elif len(line)==1:
                node1=line[0]
                node_list.append(node1)
    node_list=list(set(node_list))
    node_list.sort()
    
    return node_list

def generateMatrix(network,node_list,method='binary'):  #method可以为binary, level, overlap 三种,返回不同的权重值
    num_nodes=len(node_list)
    M=np.zeros((num_nodes,num_nodes))
    for line in network:
        if (not line.startswith('#')) and len(line)!=0:
            line=line.split('\t')
            if len(line)>=2:
                node1=line[0]
                node2=line[1]
                rankLevel=line[2]
                weight_level=line[3]
                weight_overlap=line[4]
                #定位应该找到的位置i,j。i为行号，j为列号
                i=node_list.index(node1)
                j=node_list.index(node2)
                
                weight=0
                #根据method确定选取哪种权重
                if method=='binary':
                    weight=1
                elif method=='level':
                    weight=float(weight_level)
                elif method=='overlap':
                    weight=float(weight_overlap)
                    
                #将weight填入矩阵
                if i!=j:
                    M[i][j]=weight

    return M
    
def output_score(score_dict,outpath):
    #score_dict统一结构：{filename:{key1:score1,key2:score2,....}}
    outfile=open(outpath,'w')    
    score_keys=score_dict[score_dict.keys()[0]].keys()
    #写文件头
    outfile.write('#filename\t'+'\t'.join(score_keys)+'\n')
    #写内容
    for filename in score_dict:
        content=[filename]
        for key in score_keys:
            score=score_dict[filename][key]
            content.append(str(score))
        outfile.write('\t'.join(content)+'\n')
    outfile.close()

def main(network_file_path,outDir):
    network_file=open(network_file_path,'r')
    network=network_file.readlines()
    network_file.close()

    score_HITs={}
    score_LR={}
    node_list=getNodeList(network)
        
    #解析network，获得邻接矩阵A和权重矩阵W
    #A=generateMatrix(network,node_list,method='binary')
    W=generateMatrix(network,node_list,method='level')
    
    #利用HITs算法计算节点重要性
    X=np.array([0]*len(node_list)) #初始化权威值,authority
    Y=np.array([1]*len(node_list)) #初始化枢纽值,hubs
    X,Y=HITs.HITs(W,X,Y)
    
    #利用LeaderRank算法计算节点重要性
    S=np.ones((0.005,len(node_list)))    #初始化
    S=LeaderRank_weight.LeaderRank(W,S)
    
    for i in range(0,len(node_list)):
        node=node_list[i]
        score_HITs[node]={'Authority':X[i],'Hubs':Y[i]}
        score_LR[node]={'LR_score':S[i]}
        
    
    #输出两者结果到文件
    outpath_HITs=os.path.join(outDir,'score_HITs.txt')
    outpath_LR=os.path.join(outDir,'score_LR.txt')
    output_score(score_HITs,outpath_HITs)
    output_score(score_LR,outpath_LR)
    
if __name__=='__main__':
    outDir='..\\data\\result\\method2acknow_merged'
    network_file_path=os.path.join(outDir,'Network_file.txt')
    
    main(network_file_path,outDir)