# !/usr/bin/python3
import os
import json
import matplotlib.pyplot as plt

from preprocessing import read_content
from wordcloud import WordCloud, STOPWORDS


def word_cloud(document):
    stop_words = stopwords.words('portuguese')
    content = ''
    for pauta in document['pautas']:
        assunto = ' '.join(
            [word.lower() for word in pauta['assunto'].split(' ') if word not in stop_words])
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


def search_topics(document):
    topics = []
    for pauta in document['pautas']:
        found_topic = False
        for word in pauta['assunto'].split(' '):
            if word.lower() in ['título', 'cidadão', 'natalense', 'natalence']:
                found_topic = True
        if found_topic:
            topics.append(pauta)
    return topics


if __name__ == "__main__":
    path = "../documents"
    files = []

    for dir_path, _, filenames in os.walk(path):
        for filename in [f for f in filenames if f.endswith(".pdf")]:
            files.append(os.path.join(dir_path, filename))

    # TODO: error ['../documents/Junho/ordem_do_dia_25_06_19.pdf']
    for file in files:
        # print(file)
        document = read_content(file)

        if not document:
            continue
        # print(json.dumps(document, sort_keys=True, indent=4, ensure_ascii=False))
        topics = search_topics(document)

        print('{} topics | found {} topics = {:.2f}%'
              .format(
                  len(document['pautas']),
                  len(topics),
                  (len(topics) * 100)/len(document['pautas'])
              )
              )
