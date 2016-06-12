# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
from numpy import linalg as la

def HITs(A,X,Y,cutoff=0.000005):
    a={}
    h={}
    ######## a[0] non sense
    a[0]=X
    h[0]=Y
    h[0]=h[0]/la.norm(h[0])
    
    var=1
    i=0
    
    while var>=cutoff:
        i+=1
        a[i]=np.dot(A.T,h[i-1])
        a[i]=a[i]/la.norm(a[i])
        h[i]=np.dot(A,a[i])
        h[i]=h[i]/la.norm(h[i])
        
        var=var=max(max(abs(a[i]-a[i-1])),max(abs(h[i]-h[i-1])))
    
    X=a[i]
    Y=h[i]
        
    return X,Y