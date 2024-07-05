import mysql.connector

# Подключение дб
db = mysql.connector.connect(user='root', password='root', host='localhost', database='he')
cursor = db.cursor()

# delete_tables_query = """
# use hh;
# drop table if exists vacancies, resumes;
# """
# cursor.execute(delete_tables_query)

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


res = [('1', '2', '3'), ('1', '2', '3'), ('1', '2', '3')]
result_vac = [('1', '2', '3', '4', '5', '6', '7'), ('1', '2', '3', '4', '5', '6', '7')]
result_res = [('1', '2', '3', '4', '5', '6'), ('1', '2', '3', '4', '5', '6'), ('1', '2', '3', '4', '5', '6')]

# cursor.execute(delete_tables_query)
# cursor.fetchall()
cursor.execute(create_prof_table_query)
cursor.execute(create_vacancies_table_query)
cursor.execute(create_resumes_table_query)
# cursor.nextset()

cursor.executemany(insert_prof_query, res)
cursor.executemany(insert_vacancies_table_query, result_vac)
cursor.executemany(insert_resumes_table_query, result_res)
db.commit()

drop_vacancies_table_query = "DROP TABLE IF EXISTS vacancies;"
drop_resumes_table_query = "DROP TABLE IF EXISTS resumes;"
cursor.execute(drop_vacancies_table_query)
cursor.execute(drop_resumes_table_query)
db.commit()

db.close()