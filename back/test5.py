# Просмотр по резюме

from bs4 import BeautifulSoup
import requests

url = "https://hh.ru/resume/e0f5efba00043366c20039ed1f4a716f595561?query=автор&searchRid=171949959725677922cd63372e2465c9&hhtmFrom=resume_search_catalog"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"
}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')

vacs, exp, spec, busyness, schedule, gender, pi, busy, schedul =  [], [], [], [], [], [], [], [], []

about_gender = soup.find_all('div', class_='resume-header-title')
for div in about_gender:
    gend = div.find('span', attrs={'data-qa': 'resume-personal-gender'})
    gender.append(gend.text)

about_vacs = soup.find('h2', class_='bloko-header-2')
for h2 in about_vacs:
    vacs.append(h2.text)

about_spec = soup.find_all('li', class_='resume-block__specialization')
for div in about_spec:
    spec.append(div.text)

about_job = soup.find_all('div', class_=('resume-block-container','resume-block-container'))
for div in about_job:
    if len(div.find_all('p')) == 2: 
        about_job = div
        break
for p in about_job:
    pi.append(div.p.text)
busy = pi[:1]
busy = [element.replace('Занятость: ', '') for element in busy]
for element in busy:
    busyness.extend(element.split(', '))

p_second = about_job.find_all('p')
p_second = p_second[1]
schedul.append(p_second.text)
schedul = [element.replace('График работы: ', '') for element in schedul]
for element in schedul:
    schedule.extend(element.split(', '))

about_exp = soup.find_all('span', class_='resume-block__title-text resume-block__title-text_sub')
for span in about_exp:
    if len(span.find_all('span')) == 2: 
        about_exp = span
        break
for span in about_exp:
    exp.append(span.text)
exp = exp[1::2]
exp = [element.replace('\xa0', ' ') for element in exp]

vacs = [element.lower() for element in vacs]
exp = [element.lower() for element in exp]
spec = [element.lower() for element in spec]
busyness = [element.lower() for element in busyness]
schedule = [element.lower() for element in schedule]
gender = [element.lower() for element in gender]

print(vacs, exp, spec, busyness, schedule, gender)