# encoding: utf-8
import os

data = open('footballers list.txt','r',encoding='utf-8')
newline = data.readline()
while len(newline)!=0:
    newline = data.readline().strip('/n')
    newline = newline.split('|')
    os.makedirs(newline[2])
    os.replace(newline[0]+'.png',newline[2]+'/1.png')

    
