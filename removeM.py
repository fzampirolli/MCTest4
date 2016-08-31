# -*- coding: utf-8 -*-
import string
import curses.ascii

arq = open('questions3.txt','r')
arq1 = open('questions3a.txt','w')
AllLines = arq.readlines()

tam = len(AllLines)
i = 0
while i<tam:
    string.replace( AllLines[i][:], '\r', '' )
    arq1.write(AllLines[i][:])
    i=i+1
     
arq1.close()
arq.close()
