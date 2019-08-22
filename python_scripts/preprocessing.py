# -*- coding: utf-8 -*-
import json
import itertools
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tokenize import SpaceTokenizer

import PyPDF2
import re
import nltk

# importing all necessery modules
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd

partidos = ['PRTB', 'PCB', 'PSTU', 'PP', 'PTdoB', 'PR', 'PSOL', 'PRB', 'PSL', 'PTN', 'PCO', 'PSDC', 'PHS',
            'PV', 'PPS', 'PRP', 'PMN', 'PSC', 'PSDB', 'PSB', 'PCdoB', 'DEM', 'PTC', 'PT', 'PTB', 'PMDB', 'PDT',
            'PATRIOTA', 'AVANTE', 'PMB', 'PSD', 'PROS', 'SD', 'MDB']
punctuations = ['(', ')', ';', ':', '[', ']', ',', '-']
scape = ['\n', '\\', '-', 'Œ']


def replace_all(symbol_scape, content):
    """
    Replace all 'symbol_scape' from given string

    Args: 
    symbol_scape : document words 
    content: string to remove symbols

    Returns:
        string without symbols 
    """
    new_str = content
    for symbol in symbol_scape:
        new_str = new_str.replace(symbol, '')
    return new_str


def find_orator(keywords):
    """
    Return orators

    Args: 
    keywords : document words 

    Returns:
        a list of orators name 
    """
    found_orators = False
    orators = []
    for keyword in keywords:
        # found somethig like 14h/14h15
        if found_orators and re.search(r'\d\dh', keyword):
            found_orators = False
        # append orator name if not
        if found_orators and keyword != '.':
            orators.append(keyword)
        # found a new orator
        if keyword == "ORADOR":
            found_orators = True
    orators = [s.split('.') for s in orators if s not in partidos]
    orators = list(itertools.chain.from_iterable(orators))
    final_orators = []

    count = -1

    # append string to find orators names
    for s in orators:
        if re.search(r'VER[.ª]*[ª.]*', s):
            count += 1
            final_orators.append('')
        elif s not in ['a', 'ª']:
            final_orators[count] += s + ' '

    return [s.rstrip() for s in final_orators]


def find_topics(keywords):
    flag_title = False
    flag_responsible = False
    flag_subject = False
    flag_forwarding = False

    flag_start_content = False
    topic = {'tipo': '', 'n': '', 'responsavel': '',
             'movimento': '', 'assunto': ''}

    list_topics = []
    for keyword in keywords:
        if keyword == 'PAUTA':
            flag_start_content = True

        if not flag_start_content:
            continue

        if keyword == 'ASSUNTO' and flag_title and not flag_forwarding:
            topic['tipo'] = topic['tipo'].rstrip().replace(' .', '')
            responsavel = re.sub(
                r'VER[.a]*[.ª]*[ .]* ', '',
                topic['responsavel'].rstrip()).replace(' .', '')
            # as vezes teremos mais de um partido envolvido
            # topic['partido'] = responsavel.rsplit(' ', 1)[1]
            topic['responsavel'] = responsavel  # .rsplit(' ', 1)[0]

            flag_title = False
            flag_subject = True
            continue

        if keyword == 'MOVIMENTO' and flag_subject and not flag_title:
            flag_subject = False
            flag_forwarding = True
            continue

        if keyword in ['PROJETO', 'REQUERIMENTO', 'MOÇÃO'] and not flag_subject:
            if flag_forwarding or flag_start_content:
                if flag_forwarding:
                    topic['assunto'] = topic['assunto'].replace(
                        ' . ', '')
                    topic['movimento'] = responsavel = re.sub(
                        r'ESTADO DO RIO GRANDE DO NORTE CÂMARA MUNICIPAL DO NATAL PALÁCIO PADRE MIGUELINHO \d[\d]*', '',
                        topic['movimento'].rstrip()).replace('.', '').rstrip()
                    list_topics.append(topic)

                    topic = {'tipo': '', 'n': '', 'responsavel': '',
                             'movimento': '', 'assunto': ''}

                flag_title = True
                flag_subject = flag_forwarding = flag_responsible = False
            else:
                # quuando a string 'projeto' se repete em motivmento e titulo
                continue

        if (flag_subject and not flag_title):
            topic['assunto'] += keyword + ' '

        if (flag_forwarding and not flag_subject):
            topic['movimento'] += keyword + ' '

        if flag_title and re.search(r'\d/20\d\d', keyword):
            topic['n'] = keyword
            flag_responsible = True
        elif flag_title and flag_responsible:
            topic['responsavel'] += keyword + ' '
        elif flag_title and not re.search(r'^N[.]*[\u00ba]+', keyword):
            topic['tipo'] += keyword + ' '

    return list_topics


def read_content(file_path):
    pdfFileObj = open(file_path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    pdf_text = ''
    for page in range(pdfReader.numPages):
        pdf_text += pdfReader.getPage(page).extractText()
        pdf_text = replace_all(scape, pdf_text)

    tokens = word_tokenize(pdf_text)
    keywords = [
        word for word in tokens if not word in punctuations]

    documento = {}
    documento['oradores'] = find_orator(keywords[0:150])
    documento['pautas'] = find_topics(keywords)

    return documento


def word_cloud():
    stop_words = stopwords.words('portuguese')
    content = ''
    for pauta in documento['pautas']:
        assunto = ' '.join(
            [word.lower() for word in pauta['assunto'].split(' ') if not word in stop_words])
        content += assunto

    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          stopwords=set(STOPWORDS),
                          min_font_size=10).generate(content)

    # plot the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.show()


if __name__ == "__main__":
    documento = read_content('../documents/Abril/ordem_do_dia_07_05_19.pdf')
    print(json.dumps(documento, sort_keys=True, indent=4, ensure_ascii=False))
