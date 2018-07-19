#!/usr/bin/ipython
# -*- coding: utf-8 -*-

# parte do código apresentado neste documento foi inspirado de https://code.google.com/p/criaprova

import random, sys, os, os.path, glob, csv, socket, string, smtplib

import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize # retirar acentuação

# variáveis globais
if os.name == 'nt': # Windows
    barra = '\\'
else:
    barra = '/'

mypath = '.'+barra
mypathQuestions = mypath+'questions'+barra
mypathCourses = mypath+'courses'+barra
mypathConfig = mypath
mypathTex = mypath+'tex'+barra
listextQuestions = ['*.txt']
listextConfig = ['*.txt']
listextCourses = ['*.csv']

def readQuestionsFiles(p):
    fileQuestoes = []
    listdirQuestoes = glob.os.listdir(mypathQuestions)
    listdirQuestoes.append('')
    for ext in listextQuestions:
        for file in np.sort(glob.glob(mypathQuestions+p+barra+ext)):
            fileQuestoes.append(file)
    return fileQuestoes

def readClassFilesConfig(p):
    fileConfigs = []
    for ext in listextConfig:
        for file in np.sort(glob.glob(p+ext)):
            if (file[file.rfind(barra)+1:file.rfind(barra)+7].upper()=="CONFIG"): # pega todos config*.txt
                fileConfigs.append(file)
    return fileConfigs

def classesReadFiles(files):
    print ""
    turmas = []
    for fi in files:
        alunos=[]
        with open(fi, 'rb') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                #print ">>>>", row
                s = normalize('NFKD', row[1].decode('utf-8')).encode('ASCII', 'ignore') # retirar acentos
                alunos.append([fi,row[0],s])
        print "read the class file: %-40s with %d students" % (fi,len(alunos))
        turmas.append(alunos)
    print ""
    return turmas

def getConfigLines(i, AllLines):
    tam = len(AllLines)
    while i < tam and AllLines[i]=='\n' and len(AllLines[i].split('::'))<2: # acha uma variável
        i += 1
    v = AllLines[i].split('::')
    s = []
    v0 = v[0]
    v0 = v0.replace(' ','')
    v0 = v0.replace('\t','')
    ss = v[1]
    ss = ss.lstrip()
    ss = ss.rstrip()
    ss = ss.replace('\t','')
    s.append(ss)
    i += 1
    while i < tam and len(AllLines[i].split('::'))<2:
        ss = AllLines[i]
        ss = ss.lstrip()
        ss = ss.rstrip()
        ss = ss.replace('\t','')
        s.append(ss)
        i += 1
    return (i,v0,'\n'.join([x for x in s]))


def getConfig(file):
    global config, folderQuestions, folderCourse, randomTests, barra, MCTest_sheets, folderQuestions, folderCourse
    global numQE, numQM, numQH, numQT, duplexPrinting, maxQuestQuadro, maxQuadrosHoz, headerByQuestion
    global template

    arq = open(file)
    AllLines = arq.readlines()
    tam = len(AllLines)
    i = 0
    config = dict()
    while i<tam:
        i, v, s = getConfigLines(i, AllLines)
        config[v] = s
        
    numQE = int(config['numQE']) # num. questoes fáceis
    numQM = int(config['numQM']) # num. questoes médias
    numQH = int(config['numQH']) # num. questoes difíceis
    numQT = int(config['numQT']) # num. questoes dissertativas
    folderQuestions = config['folderQuestions'] # pasta com o bd de questões
    folderCourse = config['folderCourse']
    randomTests = int(config['randomTests'])
    MCTest_sheets = int(config['MCTest_sheets'])
    duplexPrinting = int(config['duplexPrinting'])
    template = int(config['template'])
    maxQuestQuadro = int(config['maxQuestQuadro'])
    maxQuadrosHoz = int(config['maxQuadrosHoz'])
    headerByQuestion = int(config['headerByQuestion'])

def main(argv):
    global turmas, gabaritos, randomTests, barra, MCTest_sheets, folderQuestions, folderCourse
    global numQE, numQM, numQH, numQT, duplexPrinting, maxQuestQuadro, maxQuadrosHoz, headerByQuestion
    global config
    
    try:
        if len(sys.argv)==2:
            path = sys.argv[1]
        else:
            path = '/home/fz/Dropbox/PI/PI-Presencial/2018q1/script3MCTest/'

        #print path
        for f in readClassFilesConfig(path):
            #print "####",f
            getConfig(f) # ler as variáveis de configuração e layout
            
            pathPDFs = path+'tex'+barra+folderCourse+barra+folderQuestions+barra+'print'
            #print pathPDFs
            pathClasses = path+'courses'+barra+folderCourse+barra+"*.csv"
            #print pathClasses
            numClasses = len(np.sort(glob.glob(pathClasses)))
            #print numClasses
            if numClasses==0:
                print "run: " + 'ipython validClassesCSV.py '+path+'courses'+barra+folderCourse[:-3]+barra
                os.system('ipython /usr/local/MCTest/validClassesCSV.py '+path+'courses'+barra+folderCourse[:-3]+barra)
                
            runFlag = False
            #print len(np.sort(glob.glob(pathPDFs+barra+"*.pdf")))
            if numClasses != len(np.sort(glob.glob(pathPDFs+barra+"*.pdf"))):
                runFlag = True
            for file in np.sort(glob.glob(pathPDFs+barra+"*.tex")):
                if (not os.path.isfile(file[:-3]+"pdf")):
                    print "ERRO: não existe : ",file[:-3]+"pdf"
                    runFlag = True
                            
            if runFlag:
                print "RUN: " + "ipython " + path + "createTestsROBO.py " + f
                os.system('ipython '+ path + 'createTestsROBO.py '+ f)
                        

    except ValueError:
        print "Oops!  Erro in File:",sys.argv[1], "Try again..."


if __name__ == '__main__':
    main(sys.argv[1:])

