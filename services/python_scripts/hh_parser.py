from bs4 import BeautifulSoup
import requests


def get_texts_by_tag(url, tag, classname):
    page = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/35.0.1916.47 Safari/537.36 '
    })
    text_info = BeautifulSoup(page.content, 'html.parser').find_all(tag, {'class': classname})
    texts = []
    for text_obj in text_info:
        texts.append(text_obj.text.strip())
    return texts


def get_companies_by_industry(industry):
    i = 0
    companies = []
    while True:
        url = f'https://spb.hh.ru/employers_company/{industry}?page={i}'
        current_companies = get_texts_by_tag(url=url, tag='span', classname='employers-company__description')
        if len(current_companies) == 0:
            break
        companies.extend(list(map(lambda x: x[:-2], current_companies)))
        i += 1
    return companies


industry = 'neft_i_gaz'
INDUSTRIES = {
    'добывающая отрасль': 'dobyvayushaya_otrasl',
    'нефть и газ': 'neft_i_gaz',
    'энергетика': 'energetika'
}
companies = get_companies_by_industry(industry)
print(companies)
