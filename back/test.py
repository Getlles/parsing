from bs4 import BeautifulSoup
import requests
import re

url = "https://hh.ru/vacancies/avtor"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"
}

url = url.replace("/vacancies/", "/resumes/")

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')

# Поиск кол-ва страниц в резюме
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
    # получение данных по резюме. Названия, ссылки
    all_res = soup.find_all("span", class_="title--iPxTj4waPRTG9LgoOG4t")
    for span in all_res:
        name.append(span.a.span.text)
        href.append(span.a["href"])
name = [element.lower() for element in name]  
href = ["https://hh.ru" + direction for direction in href]

vacs, exp, spec, busyness, schedule, gender, pi, busyness, schedule = [],[],[],[],[],[],[],[],[]

for link in href:
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
        

    about_gender = soup.find_all("div", class_="resume-header-title")
    for div in about_gender:
        gend = div.find("span", attrs={"data-qa": "resume-personal-gender"})
        gender.append(gend.text)

    about_vacs = soup.find("h2", class_="bloko-header-2")
    for h2 in about_vacs:
        vacs.append(h2.text)

    about_spec = soup.find_all("li", class_="resume-block__specialization")
    for div in about_spec:
        spec.append(div.text)

    about_job = soup.find_all(
        "div", class_=("resume-block-container", "resume-block-container")
    )
    for div in about_job:
        if len(div.find_all("p")) == 2:
            about_job = div
            break
    for p in about_job:
        pi.append(div.p.text)
    busyness = pi[:1]
    busyness = [element.replace("Занятость: ", "") for element in busyness]

    p_second = about_job.find_all("p")
    p_second = p_second[1]
    schedule.append(p_second.text)
    schedule = [element.replace("График работы: ", "") for element in schedule]

    about_exp = soup.find_all(
        "span", class_="resume-block__title-text resume-block__title-text_sub"
    )
    for span in about_exp:
        if len(span.find_all("span")) == 2:
            exp.append(span.text)
            break
       
    exp = [element.replace("\xa0", " ") for element in exp]
    exp = [element.replace("Опыт работы ", "") for element in exp]

    vacs = [element.lower() for element in vacs]
    exp = [element.lower() for element in exp]
    spec = [element.lower() for element in spec]
    busyness = [element.lower() for element in busyness]
    schedule = [element.lower() for element in schedule]
    gender = [element.lower() for element in gender]
print(vacs, exp, spec, busyness, schedule, gender)