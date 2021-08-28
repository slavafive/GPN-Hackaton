import requests
from bs4 import BeautifulSoup


def find_company_info(id):
    URL = "https://companies.rbc.ru/id/"
    page = requests.get(URL + id)

    soup = BeautifulSoup(page.content, "html.parser")
    company_details_cards = soup.find_all("div", class_="info-card company-detail__block")
    company_info = {}

    for card in company_details_cards:
        title_element = card.find("a", class_="info-card__title")
        if title_element != None and title_element.text == 'Контакты':
            cell_container = card.find("div", class_="info-cell__container")
            cells = cell_container.find_all("div", class_="info-cell")
            for cell in cells:
                cell_title = cell.find(['a', 'span'], class_="info-cell__small").text
                if cell_title == 'Адрес':
                    address = cell.find(['a', 'span'], class_="info-cell__text").text
                    company_info['address'] = address.strip()
                if cell_title == 'Телефон':
                    phone_number = cell.find(['a', 'span'], class_="info-cell__text").text
                    company_info['phone'] = phone_number.strip()
                if cell_title == 'Сайт':
                    website = cell.find(['a', 'span'], class_="info-cell__text company-contacts__link").text
                    company_info['website'] = website.strip()
                if cell_title == 'E-mail':
                    email = cell.find(['a', 'span'], class_="info-cell__text").text
                    company_info['email'] = email.strip()
    return company_info


if __name__ == '__main__':
    # 1173850011411-ooo-irkutskij-zavod-polimerov
    print(find_company_info('1137847255545-ooo-reforma'))
