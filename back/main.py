from bs4 import BeautifulSoup
import requests
import re
import mysql.connector

# Подключение дб
db = mysql.connector.connect(user='root', password='root', host='localhost', database='hh')
cursor = db.cursor()

delete_tables_query = """
use hh;
drop table if exists info_vacancies, vacancies, info_resumes, resumes
"""

create_prof_table_query = """
CREATE TABLE IF NOT EXISTS prof (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    job VARCHAR(10000),
    counter INT,
    address VARCHAR(10000)
)
"""

create_vacancies_table_query = """
CREATE TABLE IF NOT EXISTS vacancies (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name VARCHAR(1000),
    href VARCHAR(500)
)
"""

create_info_vacancies_table_query = """
CREATE TABLE IF NOT EXISTS info_vacancies (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    vacs VARCHAR(1000),
    money VARCHAR(1000),
    exp VARCHAR(1000),
    busyness VARCHAR(1000),
    schedule VARCHAR(1000),
    company VARCHAR(1000),
    address VARCHAR(1000)
)
"""

create_resumes_table_query = """
CREATE TABLE IF NOT EXISTS resumes (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name VARCHAR(1000),
    href VARCHAR(500)
)
"""

create_info_resumes_table_query = """
CREATE TABLE IF NOT EXISTS info_resumes (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    vacs VARCHAR(1000),
    spec VARCHAR(1000),
    exp VARCHAR(1000),
    busyness VARCHAR(1000),
    schedule VARCHAR(1000),
    gender VARCHAR(1000)
)
"""

insert_prof_query = """
    INSERT INTO prof 
    (job, counter, address)
    VALUES ( %s, %s, %s )
"""

insert_vacancies_table_query = """
    INSERT INTO vacancies 
    (name, href)
    VALUES ( %s, %s )
"""

insert_info_vacancies_table_query = """
    INSERT INTO info_vacancies
    (vacs, money, exp, busyness, schedule, company, address)
    VALUES ( %s, %s, %s, %s, %s, %s, %s )
"""

insert_resumes_table_query = """
    INSERT INTO resumes 
    (name, href)
    VALUES ( %s, %s )
"""

insert_info_resumes_table_query = """
    INSERT INTO info_resumes 
    (vacs, spec, exp, busyness, schedule, gender)
    VALUES ( %s, %s, %s, %s, %s, %s )
"""

# Работа с парсингом
url = "https://hh.ru/vacancies"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"
}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, "html.parser")
# хождение по алфавитным ссылкам
href = []
all_btn = soup.find_all("a", class_="bloko-button bloko-button_scale-small")
all_btn = str(all_btn)
href = re.findall(r'href="([^"]+)"', all_btn)
href = ["https://hh.ru" + direction for direction in href]

job, counter, address = [], [], []
for link in href:
    # поиск кол-ва страниц
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    page = soup.find_all("span", class_="pager-item-not-in-short-range")
    page = str(page)
    numbers = re.findall(r"<span>(\d+)</span>", page)
    numbers = list(map(int, numbers))
    if numbers != []:
        num = max(numbers)
    else:
        num = 1

    # список вакансий, их число, ссылки на них
    for pages in range(num):
        vacancies, count, links = [], [], []
        name = soup.find_all("div", class_="catalog-link--JuoRNlNG2ovifEc18ShQ")
        for div in name:
            vacancies.append(div.a.text)
            count_span = div.find("span", class_="bloko-text_tertiary")
            count.append(div.span.text if count_span else "0")
            links.append(div.a["href"])
        links = ["https://hh.ru" + direction for direction in links]
        address.extend(links)
    job.extend(vacancies)
    counter.extend(count)
    address.extend(links)
counter = [element.split("\xa0")[0] for element in counter]
res = list(zip(job, counter, address))

