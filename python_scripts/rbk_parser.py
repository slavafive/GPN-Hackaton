import requests
from bs4 import BeautifulSoup
import re
from python_scripts.find_contacts import find_company_info


CATEGORIES_MAP = {
    'ТЭК': 543,
    'химическая промышленность': 557,
    'металлургия': 560,
    'угольная промышленность': 608,
    'нефтегазовая промышленность': 613,
    'добыча полезных ископаемых': 617
}


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
        company_info.update(find_company_info(company_info['id']))
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


if __name__ == '__main__':
    category = 'химическая промышленность'
    print(f'Категория: {category}')
    companies = parse_companies_by_category(category_id=CATEGORIES_MAP[category], page_limit=5)
    print(f'Найдено компаний: {len(companies)}')
    print(f'Первые 10 компаний: {companies[:10]}')
