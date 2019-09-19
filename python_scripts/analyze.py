# !/usr/bin/python3
import spacy
import os
import json
import matplotlib.pyplot as plt

from preprocessing import read_content
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords, mac_morpho
from nltk import data, download

# try:
#    data.find('averaged_perceptron_tagger')
# except LookupError:
#    download('averaged_perceptron_tagger')


nlp = spacy.load('pt_core_news_sm')

remove_tags = ["VERB", "ADP", "DET", "CCONJ"]


def remove_verbs(sentence):
    content = ""
    for token in nlp(sentence):
        if token.pos_ not in remove_tags:
            content += token.text + " "
    return content


def check_verb(word):
    sentence = "ela " + word.lower()
    token = nlp(sentence)
    if token[1].pos_ in remove_tags:
        return True
    return False


def to_remove(word):
    if not word:
        return True

    token = nlp(word)
    if token[0].pos_ not in remove_tags and not check_verb(word):
        return False
    return True


def word_cloud(document):
    stop_words = stopwords.words('portuguese')
    content = ''
    for pauta in document['pautas']:
        assunto = ' '.join(
            [word.lower() for word in pauta['assunto'].split(' ') if word not in stop_words and not to_remove(word)])
        # remove_verbs(assunto)
        content += assunto + " "

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
            print(pauta)
            topics.append(pauta)
    return topics


def search_topics_with_address(document):
    topics = []

    for pauta in document['pautas']:
        if (pauta['assunto'].lower().find(' rua ') > 0):
            topics.append(pauta['assunto'])

    return topics


if __name__ == "__main__":
    path = "../documents"
    files = []

    for dir_path, _, filenames in os.walk(path):
        for filename in [f for f in filenames if f.endswith(".pdf")]:
            files.append(os.path.join(dir_path, filename))

    for file in files[0:1]:
        # print(file)
        document = read_content(file)

        if not document:
            continue

        word_cloud(document)
        # print(json.dumps(document, sort_keys=True, indent=4, ensure_ascii=False))

        #topics = search_topics(document)

        # print('{} topics | found {} topics = {:.2f}%'
        #      .format(
        #          len(document['pautas']),
        #          len(topics),
        #          (len(topics) * 100)/len(document['pautas'])
        #      )
        #      )

        # TODO: encontrar ruas
        #topics = search_topics_with_address(document)
        # for topic in topics:
        #    print(topic)
