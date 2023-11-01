# import requests
# from bs4 import BeautifulSoup as BS
# import csv

# def get_html(url):
#     responce = requests.get(url)
#     return responce.text

# def get_data(html):
#     soup = BS(html, 'lxml')
#     catalog = soup.find('div', class_="browse-view")
#     laptop = catalog.find('div', calss_="row")
#     print(laptop)
# responce = get_html('https://enter.kg/computers/noutbuki_bishkek')
# get_data(responce)

import requests 
from bs4 import BeautifulSoup as BS 
import csv 
 
def get_html(url): 
    response = requests.get(url) 
    return response.text 

def write_csv(data):
    with open('enter_laptops.csv', 'a') as csv_file:
        names = ['title', 'price', 'image']
        writer = csv.DictWriter(csv_file, delimiter='|', fieldnames=names)
        writer.writerow(data)
 
def get_data(html): 
    soup = BS(html, 'lxml') 
    catalog = soup.find('div', class_ = "browse-view") 
    laptops = catalog.find_all('div', class_='row')
    # print(laptops)
    # laptop = catalog.find("div", class_ = "row") 
    for laptop in laptops:
        try:
            title = laptop.find('a', class_ = "product-image-link") 
            title = title.get("title")
        except:
            title = ''
        try:
            image = laptop.find('img').get('src')
            image = f'https://enter.kg/{image}'
        except:
            image = ''
        try:
            price = laptop.find('span', class_='price').text
        except:
            price = ''
        data = {
            'title': title,
            'image': image,
            'price': price
        }
        write_csv(data)


def get_last_page(html):
    """
    Эта функция находит ссылку на последнюю страницу
    """
    soup = BS(html, 'lxml')
    url_last_page = soup.find('li', class_='pagination-end').find('a').get('href')
    last_page = ''
    for digit in url_last_page:
        if digit.isdigit() or digit=='-':
            last_page+=digit
    last_page = last_page.split('-')
    return int(last_page[0])

def main():
    url = "https://enter.kg/computers/noutbuki_bishkek"
    html = get_html(url)
    last_page = get_last_page(html)
    for page in range(1, last_page+1,100):
        url = f"https://enter.kg/computers/noutbuki_bishkek/results,{page}-{page-1}"
        html = get_html(url)
        data = get_data(html)

main()
