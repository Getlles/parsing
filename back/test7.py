href = ['https://www.example1.com', 'https://www.example2.com', 'https://www.example3.com']
name = ['Автор студенческих работ по Педагогике', 'Автор студенческих работ по педагогике/психологии', 'Автор студенческих работ по Техническим предметам']
user_input = input('Введите вакансию: ').lower()
if user_input in name:
    index = name.index(user_input)
    url = href[index]
    print(url)
else: print('no') 