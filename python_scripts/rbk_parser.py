import requests
from bs4 import BeautifulSoup
import re

from ml.vectorizer import vectorize_corpus
from python_scripts.find_contacts import find_company_info
import json
import pandas as pd

from python_scripts.text_processing import clean_text
from python_scripts.web_scraper import save_vectorized_texts

URL = 'https://companies.rbc.ru/id/'

CATEGORIES_MAP = {
    'ТЭК': 543,
    'химическая промышленность': 557,
    'металлургия': 560,
    'угольная промышленность': 608,
    'нефтегазовая промышленность': 613,
    'добыча полезных ископаемых': 617
}


def parse_company_activities(company_id):
    activities = []
    page = requests.get(URL + company_id)
    soup = BeautifulSoup(page.content, 'html.parser')
    tags_info = soup.find_all('span', {'class': 'company-okved__code'})
    for tag_info in tags_info:
        activity = {
            'code': tag_info.text,
            'description': tag_info.parent.nextSibling.text
        }
        if activity not in activities:
            activities.append(activity)
    return list(activities)


def parse_companies_found(url):
    page = requests.get(url)
    tags_info = BeautifulSoup(page.content, 'html.parser').find_all('small')
    return int(re.sub('\D', '', tags_info[0].text))


def parse_companies(url):
    companies = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tags_info = soup.find_all('a', {'class': 'company-name-highlight'})
    for tag_info in tags_info:
        link = tag_info.attrs['href']
        company_info = {
            'name': tag_info.text.strip(),
            'link': link,
            'id': link.split('/')[-2],
            'title': tag_info.attrs['title'].strip()
        }
        company_id = company_info['id']
        company_info.update({'activities': parse_company_activities(company_id)})
        company_info.update(find_company_info(company_id))
        companies.append(company_info)
    return companies


def parse_companies_by_category(category_id, page_limit=50):
    COMPANIES_ON_PAGE = 20
    url = f'https://companies.rbc.ru/search/?category_id={category_id}&'
    companies_found = parse_companies_found(url)
    companies = []
    last_page = min(page_limit, companies_found // COMPANIES_ON_PAGE + 1)
    for page in range(1, last_page + 1):
        current_companies = parse_companies(url + f'page={page}')
        for current_company in current_companies:
            current_company.update({
                'category_id': category_id
            })
        companies.extend(current_companies)
    return companies


def save_companies():
    companies = []
    names = []
    ids = []
    corpus = []

    for category in CATEGORIES_MAP:
        print(f'Категория: {category}')
        current_companies = parse_companies_by_category(category_id=CATEGORIES_MAP[category], page_limit=50)
        print(f'Кол-во компаний: {len(current_companies)}')
        companies.extend(current_companies)
        for company in current_companies:
            names.append(company['name'])
            ids.append(company['id'])
            activities = []
            for activity in company['activities']:
                activities.append(activity['description'])
            activities = ' '.join(activities)
            corpus.append(activities)

    corpus = list(map(clean_text, corpus))
    vectorized_corpus = vectorize_corpus(corpus)
    vectorized_corpus_df = pd.DataFrame(vectorized_corpus)

    with open('../data/companies.json', 'w') as file:
        json.dump(companies, file)

    pd.concat([pd.DataFrame({'name': names}), vectorized_corpus_df], axis=1).to_csv('../data/vec_rbk.csv', index=False)
    pd.DataFrame({'name': names, 'id': ids, 'corpus': corpus}).to_csv('../data/companies.csv', index=False)


if __name__ == '__main__':
    save_companies()
    # save_vectorized_texts()
