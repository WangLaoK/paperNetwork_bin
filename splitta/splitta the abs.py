#coding:utf8
import os
import sys

#python sbd.py -m model_nb -t sample.txt -o sample.sent

for root, dirs, fns in os.walk(r'F:\works\master\project\scripts\paperNetwork\data\test'):
    for fn in fns:
        in_path=os.path.join(root,fn)
        out_path=os.path.join('abs_splitta',fn)
        out_path='test.txt'
        
        cmd = "python sbd.py -m model_nb -t "+in_path+" -o "+out_path
        os.system(cmd)