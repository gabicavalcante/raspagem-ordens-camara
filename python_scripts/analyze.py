import os
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
    files = os.listdir('../documents/Abril/')
    for file in files:
        document = read_content('../documents/Abril/' + file)
        topics = search_topics(document)

        print('{} topics | found {} topics = {:.2f}%'
              .format(
                  len(document['pautas']),
                  len(topics),
                  (len(topics) * 100)/len(document['pautas'])
              )
              )
