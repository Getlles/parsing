from bs4 import BeautifulSoup
import requests
import re
import mysql.connector

def search_vacancies_func(user_input: str):
    # Подключение дб
    db = mysql.connector.connect(user='root', password='root', host='localhost', database='hh')
    cursor = db.cursor()

    # удаление старых таблиц
    drop_vacancies_table_query = "DROP TABLE IF EXISTS vacancies;"
    cursor.execute(drop_vacancies_table_query)
    db.commit()

    create_prof_table_query = """
    CREATE TABLE IF NOT EXISTS prof (
        id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
        job VARCHAR(100),
        counter INT,
        address VARCHAR(255)
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
        address VARCHAR(255)
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

    # # проверка наличия данных в таблице для скипа списка профессий
    # check_data_query = f"SELECT COUNT(*) FROM prof"
    # cursor.execute(check_data_query)
    # result = cursor.fetchone()[0]

    # Работа с парсингом
    url = "https://hh.ru/vacancies"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"
    }

    # if result == 0:
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    # хождение по алфавитным ссылкам
    href = []
    all_btn = soup.find_all("a", class_="bloko-button bloko-button_scale-small")
    all_btn = str(all_btn)
    href = re.findall(r'href="([^"]+)"', all_btn)
    href = ["https://hh.ru" + direction for direction in href]

    li = []
    job, counter, address = [], [], []
    for link in href:
        li.append(link)
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
            li.append(link)
        
    
    vacancies, count, links = [], [], []
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    name = soup.find_all("div", class_="catalog-link--JuoRNlNG2ovifEc18ShQ")
    print(name)
    vacancies.append(name.find('a').text)
    count_span = name.find("span", class_="bloko-text_tertiary")
    count.append(count_span.text if count_span else "0")
    links.append(name.find('a').href)
    links = ["https://hh.ru" + direction for direction in links]
    print(vacancies, count, links)
    # for div in name:
    #     vacancies.append(div.a.text)
    #     count_span = div.find("span", class_="bloko-text_tertiary")
    #     count.append(div.span.text if count_span else "0")
    #     links.append(div.a["href"])
    # links = ["https://hh.ru" + direction for direction in links]
    

            
    job.append(vacancies)
    counter.append(count)
    address.append(links)
    # print(address)
        
    counter = [element.split("\xa0")[0] for element in counter]
    res = list(zip(job, counter, address))
    # print(job,counter,link)
    input_query = "SELECT * FROM prof WHERE job = %s"
    cursor.execute(input_query, (user_input,))
    result = cursor.fetchall()

    if result:
        url = result[0][3]

        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")

        user_input = user_input.lower()

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
            if company and address != []:
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

    cursor.execute(create_prof_table_query)
    cursor.execute(create_vacancies_table_query)

    cursor.executemany(insert_prof_query, res)
    cursor.executemany(insert_vacancies_table_query, result_vac)

    db.commit()

    db.close()
    # return result_vac
