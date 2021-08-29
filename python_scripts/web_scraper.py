from bs4 import BeautifulSoup
import requests
import re
from googlesearch import search
import pandas as pd

from ml.vectorizer import vectorize_corpus
from python_scripts.text_processing import clean_text


def google_search(query):
    with requests.session() as c:
        url = 'https://www.google.co.in'
        query = {'q': query}
        urllink = requests.get(url, params=query)
        return urllink.url


def parse_text_from_site(url):
    try:
        page = requests.get(url)
        paragraphs = BeautifulSoup(page.content, 'html.parser').find_all(['p', 'li'])
        content = []
        for p in paragraphs:
            text = p.getText()
            if text != '':
                content.append(text + ' ')
        all_content = ' '.join(content)
        all_content = re.sub(r'\s+', ' ', all_content)
        return all_content
    except Exception as e:
        print(e)
        return 'Произошла ошибка при запросе'


def parse_texts_from_top_sites(query, n=5):
    texts = []
    for url in search(query, tld="co.in", num=n, stop=n, pause=2, lang='ru'):
        text = parse_text_from_site(url)
        texts.append(text)
    return texts


def save_vectorized_texts():
    n = 5
    companies_df = pd.read_csv('../data/companies.csv')
    corpus = []
    names = []
    i = 1
    for name in companies_df['name'].values:
        print(i, '\t', name)
        i += 1

        names += n * [name]
        texts = parse_texts_from_top_sites(query=f'Информация о компании {name}', n=n)
        corpus.extend(texts)

    corpus = list(map(clean_text, corpus))
    vectorized_corpus = vectorize_corpus(corpus)
    vectorized_corpus_df = pd.DataFrame(vectorized_corpus)
    df = pd.DataFrame({'name': names})
    df = pd.concat([df, vectorized_corpus_df], axis=1)
    df.to_csv('../data/vec_google.csv', index=False)


if __name__ == '__main__':
    texts = parse_texts_from_top_sites(query='Информация о компании Газпром', n=5)
    clean_texts = list(map(clean_text, texts))
    vectorized_texts = vectorize_corpus(clean_texts)
