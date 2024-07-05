from bs4 import BeautifulSoup
import requests
import re

url = "https://hh.ru/vacancies/avtor"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"
}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')

# Поиск кол-ва страниц в вакансиях
page = soup.find_all("span", class_="pager-item-not-in-short-range")
page = str(page)
numbers = re.findall(r"<span>(\d+)</span>", page)
numbers = list(map(int, numbers))
if numbers != []:
    num = max(numbers)
else:
    num = 1
if num > 2: num=2 #ограничение от всяких 250+ страниц

href, name = [], []
for pages in range(num):
    # получение данных по вакансиям.
    all_vac = soup.find_all("h2", class_="bloko-header-section-2")
    for h2 in all_vac:
        name.append(h2.span.a.span.text)
        href.append(h2.span.a["href"])
name = [element.lower() for element in name]

vacs, money, exp, busy, company, address, busyness, schedule =  [], [], [], [], [], [], [], []

for link in href:
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")

    

    about_job = soup.find_all('div', class_=("wrapper-flat--H4DVL_qLjKLCo1sytcNI","backplate-module_content-wrapper-flatten-on-xs__Jb8w0"))
    for div in about_job:
        vacs.append(div.h1.text)
        money.append(div.div.span.text)
        second_p = div.find('p', attrs={'data-qa': 'vacancy-view-employment-mode'})
        busy.append(second_p.text)

    # необходимый опыт работы отдельно, тк он перехотел сотрудничать добровольно как норм код
    time = soup.find("span", {"data-qa": "vacancy-experience"})
    time = str(time)
    time = time.replace('<span data-qa="vacancy-experience">', '').replace('</span>','')
    exp.append(time)

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
    busy = [element.replace('\xa0', ' ') for element in busy]
    for element in busy:
        busyness.extend(element.split(', '))  
    company = [element.replace('\xa0', ' ') for element in company]
    address = [element.replace('\xa0', ' ') for element in address]
    schedul = busyness.pop()
    schedule.append(schedul)

    vacs = [element.lower() for element in vacs]
    money = [element.lower() for element in money]
    exp = [element.lower() for element in exp]
    busyness = [element.lower() for element in busyness]
    schedule = [element.lower() for element in schedule]
    company = [element.lower() for element in company]
    address = [element.lower() for element in address]