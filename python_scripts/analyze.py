# !/usr/bin/python3
# -*- coding: utf-8 -*-
import spacy
import json
from bson.objectid import ObjectId

import matplotlib.pyplot as plt

from wordcloud import WordCloud
from nltk.corpus import stopwords, mac_morpho
from nltk import data, download

from nltk.tokenize import WhitespaceTokenizer

from db import collection

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
    stop_words = set(stopwords.words('portuguese'))
    new_words = []
    with open("python_scripts/stopwords_portuguese.txt", 'r') as f:
        [new_words.append(word) for line in f for word in line.split()]

    all_stopwords = stop_words.union(new_words)

    content = ''

    for pauta in document['pautas']:
        assunto = ' '.join(
            [word.lower() for word in WhitespaceTokenizer().tokenize(pauta['assunto']) if word not in stop_words and not to_remove(word)])
        content += assunto + " "

    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          stopwords=all_stopwords,
                          min_font_size=10,
                          collocations=False).generate(content)
    # print(wordcloud.words_)

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
        if (pauta['assunto'].lower().find(' rua ') > 0) or (pauta['assunto'].lower().find(' avenida ') > 0) or (pauta['assunto'].lower().find(' bairro ') > 0):
            topics.append(pauta['assunto'])

    flag = False
    address = ""
    addresses = []
    count = 1
    for topic in topics:
        for word in topic.split(' '):
            if word.lower() in ['rua', 'avenida', 'bairro'] or flag:
                flag = True
                address += word + ' '
                count += 1
            if count == 5:
                flag = False
                count = 1
                break
        if "Requer" not in address:
            addresses.append({'address': address, 'topic': topic})
        address = ""
    return addresses


if __name__ == "__main__":
    document = collection.find_one(
        {'_id': ObjectId('5dbc3d2cfcaa0c48eadcac4a')})
    assuntos = [pauta.get('assunto') for pauta in document.get('pautas')]
    import ipdb
    ipdb.set_trace()


    # word_cloud(document)
    # print(json.dumps(document, sort_keys=True, indent=4, ensure_ascii=False))

    # topics = search_topics(document)
    # print('{} topics | found {} topics = {:.2f}%'
    #      .format(
    #          len(document['pautas']),
    #          len(topics),
    #          (len(topics) * 100)/len(document['pautas'])
    #      )
    # )

    # maps
    # addresses = search_topics_with_address(document)
    # import maps
    # maps.create_map(addresses)
