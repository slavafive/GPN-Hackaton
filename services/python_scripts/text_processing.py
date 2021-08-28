from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymorphy2


def normalize_word(word):
    morph = pymorphy2.MorphAnalyzer(lang='ru')
    return morph.parse(word)[0].normal_form


def clean_text(text, normalize=False):
    tokens = word_tokenize(text.lower())
    words = [word for word in tokens if word.isalpha()]
    stopwords_list = stopwords.words('russian')
    words = [word for word in words if word not in stopwords_list]
    if normalize:
        words = list(map(normalize_word, words))
    return ' '.join(words)
