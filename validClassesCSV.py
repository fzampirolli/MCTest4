# -*- coding: utf-8 -*-

# Sintaxe:
# ipython validClassesCSV ./folder/

import random, sys, os, os.path, glob, csv, socket, string, smtplib

import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize # retirar acentuação


if os.name == 'nt': # Windows
    barra = '\\'
else:
    barra = '/'


mypath = '.'+barra



EXT_CSV = ['CSV']
fileQuestoes = []

def verifyCSVfile(p,f):
    f = p + f
    filename, file_extension = os.path.splitext(f)
    if (file_extension[1:].upper() in EXT_CSV):
        fileQuestoes.append(f)

def findCSVfiles(p):
    listdir = glob.os.listdir(p)
    for dir in listdir:
        if os.path.isdir(p+dir): # se for dir, chamada recursiva
            findCSVfiles(p+dir+'/')
        elif os.path.exists(p+dir):
            verifyCSVfile(p,dir)

def readQuestionsFiles(p):
    listdirQuestoes = glob.os.listdir(p)
    findCSVfiles(p+barra)
    return np.sort(fileQuestoes)

import re

def classesReadFiles(file):
    alunos = []
    with open(file, 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            
            try:
                nome = normalize('NFKD', row[1].decode('utf-8')).encode('ASCII', 'ignore') # retirar acentos
            except ValueError:
                print "ERRO:", file, row

            nome = nome[:40]

            ra = row[0]
            ra = ra[:11]
            ra = re.sub(u"[a-zA-Z]","0",ra)
            ra = re.sub('[ ,_?./;:!@#$+*]', '', ra)
            ra = ra.replace('\'','')
            ra = ra.replace('-','')
            try:
                int(ra)
            except ValueError:
                print "ERRO: RA não é número!!! - " , file, ra, nome
            alunos.append([ra,nome])
        print "read file: %-40s with %d students" % (file,len(alunos))
    return alunos
        
def writeCSVFiles(mypath,f,turma):
    path = mypath[:-1] + "_OK"
    fout = path + barra + f.split(barra)[-1]
    try:
        os.stat(path)
    except:
        os.mkdir(path)
    
    with open(fout, 'w') as csvfile:
        spamWriter = csv.writer(csvfile, delimiter=';',quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for row in turma:
            spamWriter.writerow(row)

def main():
    global barra
    try:
        if len(sys.argv)==2:
            mypath = sys.argv[1]
            
            for f in readQuestionsFiles(mypath):
                alunos = classesReadFiles(f)
                writeCSVFiles(mypath,f,alunos)

    except ValueError:
        print "Oops!  Erro in File:",sys.argv[1], "Try again..."


if __name__ == '__main__':
    main()
