from bs4 import BeautifulSoup
import requests
import time
import os

print("put some skill that your not familiar with")
unfamiliar_skill = input('>')
print(f"filtering out {unfamiliar_skill}")

def find_jobs():
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=Home_Search&from=submit&asKey=OFF&txtKeywords=&cboPresFuncArea=35').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_ ='clearfix job-bx wht-shd-bx')
    for index, job in enumerate(jobs):
        date_Posted = job.find('span', class_ = 'sim-posted').text
        if 'today' in date_Posted:
            company_name = job.find('h3', class_ = 'joblist-comp-name').text.replace(' ','')
            skills = job.find('span', class_ = 'srp-skills').text.replace(' ','')
            more_info = job.header.h2.a['href']
            if unfamiliar_skill not in skills:
                with open(f'Jobsite Scrapper/posts/{index}.txt', 'w') as f:
                    f.write(f"\nCompany Name: {company_name.strip()}")
                    f.write(f"\nRequired Skills: {skills.strip()}")
                    f.write(f"Date Posted: {date_Posted}")
                    f.write(f"More Info: {more_info.strip()}")
                print(f'File saved: {index}')
            
if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)
