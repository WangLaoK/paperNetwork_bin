#coding:utf-8
#improved LeaderRank

from __future__ import division
import numpy as np

def getInDegree(A,index):
    #获取一个节点在邻接矩阵A中的入度
    n=A.shape[0]
    k_in=0
    for i in range(0,n):
        k_in+=A[i][index]
    return k_in

def AddGroundNode(A,S,alpha,weight):
    #添加虚拟节点
    n=A.shape[0]
    A_new=np.zeros((n+1,n+1))
    S_new=np.ones((1,n+1))[0]
    
    #将原有的点之间的边加入到新的邻接矩阵
    for i in range(0,n):
        for j in range(0,n):
            A_new[i][j]=A[i][j]
    #将虚拟节点与原有节点的边，加入到邻接矩阵
    #构建虚拟节点到原节点的边
    for i in range(0,n):
        k_in=getInDegree(A,i)
        calculated_weight=k_in**alpha
        A_new[n][i]=calculated_weight
    #构建原节点到虚拟节点的边
    for i in range(0,n):
        A_new[i][n]=weight
    
    A_new[n][n]=0   #虚拟节点与自己的边，为0
    
    S_new[n]=0
    return A_new,S_new
    
def buildKout(A):
    k=[]
    n=A.shape[0]
    for i in range(0,n):
        row=list(A[i])
        out=sum(row)
        k.append((1/out))
    K=np.diag(k)
    return K
    
def returnScore(S):
    #将虚拟节点的分数返回给所有节点
    S_new=np.zeros((1,S.shape[0]-1))[0]
    for i in range(0,S.shape[0]-1):
        S_new[i]=S[i]+S[S.shape[0]-1]/(S.shape[0]-1)

    return S_new
    
def LeaderRank(A,S,cutoff=0.00000005,alpha=0,weight=1):
    score_dict={}
    lr={}   #存储每一轮的打分结果
    A,S=AddGroundNode(A,S,alpha,weight)
    K=buildKout(A)
    lr[0]=S
    
    var=1
    i=0
    
    while var>=cutoff:
        i+=1
        tmp=np.dot(A.T,K)
        lr[i]=np.dot(tmp,lr[i-1])
        var=max(abs(lr[i]-lr[i-1]))
        
    S=returnScore(lr[i])
    return S    
    