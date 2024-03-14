from flask import Flask, render_template, request, redirect, send_file, g
import mysql.connector
import datetime as dt
from pytz import timezone
import pandas as pd
from io import BytesIO

app = Flask(__name__)

'''db_config = {
    'user': 'lexluke007',
    'password': 'dbpass123',
    'host': 'lexluke007.mysql.pythonanywhere-services.com',
    'database': 'lexluke007$test3'
}'''

db_config = {
    'dbname': 'verceldb',
    'user': 'default',
    'password': '2TLFcSNzunj5',
    'host': 'ep-falling-cell-a183j763.ap-southeast-1.aws.neon.tech',
    'port': '5432',
    'sslmode': 'require'
}


con = mysql.connector.connect(**db_config)
cursor = con.cursor(dictionary=True)

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(**db_config)
        g.cursor = g.db.cursor(dictionary=True)
    return g.db, g.cursor

def close_db(e=None):
    cursor = g.pop('cursor', None)
    if cursor is not None:
        cursor.close()

    db = g.pop('db', None)
    if db is not None:
        db.close()

def create_table(name):
    create_table_query = f"CREATE TABLE IF NOT EXISTS {name} (date VARCHAR(255), ref_no1 VARCHAR(255), ref_no2 INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), rollno VARCHAR(255), branch VARCHAR(255), phone VARCHAR(255), email VARCHAR(255), compname VARCHAR(255), comploc VARCHAR(255), pocname VARCHAR(255), pocphone VARCHAR(255))"
    cursor.execute(create_table_query)
    con.commit()

def export_to_excel(table_name):
    data = get_table_entries(table_name)
    df = pd.DataFrame(data)
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)
    return excel_file

def send_email(subject, sender, receiver, message):
    # email sending code here
    pass

def get_table_entries(table_name):
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    data = cursor.fetchall()
    return data

@app.route('/')
def index():
    author = "Aditya"
    return render_template('home.html', author=author)

@app.route('/nocdata/')
def nocdata():
    g.db, g.cursor = get_db()
    cursor.execute("SHOW TABLES")
    tables = [table['Tables_in_lexluke007$test3'] for table in cursor.fetchall()]
    return render_template('table.html', tables=tables)

@app.route('/nocdata/', methods=['POST'])
def display_table_entries():
    cursor.execute("SHOW TABLES")
    tables = [table['Tables_in_lexluke007$test3'] for table in cursor.fetchall()]
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
        # email handling code here
        sender_mail = 'lexluke007@gmail.com'
        receivers_mail = "adityasaini2004@gmail.com"  # for (user in users_db.values() if user.id == faculty[branch])
        message = f"""From: {sender_mail}\nTo: {receivers_mail}\nSubject: New Application for Registration\n\nThis is a test e-mail message."""
        send_email("New Application for Registration", sender_mail, receivers_mail, message)
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
        branch_name = {'bece': 'Electronics and Communication Engineering', 'benc': 'Electronics and Computer Engineering',
                       'bvlsi': 'Electronics Engineering (VLSI Design and Technology)'}
        create_table(faculty)
        query = f"INSERT INTO {faculty} (date, ref_no1, name, rollno, branch, phone, email, compname, comploc, pocname, pocphone) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        values = (date, ref_no1, name, rollno, faculty, phone, email, compname, comploc, pocname, pocphone)
        cursor.execute(query, values)
        con.commit()
        export_to_excel(faculty)
        sender_mail = 'lexluke007@gmail.com'
        receivers_mail = "adityasaini2004@gmail.com"  # for (user in users_db.values() if user.id == faculty[branch])
        message = f"""From: {sender_mail}\nTo: {receivers_mail}\nSubject: New NOC Application\n\nThis is a test e-mail message."""
        return render_template('confirmation.html', name=name, message="Your NOC Application has been submitted!")
    return render_template("noc.html")

if __name__ == '__main__':
    app.run(debug=True)
