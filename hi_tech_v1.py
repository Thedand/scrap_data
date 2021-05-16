from bs4 import BeautifulSoup
import grequests
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 ('
                         'KHTML, like Gecko) Version/13.0.2 Safari/605.1.15',
           'Accept': 'ru'}


def get_urls():
    urls = []
    for x in range(1, 3):  # 34
        urls.append(f'https://hi-tech.md/kompyuternaya-tehnika/noutbuki-planshety.../noutbuki/page-{x}')
    return urls


def get_data(urls):
    reqs = [grequests.get(link, headers=headers) for link in urls]
    resp = grequests.map(reqs)
    return resp


def parse(resp):
    product_list = []
    for r in resp:
        sp = BeautifulSoup(r.text, 'lxml')
        items = sp.find_all('div', {'class': 'ypi-grid-list__item_body'})
        for item in items:
            product = {
                'title': item.find_all('a', {'class': 'product-title'})[0].text.strip(),
                'price': item.find('span', {'class': 'ty-price-num'})
                    .text.replace('\xa0', '').replace(' ', '').strip(),
                'stock': item.find('span', {'class': 'ty-qty-in-stock ty-control-group__item'})
                    .text.replace('\ue86c', '').strip(),
                'uri': item.find('a', {'class': 'product-title'})['href'],
            }
            product_list.append(product)
            print('Added: ', product)
    return product_list


urls = get_urls()
resp = get_data(urls)
df = pd.DataFrame(parse(resp))
df.to_csv('product.csv', index=False)