# поиск вакансий и резюме на необходимую должность
user_input = str(input("Введите вашу профессию: ")).lower()
if user_input in job:
    index = job.index(user_input)
    url = address[index]
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")

    user_input = str(input("Вы ищите вакансии? ")).lower()

    if user_input == "да":

        # Поиск кол-ва страниц в вакансиях
        page = soup.find_all("span", class_="pager-item-not-in-short-range")
        page = str(page)
        numbers = re.findall(r"<span>(\d+)</span>", page)
        numbers = list(map(int, numbers))
        if numbers != []:
            num = max(numbers)
        else:
            num = 1

        if num > 30:
            num = 30  # ограничение от всяких 250+ страниц

        href, name, index = [], [], []
        i = 0
        for pages in range(num):
            # получение данных по вакансиям. Названия, ссылки
            all_vac = soup.find_all("h2", class_="bloko-header-section-2")
            for h2 in all_vac:
                name.append(h2.span.a.span.text)
                href.append(h2.span.a["href"])
                index.append(str(i))
                i += 1      
        name = [element.lower() for element in name]
        res_vac = list(zip(name, href))
        res_res, result_res = [], []
        
        # Инфо о вакансии
        user_input = input("Введите вакансию: ").lower()
        if user_input in index:
            index = index.index(user_input)
            url = href[index]

            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.text, "html.parser")

            vacs, money, exp, busy, company, address, busyness, schedule = (
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
            )

            about_job = soup.find_all(
                "div",
                class_=(
                    "wrapper-flat--H4DVL_qLjKLCo1sytcNI",
                    "backplate-module_content-wrapper-flatten-on-xs__Jb8w0",
                ),
            )
            for div in about_job:
                vacs.append(div.h1.text)
                money.append(div.div.span.text)
                exp.append(div.p.text)
                second_p = div.find(
                    "p", attrs={"data-qa": "vacancy-view-employment-mode"}
                )
                busy.append(second_p.text)

            about_company = soup.find_all("div", class_=("vacancy-company-redesigned"))
            for div in about_company:
                second_div = div.find(
                    "div", attrs={"data-qa": "vacancy-company__details"}
                )
                company.append(second_div.text)
                address.append(div.find_all("div")[-1].text)
            company.pop(-1)
            address.pop(-1)

            vacs = [element.replace("\xa0", " ") for element in vacs]
            money = [element.replace("\xa0", " ") for element in money]
            exp = [element.replace("\xa0", " ") for element in exp]
            busy = [element.replace("\xa0", " ") for element in busy]
            for element in busy:
                busyness.extend(element.split(", "))
            company = [element.replace("\xa0", " ") for element in company]
            address = [element.replace("\xa0", " ") for element in address]
            schedul = busyness.pop()
            schedule.append(schedul)

            vacs = [element.lower() for element in vacs]
            money = [element.lower() for element in money]
            exp = [element.lower() for element in exp]
            busyness = [element.lower() for element in busyness]
            schedule = [element.lower() for element in schedule]
            company = [element.lower() for element in company]
            address = [element.lower() for element in address]
            result_vac = list(zip(vacs, money, exp, busyness, schedule, company, address))
        else:
            print("error: Иди проспись")

    else:
        url = url.replace("/vacancies/", "/resumes/")

        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")

        # Поиск кол-ва страниц в резюме
        page = soup.find_all("span", class_="pager-item-not-in-short-range")
        page = str(page)
        numbers = re.findall(r"<span>(\d+)</span>", page)
        numbers = list(map(int, numbers))
        if numbers != []:
            num = max(numbers)
        else:
            num = 1

        if num > 30:
            num = 30  # ограничение от всяких 250+ страниц

        href, name, index = [], [], []
        i = 0
        for pages in range(num):
            # получение данных по резюме. Названия, ссылки
            all_res = soup.find_all("span", class_="title--iPxTj4waPRTG9LgoOG4t")
            for span in all_res:
                name.append(span.a.span.text)
                href.append(span.a["href"])
                index.append(str(i))
                i += 1
        name = [element.lower() for element in name]
        href = ["https://hh.ru" + direction for direction in href]
        res_res = list(zip(name, href))
        res_vac, result_vac = [], []

        # Инфо о резюме
        user_input = input("Введите индекс резюме: ").lower()
        if user_input in index:
            url = href[index]

            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.text, "html.parser")

            vacs, exp, spec, busyness, schedule, gender, pi, busy, schedul = (
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
            )

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
            busy = pi[:1]
            busy = [element.replace("Занятость: ", "") for element in busy]
            for element in busy:
                busyness.extend(element.split(", "))

            p_second = about_job.find_all("p")
            p_second = p_second[1]
            schedul.append(p_second.text)
            schedul = [element.replace("График работы: ", "") for element in schedul]
            for element in schedul:
                schedule.extend(element.split(", "))

            about_exp = soup.find_all(
                "span", class_="resume-block__title-text resume-block__title-text_sub"
            )
            for span in about_exp:
                if len(span.find_all("span")) == 2:
                    about_exp = span
                    break
            for span in about_exp:
                exp.append(span.text)
            exp = exp[1::2]
            exp = [element.replace("\xa0", " ") for element in exp]

            vacs = [element.lower() for element in vacs]
            exp = [element.lower() for element in exp]
            spec = [element.lower() for element in spec]
            busyness = [element.lower() for element in busyness]
            schedule = [element.lower() for element in schedule]
            gender = [element.lower() for element in gender]
            result_res = list(zip(vacs, exp, spec, busyness, schedule, gender))
        else:
            print("error: Иди проспись")

cursor.execute(create_prof_table_query)
cursor.execute(create_vacancies_table_query)
cursor.execute(create_info_vacancies_table_query)
cursor.execute(create_resumes_table_query)
cursor.execute(create_info_resumes_table_query)

cursor.executemany(insert_prof_query, res)
cursor.executemany(insert_vacancies_table_query, res_vac)
cursor.executemany(insert_info_vacancies_table_query, result_vac)
cursor.executemany(insert_resumes_table_query, res_res)
cursor.executemany(insert_info_resumes_table_query, result_res)
db.commit()

db.close()