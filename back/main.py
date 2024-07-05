from bs4 import BeautifulSoup
import requests
import re
import mysql.connector
from flask import Flask

# работа с Flask
app = Flask(__name__, template_folder='/app/front', static_folder='/app/front')



# Подключение дб
db = mysql.connector.connect(user='root', password='root', host='localhost', database='hh')
cursor = db.cursor()

drop_vacancies_table_query = "DROP TABLE IF EXISTS vacancies;"
drop_resumes_table_query = "DROP TABLE IF EXISTS resumes;"
cursor.execute(drop_vacancies_table_query)
cursor.execute(drop_resumes_table_query)
db.commit()

create_prof_table_query = """
CREATE TABLE IF NOT EXISTS prof (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    job VARCHAR(100),
    counter INT,
    address VARCHAR(100)
);
"""

create_vacancies_table_query = """
CREATE TABLE IF NOT EXISTS vacancies (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    vacs VARCHAR(100),
    money VARCHAR(100),
    exp VARCHAR(100),
    busyness VARCHAR(100),
    schedule VARCHAR(100),
    company VARCHAR(100),
    address VARCHAR(100)
);
"""

create_resumes_table_query = """
CREATE TABLE IF NOT EXISTS resumes (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    vacs VARCHAR(100),
    spec VARCHAR(100),
    exp VARCHAR(100),
    busyness VARCHAR(100),
    schedule VARCHAR(100),
    gender VARCHAR(100)
);
"""

insert_prof_query = """
    INSERT INTO prof 
    (job, counter, address)
    VALUES ( %s, %s, %s );
"""

insert_vacancies_table_query = """
    INSERT INTO vacancies
    (vacs, money, exp, busyness, schedule, company, address)
    VALUES ( %s, %s, %s, %s, %s, %s, %s );
"""

insert_resumes_table_query = """
    INSERT INTO resumes 
    (vacs, spec, exp, busyness, schedule, gender)
    VALUES ( %s, %s, %s, %s, %s, %s );
"""

# проверка наличия данных в таблице для скипа списка профессий
check_data_query = f"SELECT COUNT(*) FROM prof"
cursor.execute(check_data_query)
result = cursor.fetchone()[0]

# Работа с парсингом
url = "https://hh.ru/vacancies"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"
}

if result == 0:
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

input_query = "SELECT * FROM prof WHERE job = %s"
cursor.execute(input_query, (user_input,))
result = cursor.fetchall()

if result:
    url = result[0][3]

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
        if num > 2: num=2 #ограничение от всяких 250+ страниц. Такое малое число для чуть более быстрой загрузки.

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
            result_vac = list(zip(vacs, money, exp, busyness, schedule, company, address))
            result_res = []

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
        if num > 2: num=2 #ограничение от всяких 250+ страниц

        href, name = [], []
        for pages in range(num):
            # получение данных по резюме. Названия, ссылки
            all_res = soup.find_all("span", class_="title--iPxTj4waPRTG9LgoOG4t")
            for span in all_res:
                name.append(span.a.span.text.lower())
                href.append("https://hh.ru" + span.a["href"])

            vacs, exp, spec, busyness, schedule, gender = [], [], [], [], [], []

            for link in href:
                page = requests.get(link, headers=headers)
                soup = BeautifulSoup(page.text, "html.parser")

                about_gender = soup.find_all("div", class_="resume-header-title")
                for div in about_gender:
                    gend = div.find("span", attrs={"data-qa": "resume-personal-gender"})
                    gender.append(gend.text.lower())

                about_vacs = soup.find("h2", class_="bloko-header-2")
                vacs.append(about_vacs.text.lower())

                about_spec = soup.find_all("li", class_="resume-block__specialization")
                for div in about_spec:
                    spec.append(div.text.lower())

                about_job = soup.find_all("div", class_=("resume-block-container", "resume-block-container"))
                for div in about_job:
                    if len(div.find_all("p")) == 2:
                        about_job = div
                        break
                for p in about_job.find_all("p"):
                    pi = div.p.text.lower().replace('занятость: ', '').replace('\xa0', ' ')
                    busyness.append(pi)

                p_second = about_job.find_all("p")[1]
                schedule.append(p_second.text.lower().replace("график работы: ", "").replace('\xa0', ' '))

                about_exp = soup.find_all("span", class_="resume-block__title-text resume-block__title-text_sub")
                for span in about_exp:
                    if len(span.find_all("span")) == 2:
                        exp.append(span.text.lower().replace("\xa0", " ").replace("опыт работы ", ""))
                        break

            result_res = list(zip(vacs, spec, exp, busyness, schedule, gender))
            result_vac = []

cursor.execute(create_prof_table_query)
cursor.execute(create_vacancies_table_query)
cursor.execute(create_resumes_table_query)

cursor.executemany(insert_prof_query, res)
cursor.executemany(insert_vacancies_table_query, result_vac)
cursor.executemany(insert_resumes_table_query, result_res)
db.commit()

db.close()