from flask import Flask, render_template, request, redirect, send_file, g
import psycopg2
import datetime as dt
from pytz import timezone
import pandas as pd
from io import BytesIO

app = Flask(__name__)

db_config = {
    'dbname': 'verceldb',
    'user': 'default',
    'password': '2TLFcSNzunj5',
    'host': 'ep-falling-cell-a183j763.ap-southeast-1.aws.neon.tech',
    'port': '5432',
    'sslmode': 'require'
}

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(**db_config)
        g.cursor = g.db.cursor()
    return g.db, g.cursor

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

    cursor = g.pop('cursor', None)
    if cursor is not None:
        cursor.close()

def create_table(name):
    _, cursor = get_db()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} (date VARCHAR(255), ref_no1 VARCHAR(255), ref_no2 SERIAL PRIMARY KEY, name VARCHAR(255), rollno VARCHAR(255), branch VARCHAR(255), phone VARCHAR(255), email VARCHAR(255), compname VARCHAR(255), comploc VARCHAR(255), pocname VARCHAR(255), pocphone VARCHAR(255))")
    g.db.commit()

def export_to_excel(table_name):
    data = get_table_entries(table_name)
    df = pd.DataFrame(data)
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)
    return excel_file

def get_table_entries(table_name):
    _, cursor = get_db()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    return data

@app.route('/')
def index():
    author = "Aditya"
    return render_template('home.html', author=author)

@app.route('/nocdata/')
def nocdata():
    _, cursor = get_db()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = [table[0] for table in cursor.fetchall()]
    return render_template('table.html', tables=tables)

@app.route('/nocdata/', methods=['POST'])
def display_table_entries():
    _, cursor = get_db()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = [table[0] for table in cursor.fetchall()]
    table_name = request.form.get('table_selector')
    try:
        data = get_table_entries(table_name)
        return render_template('table.html', data=data, table_name=table_name, tables=tables)
    except:
        return render_template('table.html', tables=tables)

@app.route('/export/<table_name>', methods=['GET', 'POST'])
def export_to_excel_route(table_name):
    excel_file = export_to_excel(table_name)
    return send_file(excel_file, as_attachment=True, download_name=f'{table_name}_data.xlsx')

@app.route('/register/', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        name = request.form['name']
        rollno = request.form['rollno']
        branch = request.form['branch']
        sender_mail = 'lexluke007@gmail.com'
        receivers_mail = "adityasaini2004@gmail.com"
        message = f"""From: {sender_mail}\nTo: {receivers_mail}\nSubject: New Application for Registration\n\nThis is a test e-mail message."""
        return render_template('confirmation.html', name=name, message="Your Registration for Eighth Semester is Submitted!")
    return render_template('register.html')

@app.route('/noc/', methods=['GET', 'POST'])
def nocreq():
    if request.method == 'POST':
        title = request.form['title']
        name = request.form['name']
        rollno = request.form['rollno']
        branch = request.form['branch']
        phone = request.form['phone']
        email = request.form['email']
        compname = request.form['companyname']
        comploc = request.form['companyloc']
        pocname = request.form['pocname']
        pocphone = request.form['pocphone']
        date = dt.datetime.now(timezone('UTC')).astimezone(timezone('Asia/Kolkata')).strftime("%B %d, %Y")
        ref_no1 = dt.datetime.now(timezone('UTC')).astimezone(timezone('Asia/Kolkata')).strftime("%Y_%d")
        branch_sel = {'bece': 'BE_ECE', 'benc': 'BE_ENC', 'bvlsi': 'BE_VLSI', 'mece': 'ME_ECE', 'mvlsi': 'ME_VLSI',
                      'others': 'Others'}
        faculty = branch_sel[branch]
        certificate = "NOC_" + str(rollno)
        create_table(faculty)
        _, cursor = get_db()
        query = f"INSERT INTO {faculty} (date, ref_no1, name, rollno, branch, phone, email, compname, comploc, pocname, pocphone) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        values = (date, ref_no1, name, rollno, faculty, phone, email, compname, comploc, pocname, pocphone)
        cursor.execute(query, values)
        g.db.commit()
        export_to_excel(faculty)
        sender_mail = 'lexluke007@gmail.com'
        receivers_mail = "adityasaini2004@gmail.com"
        message = f"""From: {sender_mail}\nTo: {receivers_mail}\nSubject: New NOC Application\n\nThis is a test e-mail message."""
        return render_template('confirmation.html', name=name, message="Your NOC Application has been submitted!")
    return render_template("noc.html")

if __name__ == '__main__':
    app.run(debug=True)
