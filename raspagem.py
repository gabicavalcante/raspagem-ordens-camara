import sys
import os
import requests
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
    '12': 'Dezembro'
}

years = {
    '8': '2019',
    '7': '2018',
    '6': '2017',
    '5': '2016',
    '4': '2015'
}

for month, label in months.items():
    print('{}...'.format(label))
    parameters = {'ano_id': '8', 'mes_id': month}
    url = "https://www.cmnat.rn.gov.br/ordens/send"

    response = requests.post(url, data=parameters)

    doc = BeautifulSoup(response.text, 'html.parser')
    content = doc.select(".listagem-noticias li p a")
    if not content:
        continue

    documents = [c.get_text() for c in content]
    urls = [c['href'] for c in content]

    path = 'documents/{}/'.format(label)
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
            .replace('-', '_'))
        open('documents/{}/{}.pdf'.format(label,
                                          file_name), 'wb').write(pdf.content)
