#Kyle Button
#Purpose: To take a dataset of information and extract it into a clean table

#imports
import requests
from bs4 import BeautifulSoup
import unicodedata

#function to fetch and parse data from single page
def extract_books_from_page(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    books = []
    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        price = book.select_one('p.price_color').text
        books.append((title, price))
    return books

base_url = 'https://books.toscrape.com/'
all_books = extract_books_from_page(base_url)

#tracking amount of books scraped
total_books_scraped = len(all_books)

while True:
    response = requests.get(base_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    next_button = soup.select_one('li.next a')
    if not next_button:
        break

    next_page = next_button['href']
    base_url = f'https://books.toscrape.com/{next_page}'
    all_books.extend(extract_books_from_page(base_url))

def parse_price(price_str):
    price_str = unicodedata.normalize('NFKD', price_str)
    print(f"Debug price_str: '{price_str}'")
    price_str = price_str.strip().replace('£', '').replace(',', '')
    try:
        return float(price_str)
    except ValueError as e:
        # Print error if conversion fails
        print(f"Error parsing price: {price_str}")
        raise e

all_books_sorted = sorted(all_books, key=lambda x: parse_price(x[1]), reverse=True)

for title, price in all_books_sorted:
    print(f'Title: {title},     Price: {price}')
    print(f'Total Books: {total_books_scraped}')
