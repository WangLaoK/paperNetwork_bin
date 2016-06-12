#coding:utf-8
from __future__ import division
import numpy as np

def AddGroundNode(A,S,weight):
    #添加虚拟节点
    n=A.shape[0]
    A_new=np.zeros((n+1,n+1))
    S_new=np.ones((1,n+1))[0]
    
    for i in range(0,n+1):
        for j in range(0,n+1):
            if i<n and j<n:
                A_new[i][j]=A[i][j]
            else:
                A_new[i][j]=weight
    A_new[n][n]=0
    
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
    
def LeaderRank(A,S,weight=1,cutoff=0.00000005):
    score_dict={}
    lr={}   #存储每一轮的打分结果
    A,S=AddGroundNode(A,S,weight)
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
    