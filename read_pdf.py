# -*- coding: utf-8 -*-
import json
import itertools
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tokenize import SpaceTokenizer

import PyPDF2
import re
import nltk

partidos = ['PRTB', 'PCB', 'PSTU', 'PP', 'PTdoB', 'PR', 'PSOL', 'PRB', 'PSL', 'PTN', 'PCO', 'PSDC', 'PHS',
            'PV', 'PPS', 'PRP', 'PMN', 'PSC', 'PSDB', 'PSB', 'PCdoB', 'DEM', 'PTC', 'PT', 'PTB', 'PMDB', 'PDT',
            'PATRIOTA', 'AVANTE', 'PMB', 'PSD', 'PROS', 'SD', 'MDB']
punctuations = ['(', ')', ';', ':', '[', ']', ',', '-']
scape = ['\n', '\\', '-', 'Œ']


def replace_all(symbol_scape, content):
    new_str = content
    for symbol in symbol_scape:
        new_str = new_str.replace(symbol, '')
    return new_str


def find_orador(keywords):
    find_orador = False
    oradores = []
    for keyword in keywords:
        if find_orador and re.search(r'\d\dh', keyword):
            find_orador = False
        if find_orador and keyword != '.':
            oradores.append(keyword)
        if keyword == "ORADOR":
            find_orador = True
    oradores = [s.split('.') for s in oradores if s not in partidos]
    oradores = list(itertools.chain.from_iterable(oradores))
    oradores_final = []

    count = -1
    for s in oradores:
        if re.search(r'VER[.ª]*[ª.]*', s):
            count += 1
            oradores_final.append('')
        elif s != 'a':
            oradores_final[count] += s + ' '
    return [s.rstrip() for s in oradores_final]


def find_projeto_de_lei(keywords):
    found_projeto = False
    flag_responsavel = False
    pauta = {'tipo': '', 'n': '', 'responsavel': ''}
    list_pautas = []
    for keyword in keywords:
        if keyword in ['PROJETO', 'REQUERIMENTO', 'MOÇÃO']:
            found_projeto = True
        if keyword == 'ASSUNTO':
            pauta['tipo'] = pauta['tipo'].rstrip().replace(' .', '')
            pauta['responsavel'] = re.sub(
                r'VER[.a]*[.ª]*[ .]* ', '', pauta['responsavel'].rstrip()).replace(' .', '')
            list_pautas.append(pauta)
            pauta = {'tipo': '', 'n': '', 'responsavel': ''}
            found_projeto = False
            flag_responsavel = False
            continue

        if found_projeto and re.search(r'\d/20\d\d', keyword):
            pauta['n'] = keyword
            flag_responsavel = True
        elif found_projeto and flag_responsavel:
            pauta['responsavel'] += keyword + ' '
        elif found_projeto and not re.search(r'^N[.]*[\u00ba]+', keyword):
            pauta['tipo'] += keyword + ' '

    return list_pautas


pdfFileObj = open('documents/Abril/ordem_do_dia_30_04_19.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pageObj = pdfReader.getPage(0)

pdf_text = ''
for page in range(pdfReader.numPages):
    pdf_text += pdfReader.getPage(page).extractText()
    pdf_text = replace_all(scape, pdf_text)

tokens = word_tokenize(pdf_text)
stop_words = stopwords.words('portuguese')
keywords = [
    word for word in tokens if not word in stop_words and not word in punctuations]

documento = {}
documento['oradores'] = find_orador(keywords[0:150])
documento['pautas'] = find_projeto_de_lei(keywords)

print(json.dumps(documento, sort_keys=True, indent=4, ensure_ascii=False))
