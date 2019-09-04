#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
# requests allows you to send requests, without the need for manual labor
# https://2.python-requests.org/en/master/
import requests
# a toolkit for dissecting a document and extracting what you need
# https://www.crummy.com/software/BeautifulSoup/
from bs4 import BeautifulSoup

months = {
    '01': 'Janeiro',
    '02': 'Fevereiro',
    '03': 'Marco',
    '04': 'Abril',
    '05': 'Maio',
    '06': 'Junho',
    '07': 'Julho',
    '08': 'Agosto',
    '09': 'Setembro',
    '10': 'Outubro',
    '11': 'Novembro',
    '12': 'Dezembro',
}

years = {
    '8': '2019',
    '7': '2018',
    '6': '2017',
    '5': '2016',
    '4': '2015',
}

for month, label in months.items():
    print('{}...'.format(label))
    # info to make the request
    parameters = {'ano_id': '8', 'mes_id': month}
    url = "https://www.cmnat.rn.gov.br/ordens/send"

    # request to find the documents
    response = requests.post(url, data=parameters)

    doc = BeautifulSoup(response.text, 'html.parser')
    # find tag a <inside> tag p <inside> tag li
    content = doc.select(".listagem-noticias li p a")
    if not content:
        continue

    # get documents date
    documents = [c.get_text() for c in content]
    # get documents link
    urls = [c['href'] for c in content]

    # create path if it doesnt exist
    path = '../documents/{}/'.format(label)
    if not os.path.exists(path):
        os.makedirs(path)

    for doc, url in zip(documents, urls):
        pdf = requests.get(url)
        file_name = '{}'.format(
            doc
            .lstrip()  # remove initial space
            .lower()  # convert to lowcase
            .replace(' ', '_')
            .replace('/', '_')
            .replace('-', '_'))
        open('../documents/{}/{}.pdf'.format(label,
                                             file_name), 'wb').write(pdf.content)
