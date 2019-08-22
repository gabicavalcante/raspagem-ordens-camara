import json
import itertools
import re

from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tokenize import SpaceTokenizer
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import PyPDF2


PARTIDOS = [
    'PRTB', 'PCB', 'PSTU', 'PP', 'PTdoB', 'PR',
    'PSOL', 'PRB', 'PSL', 'PTN', 'PCO', 'PSDC',
    'PHS', 'PMDB', 'PPS', 'PRP', 'PMN', 'PSC',
    'PSDB', 'PSB', 'PCdoB', 'DEM', 'PTC', 'PT',
    'PTB', 'PV', 'PDT', 'PATRIOTA', 'AVANTE',
    'PMB', 'PSD', 'PROS', 'SD', 'MDB'
]
PUNCTUATIONS = ['(', ')', ';', ':', '[', ']', ',', '-']
TO_SCAPE = ['\n', '\\', '-', 'Œ']


def replace_all(symbol_scape, content):
    new_str = content
    for symbol in symbol_scape:
        new_str = new_str.replace(symbol, '')
    return new_str


def find_orador(keywords, limit=150):
    find_orador = False
    oradores = []
    for keyword in keywords:
        if find_orador and re.search(r'\d\dh', keyword):
            find_orador = False
        if find_orador and keyword != '.':
            oradores.append(keyword)
        if keyword == "ORADOR":
            find_orador = True
    oradores = [s.split('.') for s in oradores if s not in PARTIDOS]
    oradores = list(itertools.chain.from_iterable(oradores))
    oradores_final = []

    count = -1
    for s in oradores:
        if re.search(r'VER[.ª]*[ª.]*', s):
            count += 1
            oradores_final.append('')
        elif s != 'a':
            oradores_final[count] += s + ' '
    return [s.rstrip() for s in oradores_final][0:limit]


def find_topics(keywords):
    flag_titulo = False
    flag_responsavel = False
    flag_assunto = False
    flag_movimento = False

    flag_start_content = False
    pauta = {
        'tipo': '',
        'n': '',
        'responsavel': '',
        'movimento': '',
        'assunto': ''
    }
    list_pautas = []
    for keyword in keywords:
        if keyword == 'PAUTA':
            flag_start_content = True

        if not flag_start_content:
            continue

        if keyword == 'ASSUNTO' and flag_titulo and not flag_movimento:
            pauta['tipo'] = pauta['tipo'].rstrip().replace(' .', '')
            responsavel = re.sub(
                r'VER[.a]*[.ª]*[ .]* ', '',
                pauta['responsavel'].rstrip()).replace(' .', '')
            pauta['responsavel'] = responsavel

            pauta = {
                'tipo': '',
                'n': '',
                'responsavel': '',
                'movimento': '',
                'assunto': ''
            }

            flag_titulo = False
            flag_assunto = True
            continue

        if keyword == 'MOVIMENTO' and flag_assunto and not flag_titulo:
            flag_assunto = False
            flag_movimento = True
            continue

        if keyword in ['PROJETO', 'REQUERIMENTO', 'MOÇÃO'] and not flag_assunto:
            if flag_movimento or flag_start_content:
                if flag_movimento:
                    pauta['assunto'] = pauta['assunto'].replace(
                        ' . ', '')
                    pauta['movimento'] = responsavel = re.sub(
                        r'ESTADO DO RIO GRANDE DO NORTE CÂMARA MUNICIPAL DO NATAL PALÁCIO PADRE MIGUELINHO \d[\d]*', '',
                        pauta['movimento'].rstrip()).replace('.', '').rstrip()
                    list_pautas.append(pauta)
                flag_titulo = True
                flag_assunto = flag_movimento = flag_responsavel = False
            else:
                continue

        if flag_assunto and not flag_titulo:
            pauta['assunto'] += keyword + ' '

        if flag_movimento and not flag_assunto:
            pauta['movimento'] += keyword + ' '

        if flag_titulo and re.search(r'\d/20\d\d', keyword):
            pauta['n'] = keyword
            flag_responsavel = True
        elif flag_titulo and flag_responsavel:
            pauta['responsavel'] += keyword + ' '
        elif flag_titulo and not re.search(r'^N[.]*[\u00ba]+', keyword):
            pauta['tipo'] += keyword + ' '

    return list_pautas


pdf_file_obj = open('documents/Abril/ordem_do_dia_07_05_19.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)

pdf_text = ''
for page in range(pdf_reader.numPages):
    pdf_text += pdf_reader.getPage(page).extractText()
    pdf_text = replace_all(TO_SCAPE, pdf_text)

tokens = word_tokenize(pdf_text)
keywords = [
    word for word in tokens if not word in PUNCTUATIONS]

documento = {}
documento['oradores'] = find_orador(keywords)
documento['pautas'] = find_topics(keywords)

print(json.dumps(documento, sort_keys=True, indent=4, ensure_ascii=False))

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

plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()
