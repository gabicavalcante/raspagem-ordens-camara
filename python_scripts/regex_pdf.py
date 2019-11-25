# -*- coding: utf-8 -*-
import json
import itertools
import PyPDF2
import re
import os
import sys

import nltk
from nltk import word_tokenize
from nltk.tokenize import SpaceTokenizer

import pandas as pd


def read_content(file_path):
    pdfFileObj = open(file_path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)

    pdf_text = ''
    for page in range(pdfReader.numPages):
        page_text = pdfReader.getPage(page).extractText()
        pdf_text += page_text

    return pdf_text


def find_topic(content):
    assunto = re.findall(r"ASSUNTO.*?MOVIMENTO", content, re.DOTALL)
    return assunto


if __name__ == "__main__":
    file_path = "documents/Abril/ordem_do_dia_07_05_19.pdf"
    content = read_content(file_path)
    assuntos = find_topic(content)
    for assunto in assuntos:
        text = re.sub('\s+', ' ', assunto)
        text = re.sub('ASSUNTO: -', ' ', text)
        text = re.sub('MOVIMENTO', ' ', text)
