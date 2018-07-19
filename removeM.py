#!/usr/bin/ipython

# -*- coding: utf-8 -*-
import string
#import curses.ascii
import sys
import os

print "remove ^M in :", sys.argv[1]

def convertFileWin2Linux(f):
    #awk '{ sub("\r$", ""); print }' input.txt > output.txt
    os.system(''' awk '{ sub("\\r$", ""); print }' '''+ f+ ' > '+ f[:-4] + '__a__.txt')
    os.system('mv '+ f[:-4] + '__a__.txt ' + f)


convertFileWin2Linux(sys.argv[1])
convertFileWin2Linux(sys.argv[1])
