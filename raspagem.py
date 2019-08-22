import sys
import os
import requests
from bs4 import BeautifulSoup


MONTHS = {
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
    '12': 'Dezembro'
}

YEARS_ID = {
    '2019': '8',
    '2018': '7',
    '2017': '6',
    '2016': '6',
    '2015': '5'
}

for month in MONTHS:
    print('{}...'.format(MONTHS[month]))
    data = {
        'ano_id': YEARS_ID['2018'],
        'mes_id': month
    }
    url = "https://www.cmnat.rn.gov.br/ordens/send"
    response = requests.post(url, data=data)
    doc = BeautifulSoup(response.text, 'html.parser')
    content = doc.select(".listagem-noticias li p a")
    if not content:
        continue

    documents = [c.get_text() for c in content]
    urls = [c['href'] for c in content]

    path = 'documents/{}/'.format(MONTHS[month])
    if not os.path.exists(path):
        os.makedirs(path)

    for doc, url in zip(documents, urls):
        pdf = requests.get(url)
        file_name = '{}'.format(
            doc
            .lstrip()
            .lower()
            .replace(' ', '_')
            .replace('/', '_')
            .replace('-', '_')
        )
        open('documents/{}/{}.pdf'.format(MONTHS[month],
                                          file_name), 'wb').write(pdf.content)
