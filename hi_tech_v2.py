from bs4 import BeautifulSoup
import requests
from requests.exceptions import MissingSchema, InvalidURL
from saver import save

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
    'accept': '*/*'
}


def get_html(url, params=None):
    r = requests.get(url=url, headers=HEADERS, params=params)
    return r


def check_connection(url: str):
    try:
        html_page = get_html(url)
    except MissingSchema:
        print("[X]Ошибка подключения.")
        return False
    except InvalidURL:
        print("[X]Неправильный адрес.")
        return False
    connected = True if html_page.status_code == 200 else False
    if connected:
        print("[V]Подключение успешно.")
        return html_page.content
    else:
        print("[X]Ошибка подключения.")
        return False


def data_extracting(html):
    soup = BeautifulSoup(html, 'html.parser')
    raw_data = soup.find_all('div', {'class': 'ypi-grid-list__item_body'})
    cleaned_data = []
    for item in raw_data:
        cleaned_data.append({
            'title': item.find_all('a', {'class': 'product-title'})[0].text.strip(),
            'price': item.find('span', {'class': 'ty-price-num'})
                .text.replace('\xa0', '').replace(' ', '').strip(),
            'stock': item.find('span', {'class': 'ty-qty-in-stock ty-control-group__item'})
                .text.replace('\ue86c', '').strip(),
            'uri': item.find('a', {'class': 'product-title'})['href'],
        })
    return cleaned_data


def main():
    url = input("Введите адрес на продукт:\n")
    connection = check_connection(url)
    if connection:
        cleaned_data = []
        pages = int(BeautifulSoup(connection, 'html.parser').find_all
                    ('a', {'class': 'cm-history ty-pagination__item cm-ajax'})[-1].get_text())
        for page in range(1, pages + 1):
            print(f"Страница {page} из {pages}")
            page = get_html(url, params={'page': page})
            for item in data_extracting(page.content):
                cleaned_data.append(item)
        path = input("Введите имя файла с раширением .csv чтобы сохранить его:\n")
        try:
            save(cleaned_data, path)
        except Exception as e:
            print(e)
    else:
        return None


if __name__ == '__main__':
    main()
