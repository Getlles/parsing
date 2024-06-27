from bs4 import BeautifulSoup
import requests
import webbrowser

links = ['https://www.example1.com', 'https://www.example2.com', 'https://www.example3.com']

user_input = int(input('Введите номер ссылки для открытия: '))

if user_input > 0 and user_input <= len(links):
    url = links[user_input - 1]  # выбор ссылки из массива по номеру
    response = requests.get(url)  # получение содержимого страницы
    soup = BeautifulSoup(response.content, 'html.parser')
    webbrowser.open(url)
else:
    print('Введенный номер недействителен')