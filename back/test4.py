# Просмотр по вакансиям

from bs4 import BeautifulSoup
import requests

url = "https://hh.ru/vacancies/avtor"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"
}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')

vacs, money, exp, busyness, company, address =  [], [], [], [], [], []

about_job = soup.find_all('div', class_=("wrapper-flat--H4DVL_qLjKLCo1sytcNI","backplate-module_content-wrapper-flatten-on-xs__Jb8w0"))
for div in about_job:
    vacs.append(div.h1.text)
    money.append(div.div.span.text)
    exp.append(div.p.text)
    second_p = div.find('p', attrs={'data-qa': 'vacancy-view-employment-mode'})
    busyness.append(second_p.text)

about_company = soup.find_all('div', class_=("vacancy-company-redesigned"))
for div in about_company:
    second_div = div.find('div', attrs={'data-qa': 'vacancy-company__details'})
    company.append(second_div.text)
    address.append(div.find_all("div")[-1].text)
company.pop(-1)
address.pop(-1)

vacs = [element.replace('\xa0', ' ') for element in vacs]
money = [element.replace('\xa0', ' ') for element in money]
exp = [element.replace('\xa0', ' ') for element in exp]
busyness = [element.replace('\xa0', ' ') for element in busyness]
company = [element.replace('\xa0', ' ') for element in company]
address = [element.replace('\xa0', ' ') for element in address]

print(vacs, money, exp, busyness, company, address)