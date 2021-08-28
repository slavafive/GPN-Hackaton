import numpy as np
import ru_core_news_md

nlp = ru_core_news_md.load()


def vectorize_text(text):
    return nlp(text).vector


def vectorize_corpus(corpus, method='word2vec'):
    if method == 'word2vec':
        with nlp.disable_pipes():
            vectors = np.array([nlp(text).vector for text in corpus])
    return vectors


if __name__ == 'main':
    pass
