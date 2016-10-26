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
mypathTex = mypath+'tex'+barra
listextQuestions = ['*.txt']
listextCourses = ['*.csv']


letras_1 = ['A','B','C','D','E','F','G','H','I','J', 'K','L', 'M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def getQuestion(i, AllLines):
    tam = len(AllLines)
    while i < tam and AllLines[i][:3] not in ['QT:','QE:','QM:','QH:']: # acha uma questão
        i += 1
    #if i == tam: return(i,' ') # não achou questão
    tp = AllLines[i][:3]
    q = []
    q.append(AllLines[i])
    i += 1
    while i < tam and AllLines[i][:AllLines[i].find(':')] not in ['QT','QE','QM','QH','A']:
        q.append(AllLines[i])
        i += 1
    if i<=tam and tp == 'QT:': # questao do tipo texto
        return (i,' '.join([x for x in q]))
    if i<tam and tp in ['QE:','QM:','QH:'] and AllLines[i][:2] in ['QT','QE:','QM:','QH:']:
        print 'ERRO: questão sem alternativas'
    return (i,' '.join([x for x in q]))


def getAnswer(i, AllLines):
    tam = len(AllLines)
    while i < tam and AllLines[i][:2] not in ['A:']: # acha uma questão
        i += 1
    #if i == tam: return(i,' ') # não achou questão
    q = []
    q.append(AllLines[i])
    i += 1
    while i < tam and AllLines[i][:AllLines[i].find(':')] not in ['QT','QE','QM','QH','A']:
        q.append(AllLines[i])
        i += 1
    return (i,' '.join([x for x in q]))


def questionsReadFiles(arquivos):
    # estados possiveis: fora de alguma questao
    #                    dentro de uma questao - 'QT','QE','QM','QH' - pergunta
    #                    dentro de uma questao - A - respostas
    # as questões são dos tipos QT (somente texto), QE (fácil), QM (média) ou QH (difícil)
    # podendo ter subtipos, por exemplo, se tiver 5 questões, QE:a:, será escolhido de forma
    # aleatória, somente uma questão do subtipo "a".
    # As questões QT, contendo apenas textos, serão inseridas no final do tex.

    listao = []
    respostas = []
    d = dict()
    arqnum = 0
    questnum = 0
    questtotal = 0
    questions_file = 0
    
    for a in arquivos: # para cada arquivo de questões
        
        arq = open(a)
        AllLines = arq.readlines()

        tam = len(AllLines)
        i = 0
        while i<tam:
            i, q = getQuestion(i, AllLines)
            
            d = dict()
            
            d["t"] = ''
            vet = q.split('::')
            if len(vet)==2: #somente tipo
                d["t"] = vet[0]  # tipo QT, QE, QM ou QH
                d["q"] = vet[1].strip()
                d["c"] = ''
                d["st"] = ''
            elif len(vet)==3: # com conteúdo abordado da questão
                d["t"] = vet[0]
                s = normalize('NFKD', vet[1].decode('utf-8')).encode('ASCII', 'ignore') # retirar acentos
                d["c"] = s
                d["q"] = vet[2].strip()
                d["st"] = ''
            elif len(vet)==4: # subtipo da questão, um caracter qualquer
                d["t"] = vet[0]  # tipo QT, QE, QM ou QH
                s = normalize('NFKD', vet[1].decode('utf-8')).encode('ASCII', 'ignore') # retirar acentos
                d["c"] = s
                d["st"] = vet[2]
                d["q"] = vet[3].strip()
            
            d["n"] = questnum
            d["arq"] = arqnum
            
            respostas = []
            if d["t"] != "QT":
                contRespostas = 0
                while i < tam and AllLines[i][:AllLines[i].find(':')] in ['A']:
                    i, r = getAnswer(i,AllLines)
                    #if i == tam: break # não achou questão
                    respostas.append(r[2:].strip())
                    contRespostas +=  1
                
                if contRespostas==0:
                    print 'ERRO: questão sem respostas'
                    sys.exit(-1)
                
            d["a"] = respostas
                        
            listao.append(d)
            questnum += 1

        arq.close()
        arqnum += 1
        print "read the questions file: %-40s with %d questions" % (a,len(listao) - questions_file)
        questions_file = len(listao)
        
    print "\nTotal of questions without suptype:"    
    print "Easy questions QE: %d" % (len([y for y in listao if y['t'] == 'QE' and y['st']=='']))
    print "Mean questions QM: %d" % (len([y for y in listao if y['t'] == 'QM' and y['st']=='']))
    print "Hard questions QH: %d" % (len([y for y in listao if y['t'] == 'QH' and y['st']=='']))
    print "Text questions QT: %d" % (len([y for y in listao if y['t'] == 'QT' and y['st']=='']))

    print "\nTotal of questions with suptype:"    
    print "Easy questions QE: %d" % (len([y for y in listao if y['t'] == 'QE' and y['st']!='']))
    print "Mean questions QM: %d" % (len([y for y in listao if y['t'] == 'QM' and y['st']!='']))
    print "Hard questions QH: %d" % (len([y for y in listao if y['t'] == 'QH' and y['st']!='']))
    print "Text questions QT: %d" % (len([y for y in listao if y['t'] == 'QT' and y['st']!='']))
    
    return listao

def createListTypes(listao,tipo,numQ):
    questTipo = [y for y in listao if y['t'] == tipo and y['st']==''] # pega todas as questões SEM subtipo
    
    st =  [(y['st'],y['n']) for y in listao if y['t'] == tipo and y['st']!=''] # pega COM subtipos
    if st:
        stSet = list(set([i[0] for i in st])) # retira elementos repetidos
        for i in stSet: # para cada subtipo, pego apenas UMA questão aleatoriamente
            li =  [(y['st'],y['n']) for y in listao if y['t'] == tipo and y['st']==i]
            escolhoUM = random.sample(li,1)
            ques  = [y for y in listao if y['n'] == escolhoUM[0][1]]
            questTipo.append(ques[0])

    if numQ > len(questTipo):
        print "number of available questions %s: \t %-5d" % (tipo, len(questTipo))
        print "\nERRO: number of solicitous questions is incompatible with the number of available questions\n"
        sys.exit(-1)
    
    return questTipo


def createTests(listao, turmas):
    """ se a variável randomTests==0:
        significa que não serão geradas provas aleatórias, ou seja, esta função vai pegar
        as primeiras questões fáceis, médias e difíceis e não vai embaralhar as respostas;
        caberá ao professor gerar um arquivo *_GAB, fornecendo as soluções de cada questão
        
        se a variável randomTests!=0:
        cada prova eh gerada aleatoriamente a partir da lista de tuplas com todas as questoes.
        recebe como argumentos: uma listao de tuplas (q,a), o num de provas a serem geradas e
        quantas questoes cada prova deve ter.
        retorna as provas embaralhas; as provas sao listas de tuplas (q,a,n,arq)
        considerando que toda resposta correta esta na opcao A, posicão 0, esta funcao retorna
        tambem gabaritos, com as posições onde ficam a opção A após o embaralhamento, de cada
        questão e de cada prova
        
        gabaritos = [Turma, matricula, gab, conteudos]
        provas    = [Turma, matricula, nome, questoes])
        
        código adaptado de https://code.google.com/p/criaprova/downloads/list
        """
    
    provas = []
    questaoporprova = numQE + numQM + numQH + numQT
    gabaritos = []

    countTurma = 0
    for t in turmas: # para cada turma
        
        for n in t: # para cada aluno da turma
            questoes = []
            
            questQE = createListTypes(listao,'QE',numQE) # tem que ficar aqui para pegar para cada aluno
            questQM = createListTypes(listao,'QM',numQM) # uma questão aleatória de uma subclasse
            questQH = createListTypes(listao,'QH',numQH) # caso exista
            questQT = createListTypes(listao,'QT',numQT)
        
            if int(randomTests)!=0: #questões aleatórias
                quest = random.sample(questQE,numQE)
                quest.extend(random.sample(questQM,numQM))
                quest.extend(random.sample(questQH,numQH))
                quest.extend(random.sample(questQT,numQT))
            else: #questões sequenciais, com as primeiras questões fáceis, médias e difíceis
                quest = questQE[:numQE]
                quest.extend(questQM[:numQM])
                quest.extend(questQH[:numQM])
                quest.extend(questQT[:numQT])
            
            indexQuest = []
            for q in quest:
                indexQuest.append(listao.index(q))
            
            c =  [y['c'] for y in listao if y['c']!=''] # pega questões COM conteúdo(s)
            cSet = []
            if c:
                for i in c:
                    for j in i.split(' - '): # retira questão com mais de um conteúdo
                        cSet.append(j)
        
            conteudo = [] # cria uma lista de conteúdos
            if len(cSet):
                cSet = sorted(list(set(cSet))) # retira conteúdos repetidos
                for i in cSet:
                    conteudo.append([i,[]])
            
            sequencia = []
            gab = []
            contQuest = 0
            for q in quest:
                perg = q['q']
                contQuest += 1
                
                if q['c']: # questão tem conteúdo(s)
                    ii=0
                    for i in conteudo:
                        #print ">>>",i[0],q['c']
                        for j in q['c'].split(' - '):
                            if i[0] == j:
                                #print ">",i[0],j
                                conteudo[ii][1].extend([contQuest])
                        ii += 1
                
                embaralhaResps = []
                g = []
                if q["t"] != 'QT': # não é uma questão dissertativa, embaralha respostas
                    if int(randomTests)!=0: #questões aleatórias
                        embaralhaResps = random.sample(q['a'],len(q['a']))
                    else:
                        embaralhaResps = q['a'][:len(q['a'])]

                    g = embaralhaResps.index(q['a'][0])
                    gab.append(g)

                sequencia.append((perg,embaralhaResps,q['n'],q['arq'],g))
                if q['t'] != 'QNI':
                    pass

            questoes.extend(sequencia)
        
            if len(questoes) < questaoporprova:
                print "\n\n Prova %d com menos questoes do que o solicitado; algum arquivo contem poucas questoes!" % (n)

            if int(randomTests)!=0: #questões aleatórias, então salva gabarito
                gabaritos.append([n[0], n[1], gab, indexQuest, conteudo])

            provas.append([n[0], n[1], n[2], questoes])
        
        countTurma = countTurma + 1

    return provas, gabaritos

def readQuestionsFiles(p):
    fileQuestoes = []
    listdirQuestoes = glob.os.listdir(mypathQuestions)
    listdirQuestoes.append('')
    for ext in listextQuestions:
        for file in np.sort(glob.glob(mypathQuestions+p+barra+ext)):
            fileQuestoes.append(file)
    return fileQuestoes

def readClassFiles(p):
    fileTurmas = []
    listdirTurmas = glob.os.listdir(mypathCourses)
    listdirTurmas.append('')
    for ext in listextCourses:
        for file in np.sort(glob.glob(mypathCourses+p+barra+ext)):
            fileTurmas.append(file)
    return fileTurmas

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

def savesTemplates(gabaritos): # salva em disco todos os gabaritos num arquivo csv por turma
    print ""

    if randomTests==0: #questões não aleatórias
        print "Warning: You chose in config.txt the option to generate non-random tests."
        print "In this case, if you want to use the automatic correction using MCTest,"
        print "you must provide a file with the template or consider that the first test"
        print "in pdf file is a template."
    
    else:

        files = []
        for g in gabaritos:
            files.append(g[0])
    
        for ff in sorted(set(files)):

            f = ff[:-4]+'__seuEmail@dominio.com_GAB'

            past = f[10:]
            filename = past[past.find(barra):]
            past = mypathTex+barra+past[:past.find(barra)]
            try:
                os.stat(past)
            except:
                os.mkdir(past)
            
            past += barra+folderQuestions
            try:
                os.stat(past)
            except:
                os.mkdir(past)

            f = past+filename
            
            print "aquivo salvo com os gabaritos da cada aluno da turma:",f

            #[n[0], n[1], gab, indexQuest, conteudo]
            with open(f, 'w') as csvfile:
                for gab in gabaritos:
                    if ff is gab[0]:
                        spamWriter = csv.writer(csvfile, delimiter=' ',quotechar=' ', quoting=csv.QUOTE_MINIMAL)
                        pathFile = gab[0]
                        if os.name=='nt': #windows
                            pathFile = pathFile.replace(barra,'/')
                        s = ''.join([x for x in str(gab[2])] )
                        s = s.strip('[')
                        s = s.strip(']')
                        s = s.replace(' ','')
                        s = s.strip()
                        
                        i = ''.join([x for x in str(gab[3])] )
                        i = i.strip('[')
                        i = i.strip(']')
                        i = i.replace(' ','')
                        i = i.strip()
                        
                        t = ''.join([x for x in str(gab[4])] )
                        
                        spamWriter.writerow([pathFile, ';',  gab[1],';', s, ';', i, ';',t])

def defineHeader(arqprova,strTurma,idAluno,nomeAluno): # define o cabeçalho de cada página
    global instrucoes

    if config['language'].replace('\n','')=='portuguese':
        turma = "\\textbf{Turma:} %s\n" %  strTurma
        idAluno = "\\textbf{Matrícula:} %s\n" %  str(idAluno)
        nomeAluno="\\textbf{Aluno:} %s\n" % nomeAluno
        strAluno = "\\noindent"+nomeAluno+"\\hfill"+idAluno+"\\hfill"+turma+"\\hspace{-1mm}\n"
        ass = "\\noindent\\textbf{Ass:}\\rule{11.5cm}{0.1pt}\\hfill\\hspace{1cm}\n"
        instrucoes = "Instru\\c c\\~oes: "
        course = "Disciplina:"
        teachers = "Professor(es):"
        period = "Quadrimestre:"
        modality = "Modalidade:"
        date = "Data:"

    if config['language'].replace('\n','')=='english':
        turma = "\\textbf{Room:} %s\n" %  strTurma
        idAluno = "\\textbf{Registration:} %s\n" %  str(idAluno)
        nomeAluno="\\textbf{Student:} %s\n" % nomeAluno
        strAluno = "\\noindent"+nomeAluno+"\\hfill"+idAluno+"\\hfill"+turma+"\\hspace{-1mm}\n"
        ass = "\\noindent\\textbf{Sig.:}\\rule{11.5cm}{0.1pt}\\hfill\\hspace{1cm}\n"
        instrucoes = "Instructions: "
        course = "Course:"
        teachers = "Teacher(s):"
        period = "Period:"
        modality = "Modality:"
        date = "Date:"

    arqprova.write("")
    if duplexPrinting!=0:
        arqprova.write("\\makeatletter\\renewcommand*\\cleardoublepage{\\ifodd\\c@page \\else\\hbox{}\\newpage\\fi}\n")
        arqprova.write("\\makeatother\n")
        arqprova.write("\\cleardoublepage\n")
    
    # header da página 1/2
    arqprova.write("\\begin{table}[h]\\centering\n")
    arqprova.write("\\begin{tabular}{|p{16mm}|p{16cm}|}\n\hline")
    arqprova.write("\multirow{4}{*}{\\hspace{-2mm}\\includegraphics[width=2cm]{../../../figs/"+config['logo'].replace('\n','')+"}}\n")
    arqprova.write("&\\vspace{-2mm}\\noindent\\large\\textbf{"+config['title'].decode('utf-8').encode("latin1")+"}\\\\\n")
    arqprova.write("&\\noindent\\textbf{"+course+"} "+config['course'].decode('utf-8').encode("latin1")+"\\\\\n")
    arqprova.write("&\\noindent\\textbf{"+teachers+"} "+config['teachers'].decode('utf-8').encode("latin1")+"\\\\\n")
    arqprova.write("&\\noindent\\textbf{"+period+"} "+config['period']+"\\hfill")
    arqprova.write("\\textbf{"+modality+"} "+config['modality']+"\\hfill")
    arqprova.write("\\textbf{"+date+"} "+config['date']+"\\hspace{-8mm}\\\\\n\hline")
    arqprova.write("\\end{tabular}\n")
    arqprova.write("\\end{table}\n")
    arqprova.write("\\vspace{-4mm}\\small{\n"+strAluno.decode('utf-8').encode("latin1"))
    arqprova.write("\n\\vspace{8mm}\n")
    arqprova.write(ass.decode('utf-8').encode("latin1"))
    arqprova.write("}")


def createTexTests(provas): # salva em disco todos os testes em arquivos .tex
    preambulo1 = """
        \documentclass[10pt,brazil,a4paper]{exam}
        \usepackage[latin1]{inputenc}
        \usepackage[portuguese]{babel}
        \usepackage[dvips]{graphicx}
        %\usepackage{multicol}
        %\usepackage{shadow}
        %\usepackage{pifont}
        %\usepackage{listings}
        %\usepackage{fancyvrb}
        
        \\newcommand*\\varhrulefill[1][0.4pt]{\\leavevmode\\leaders\\hrule height#1\\hfill\\kern0pt}
        
        \\def\\drawLines#1{{\\color{cyan}\\foreach \\x in {1,...,#1}{\\par\\vspace{2mm}\\noindent\\hrulefill}}}
        
        \usepackage{enumitem}
        \usepackage{multirow}
        \usepackage{amsmath}
        \usepackage{changepage,ifthen}
        %\usepackage{boxedminipage}
        %\usepackage{theorem}
        \usepackage{verbatim}
        \usepackage{tabularx}
        %\usepackage{moreverb}
        \usepackage{times}
        %\usepackage{relsize}
        \usepackage{pst-barcode}
        \usepackage{tikz}
        \setlength{\\textwidth}{185mm}
        \setlength{\\oddsidemargin}{-0.5in}
        \setlength{\\evensidemargin}{0in}
        \setlength{\\columnsep}{8mm}
        \setlength{\\topmargin}{-28mm}
        \setlength{\\textheight}{265mm}
        \setlength{\\itemsep}{0in}
        \\begin{document}
        \\pagestyle{empty}
        %\lstset{language=python}
        """
    
    files = []
    for t in provas: # acha as turmas
        files.append(t[0])

    for fff in sorted(set(files)): # para cada turma
        
        f = fff[:-4]+'.tex'
        
        past = f[10:]
        filename = past[past.find(barra):]
        past = mypathTex+barra+past[:past.find(barra)]
        try:
            os.stat(past)
        except:
            os.mkdir(past)

        past += barra+folderQuestions
        try:
            os.stat(past)
        except:
            os.mkdir(past)

        f = past+filename
        

        with open(f, 'w') as arqprova:
            
            print "latex file saved with the tests of all students of the class(es):",f
            arqprova = open(f,'w')
            arqprova.write(preambulo1.decode('utf-8').encode("latin1"))
            
            if False:
                arqprova.write("\\begin{center}\n\n")
                arqprova.write("\\resizebox{!}{5mm}{Provas criadas por}\\vspace{1cm}\n\n")
                arqprova.write("\\resizebox{!}{5mm}{createTexTests.py}\\vspace{1cm}\n\n")
                arqprova.write("\\resizebox{!}{5mm}{para o arquivo/turma:}\\vspace{1cm}\n\n")
                arqprova.write("\\resizebox{!}{5mm}{"+ filename[1:-4].replace('_','\_') + "}\\vspace{1cm}\n\n")
                arqprova.write("\\resizebox{!}{5mm}{Guarde com seguran\c ca o arquivo abaixo:}\\vspace{1cm}\n\n")
                arqprova.write("\\resizebox{!}{5mm}{"+ filename[1:-4].replace('_','\_') + "\_GAB}\\vspace{1cm}\n\n")
                arqprova.write("\\resizebox{!}{5mm}{Este arquivo contem os gabaritos}\\vspace{1cm}\n\n")
                arqprova.write("\\resizebox{!}{5mm}{individuais de cada teste!!!}\\vspace{1cm}\n\n")
                arqprova.write("\\resizebox{!}{7mm}{\\'E \\'unico toda vez que gera o .tex.}\\vspace{1cm}\n\n")
                arqprova.write("\\end{center}\n\n")
                arqprova.write("\\newpage\\thispagestyle{empty}\\mbox{}\\newpage\n")


            for t in provas:
                if fff is t[0]: # se prova é da mesma turma, acrescente
                    ff = t[0]
                    ff = ff[:-4]
                    strTurma = ff[len(ff)-ff[::-1].find(barra):]
                    strTurma = strTurma.replace("_","$\\_$")


                    ###### Padroes dos quadros de respostas ######

                    numQuestoes = len(t[3])-numQT # somente questões de múltpla escolha
                    numRespostas = len(t[3][0][1])
                    
                    if numQuestoes>0:
                        
                        let = letras_1[0:numRespostas]
                        strResps = (',').join([(let[x]+'/'+ str(x+1)) for x in range(len(let))])
                
                        # questões por quadro
                        numQuadros = numQuestoes/maxQuestQuadro
                        numResto = numQuestoes % maxQuestQuadro
                        if numResto:
                            numQuadros+=1
                        if numQuadros==0:
                            numQuadros+=1
                        
                        maxQuadrosHoz = int(config['maxQuadrosHoz'])

                        if numQuestoes/maxQuestQuadro < maxQuadrosHoz:
                            maxQuadrosHoz = int(numQuestoes/maxQuestQuadro)
                        
                        numQuadrosHoz = numQuadros
                        if maxQuadrosHoz<numQuadros:
                            numQuadrosHoz = maxQuadrosHoz
            
                        numQuestoesQuadro = maxQuestQuadro
                        if numQuestoes < maxQuestQuadro:
                            numQuestoesQuadro = numQuestoes
                        QL=1
                        if maxQuadrosHoz:
                            QL = numQuadros/maxQuadrosHoz # quadros por linha
                        QC = numQuadrosHoz            # quadros por coluna
                        if QC==0:
                            QC=1
                        fimQuadro_ij = np.zeros([QL,QC])
                        contadorQuestoes = 0
                        for j in range(QC):
                            for i in range(QL):
                                contadorQuestoes += numQuestoesQuadro
                                fimQuadro_ij[i][j] = contadorQuestoes
                        if numQuestoes > maxQuestQuadro:
                            fimQuadro_ij[QL-1][QC-1] += numResto

                        numQuestStart = numQuestEnd = 0
 
                    if int(MCTest_sheets)!=1: # foi escolhido a opção de gerar somente o quadro de respostas

                        ################# pagina de resposta - Parte 1 ##############
                        
                        defineHeader(arqprova,strTurma,t[1],t[2]) # cabeçalho da página
                        
                        arqprova.write("\\begin{pspicture}(6,0in)\n")
                        arqprova.write("\\psbarcode[scalex=1.6,scaley=0.35]{%s}{}{ean13}\n" % str(t[1]).zfill(12)) #includetext
                        arqprova.write("\\end{pspicture}\n")
                        
                        
                        if (config['instructions1']!="\n"):
                            arqprova.write("\\\\{\\scriptsize\n\n\\noindent\\textbf{"+instrucoes+"}\\vspace{-1mm}\\begin{verbatim}\n")
                            arqprova.write(config['instructions1'].decode('utf-8').encode("latin1"))
                            arqprova.write("\\end{verbatim}\n")

                        if (config['titPart1']!="\n"):
                            arqprova.write("\\begin{center}\\textbf{"+config['titPart1'].decode('utf-8').encode("latin1")+"}\\end{center}\n")

                        arqprova.write("\\vspace{-5mm}\\noindent\\varhrulefill[0.4mm]\\vspace{1mm}\n\n")
                        arqprova.write("\\vspace{-3mm}\\noindent\\varhrulefill[0.4mm]\\vspace{1mm}\n\n")
    
                        #print numQuestoes,numQuadros,numQuestoesQuadro, numResto
                        arqprova.write("\\begin{center}\n")

                        for i in range(QL): # para cada linha de quadros
                            for j in range(QC): # para cada coluna de quadros

                                if fimQuadro_ij[i][j] == numQuestoes: # para o último quadro
                                    numQuestStart = int(fimQuadro_ij[i][j] - numQuestoesQuadro + 1 - numQuestoes%numQuestoesQuadro)
                                else:
                                    numQuestStart = int(fimQuadro_ij[i][j] - numQuestoesQuadro + 1)

                                numQuestEnd = int(fimQuadro_ij[i][j])
                                #print "quadro",i,j, numQuestStart, numQuestEnd
                                
                                arqprova.write("\\begin{tikzpicture}[font=\\tiny]\n")
                                arqprova.write("  \\foreach \\letter/\\position in {%s} {\n" % strResps)
                                arqprova.write("    \\node[inner sep=3pt] at ({\\position * 0.5},0) {\\letter};\n")
                                arqprova.write("  }\n")
                                arqprova.write("  \\foreach \\line in {%s,...,%s} {\n" % (numQuestStart, numQuestEnd) )
                                arqprova.write("     \\begin{scope}[xshift=0cm,yshift=-(\\line-%s+1)*5mm]\n" % (numQuestStart))
                                arqprova.write("       \\foreach \\letter/\\position in {%s} {\n" % strResps)
                                #arqprova.write("           \\node[draw,fill,gray!80!white,inner sep=9pt] at (-0.5,0) {};\n")
                                arqprova.write("           \\node at (-0.1,0) {\\line};\n")
                                arqprova.write("           \\node[fill=black!30,draw,circle,inner sep=3pt] at ({\\position * 0.5},0) {};\n")
                                arqprova.write("           \\node[fill=white,draw,circle,inner sep=2pt] at ({\\position * 0.5},0) {};\n")
                                arqprova.write("       }\n")
                                arqprova.write("     \\end{scope}\n")
                                arqprova.write("  }\n")
                                arqprova.write("\\end{tikzpicture}\\hspace{%s cm}\n" % 1 )#(5-numQuadros))
                            arqprova.write("\n\n")


                        arqprova.write("\\end{center}\n")
                        saltaLinhas = max(0,15-numQuestoesQuadro/2)
                        
                        #arqprova.write("\\vspace{%s cm}\\noindent\\hrulefill\n\n" % saltaLinhas )
                        
                        arqprova.write("\\vspace{1cm}\\noindent\\varhrulefill[0.4mm]\\vspace{1mm}\n\n")
                        arqprova.write("\\vspace{-3mm}\\noindent\\varhrulefill[0.4mm]\\vspace{1mm}\n\n")

                        arqprova.write(config['endTable'].decode('utf-8').encode("latin1"))

                        arqprova.write("\\newpage")
                        if duplexPrinting!=0:
                            arqprova.write("\\thispagestyle{empty}\\mbox{}\n \\ \ \n\\newpage\n")
            
                    if int(MCTest_sheets)!=0: # foi escolhido a opção de gerar somente a página de respostas
 
                        ##################  pagina de questoes - Parte 2 ##################

                        
                        if numQuestoes>0:
                            defineHeader(arqprova,strTurma,t[1],t[2]) # cabeçalho da página
                            arqprova.write("\n\\vspace{4mm}\n")
                            
                            if (config['instructions2']!="\n"):
                                arqprova.write("\\\\{\\scriptsize\n\n\\noindent\\textbf{"+instrucoes+"}\\vspace{-1mm}\\begin{verbatim}\n")
                                arqprova.write(config['instructions2'].decode('utf-8').encode("latin1"))
                                arqprova.write("\\end{verbatim}\n")
                        
                            if (config['titPart2']!="\n"):
                                arqprova.write("\\begin{center}\\textbf{"+config['titPart2'].decode('utf-8').encode("latin1")+"}\\end{center}\n")
                                
                            arqprova.write("{\\small\n")
                            arqprova.write("\\begin{questions}\n")
                            arqprova.write("\\itemsep0pt\\parskip0pt\\parsep0pt\n")
                            for q in t[3]: # questões
                                if q[1]:
                                    qstr = q[0]
                                    #print ">>>",qstr
                                    arqprova.write("\\question %s\n" % qstr.decode('utf-8').encode("latin1"))
                                    arqprova.write("\\begin{choices}\n") #oneparchoices - choice
                                    arqprova.write("\\itemsep0pt\\parskip0pt\\parsep0pt\n")
                                    for r in q[1]: # respostas
                                        #print ">>",r
                                        arqprova.write("\\choice %s\n" % r.decode('utf-8').encode("latin1"))
                                    arqprova.write("\\end{choices}\n")
                            arqprova.write("\\end{questions}\n")
                            arqprova.write("}")
                            arqprova.write("\n \ \ \\ \n \\newpage\n")

                        if numQT>0:
                            ##################  questoes dissertativas - Parte 3 ##################
                            if headerByQuestion!=1: # =1, um cabeçalho por questão
                                defineHeader(arqprova,strTurma,t[1],t[2]) # cabeçalho da página
                                arqprova.write("\n\\vspace{4mm}\n")
                        
                            if config['titPart3']!="\n":
                                arqprova.write("\\begin{center}\\textbf{"+config['titPart3'].decode('utf-8').encode("latin1")+"}\\end{center}\n")
                            
                            arqprova.write("{\\small\n")
                            #arqprova.write("\\begin{questions}\n")
                            #arqprova.write("\\itemsep0pt\\parskip0pt\\parsep0pt\n")
                            for q in sorted(t[3]): # questões
                                if q[1]==[]:
                                    if headerByQuestion==1: # um cabeçalho na página por questão
                                        defineHeader(arqprova,strTurma,t[1],t[2])
                                        arqprova.write("\n\n\\vspace{4mm}")
                                    arqprova.write("\\noindent %s \n\n" % q[0].decode('utf-8').encode("latin1"))
                                    arqprova.write("\n \ \ \\ \n \\newpage\n")
                                    #arqprova.write("\\question %s\n" % q[0].decode('utf-8').encode("latin1"))
                            #arqprova.write("\\end{questions}\n")
                            arqprova.write("}\n")


            arqprova.write("\\end{document}")
            arqprova.close() # final do arquivo

def createTex2PDF(provas):
    files = []
    for t in provas: # acha as turmas
        files.append(t[0])
    for fff in sorted(set(files)): # para cada turma
        f = fff[:-4]+'.tex'
        past = f[10:]
        arq = past[past.find(barra):]
        past = mypathTex+past[:past.find(barra)]
        past += barra+folderQuestions
        f = past+arq
        p = os.getcwd()
        os.chdir(p+past[1:])
        os.system('cd '+f[len(past)+1:])
        os.system('latex '+'.'+arq)
        if os.name == 'nt': # Windows
            os.system('dvips -P pdf '+'.'+arq[:-4]+'.dvi')
            os.system('ps2pdf '+'.'+arq[:-4]+'.ps')
            os.system('del *.aux *.dvi *.aux *.log *.ps')
        else:
            os.system('dvipdf '+'.'+arq[:-4]+'.dvi')
            os.system('rm *.aux *.dvi *.aux *.log')
        os.chdir(p)
                                       

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

def main():
    global turmas, gabaritos, randomTests, barra, MCTest_sheets, folderQuestions, folderCourse
    global numQE, numQM, numQH, numQT, duplexPrinting, maxQuestQuadro, maxQuadrosHoz, headerByQuestion
    global config
    
    try:
        if len(sys.argv)==2:
            getConfig(sys.argv[1]) # ler as variáveis de configuração e layout

            turmas = classesReadFiles(readClassFiles(folderCourse))
            provas=[]
            gabaritos=[]
            listao = questionsReadFiles(readQuestionsFiles(folderQuestions))
            provas, gabaritos = createTests(listao, turmas)
            createTexTests(provas)
            if template!=0:
                savesTemplates(gabaritos)
            createTex2PDF(provas)

    except ValueError:
        print "Oops!  Erro in File:",sys.argv[1], "Try again..."


if __name__ == '__main__':
    main()

