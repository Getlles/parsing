from flask import Flask, render_template, request
from src.db.resumes import search_resumes_func
from src.db.vacanceis import search_vacancies_func
import os
from flask_mysqldb import MySQL

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

template_dir = os.path.join(base_dir, 'src', 'front')
static_dir = os.path.join(base_dir, 'src', 'front')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'hh'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('user_input', '').lower()
        search_vacancies_func(user_input)
        search_resumes_func(user_input)
    else:
        print("GET")        
    return render_template('index.html')

@app.route('/allvac', methods=['GET', 'POST'])
def vacancies():
    cursor = mysql.connection.cursor()
    cursor.execute('select * from vacancies')
    vacancie = cursor.fetchall()
    if request.method == 'POST':
        method_sql = request.form.get('btn__exp')
        if method_sql == 'не имеет значения':
            cursor.execute('select * from vacancies')
            vacancie = cursor.fetchall()
        else:
            cursor.execute(f"select * from hh.vacancies where exp = '{method_sql}'")
            vacancie = cursor.fetchall()
    return render_template('vacancies.html', vacancie=vacancie)

@app.route('/allres', methods=['GET', 'POST'])
def resumes():
    cursor = mysql.connection.cursor()
    cursor.execute('select * from resumes')
    resume = cursor.fetchall()
    if request.method == 'POST':
        method_sql = request.form.get('btn__gen')
        if method_sql == 'не имеет значения':
            cursor.execute('select * from resumes')
            resume = cursor.fetchall()
        else:
            cursor.execute(f"select * from hh.resumes where gender = '{method_sql}'")
            resume = cursor.fetchall()
    return render_template('resumes.html', resume=resume)

if __name__ == "__main__":
    app.run(debug=True, port=5000)