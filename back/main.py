from bs4 import BeautifulSoup
import requests
import re

url = "https://hh.ru/vacancies"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"
}

page = requests.get(url, headers=headers)
# хождение по ссылкам алфавитным
soup = BeautifulSoup(page.text, "html.parser")
href = []
all_btn = soup.find_all("a", class_="bloko-button bloko-button_scale-small")
all_btn = str(all_btn)
href = re.findall(r'href="([^"]+)"', all_btn)
href = ["https://hh.ru" + direction for direction in href]

for link in href:
    # поиск кол-ва страниц
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    pg = soup.find_all("span", class_="pager-item-not-in-short-range")
    pg = str(pg)
    numbers = re.findall(r"<span>(\d+)</span>", pg)
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
        print(vacancies, count, links)