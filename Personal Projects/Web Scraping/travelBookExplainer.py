import requests  # Library for making HTTP requests
from bs4 import BeautifulSoup  # Library for parsing HTML
import unicodedata  # Library for handling Unicode characters

# Function to fetch and parse book data from a single page
def get_books_from_page(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    # Ensure the response is interpreted with UTF-8 encoding
    response.encoding = 'utf-8'
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    books = []
    # Iterate over each book entry on the page
    for book in soup.find_all('article', class_='product_pod'):
        # Extract the book title from the 'title' attribute of the <a> tag within <h3>
        title = book.h3.a['title']
        # Extract the price of the book
        price = book.select_one('p.price_color').text
        # Append a tuple (title, price) to the books list
        books.append((title, price))
    return books

# Base URL of the category page containing the list of books
base_url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'

# Initialize the list to hold all book data
all_books = get_books_from_page(base_url)

# Continue fetching data from subsequent pages until there are no more pages
while True:
    # Send an HTTP GET request to the current base URL
    response = requests.get(base_url)
    # Ensure the response is interpreted with UTF-8 encoding
    response.encoding = 'utf-8'
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    # Check if there is a 'next' button to go to the next page
    next_button = soup.select_one('li.next a')
    # If no 'next' button, break the loop
    if not next_button:
        break

    # Extract the relative URL for the next page
    next_page = next_button['href']
    # Construct the full URL for the next page
    base_url = f'https://books.toscrape.com/catalogue/category/books/travel_2/{next_page}'
    # Fetch and add books from the next page to the list
    all_books.extend(get_books_from_page(base_url))

# Function to parse the price string and convert it to a float
def parse_price(price_str):
    # Normalize the string to remove any unexpected characters or accents
    price_str = unicodedata.normalize('NFKD', price_str)
    # Debug print statement to show the raw price string
    print(f"Debug price_str: '{price_str}'")
    # Remove the pound currency symbol and any commas from the price string
    price_str = price_str.strip().replace('£', '').replace(',', '')
    try:
        # Convert the cleaned price string to a float
        return float(price_str)
    except ValueError as e:
        # Print error if conversion fails
        print(f"Error parsing price: {price_str}")
        raise e

# Sort the list of books by price in descending order
all_books_sorted = sorted(all_books, key=lambda x: parse_price(x[1]), reverse=True)

# Print out the titles and prices of the books sorted by price
for title, price in all_books_sorted:
    print(f'Title: {title}, Price: {price}')
