from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://ca.indeed.com/jobs?q=cook&l=Kanata%2C%20ON&from=searchOnHP').text
soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find_all('h2', class_ = 'jobTitle css-198pbd eu4oa1w0')
print(jobs)