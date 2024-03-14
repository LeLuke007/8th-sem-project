from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import csv, http.client, datetime as dt
from smtplib import SMTP
import smtplib
import pandas as pd

app = Flask(__name__)

token='yJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhMjY3NWNjOGUzZDkwZmZlM2VkMWZlMzI4M2VmZWEwZjIyMzk1NmQyNjQxZDNmY2MwMDliNGRlZGFlZGM1Yjc2Iiwic3ViIjoieXV2cmFqZzI0MTlAZ21haWwuY29tIiwiZXhwIjoxNzEwMDAxMDkwfQ.rCub74THCMUtkfvlfOnmLY2KH2pvD5sauqJHMYnnm2c'

@app.route('/')
@app.route('/<name>/')
def index(name=None):
    author = "Aditya"
    return render_template('home.html', author=author, name=name)

@app.route('/register/', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        name = request.form['name']
        rollno = request.form['rollno']
        branch = request.form['branch']
        faculty={'bece':'1','benc':'2','bvlsi':'3','mece':'4','mvlsi':'5','others':'6'}
        # EMAIL Using SMTP Work to do
        '''receivers_mail = "adityasaini2004@gmail.com" #for (user in users_db.values() if user.id == faculty[branch])
        sender_mail = 'lexluke007@gmail.com'
        message="""From: From Person %s  
        To: To Person %s  
        Subject: New Application for Registration   
        This is a test e-mail message.  
        """%(sender_mail,receivers_mail)

        smtpObj = smtplib.SMTP("gmail.com", 587)
        smtpObj.sendmail(sender_mail, receivers_mail, message) '''
        return render_template('confirmation.html', name=name, message ="Your Registration for Eighth Semester is Submitted!")
    return render_template('register.html')

@app.route('/noc/', methods=['GET', 'POST'])
def nocreq():
    if request.method== 'POST':
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
        date = dt.datetime.now().strftime("%B %d, %Y")
        ref_no1 = dt.datetime.now().strftime("%Y_%d")
        branch_sel = {'bece':'ECE', 'benc':'ENC','bvlsi':'VLSI'}
        certificate = "NOC_"+str(rollno)
        branch_name={'bece':'Electronics and Communication Engineering','benc':'Electronics and Computer Engineering','bvlsi':'Electronics Engineering (VLSI Design and Technology)'}
        header = ['Ref No1','Ref No2','Student Name','Roll Number','Branch','Phone No.','Student Email','Company Name','Company Location','POC Name','POC Contact']
        faculty={'bece':'1','benc':'2','bvlsi':'3','mece':'4','mvlsi':'5','others':'6'}
        file=str(faculty[branch])+".csv"
        
        ref_no2 = 0
        with open(file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            if not rows or (len(rows) == 1 and rows[0] == header):
                ref_no2 = 0
                with open(file, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(header)
            elif rows:
                ref_no2 = int(rows[-1][1]) + 1

        fields = [[ref_no1,ref_no2,name,rollno,branch_sel[branch],phone,email,compname,comploc,pocname,pocphone]]
        
        with open(file, 'a',newline='') as csvfile:
            writer = csv.writer(csvfile)
            if csvfile.tell() == 0:
                writer.writerow(header)
            writer.writerows(fields)
        
        conn = http.client.HTTPSConnection("us1.pdfgeneratorapi.com")
        headers = {
        'Content-Type': "application/json"
        }
        payload = '{"template": {"id":"982526", "data": {"title": "%s", "name": "%s", "date": "%s", "branch": "%s", "roll_no": "%s", "branch_name": "%s", "ref_no1": "%s", "ref_no2": "%s" }}, "format": "pdf", "output": "url", "name": "%s"}' % (title, name, date, branch_sel[branch], rollno, branch_name[branch], ref_no1,ref_no2,certificate)
        conn.request("POST", "/api/v4/documents/generate", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data)
        if res.status == 200 and res.getheader('Content-Type') == 'application\\/pdf':
            with open("certificate.pdf", "wb") as pdf_file:
                pdf_file.write(data)
        return render_template('confirmation.html', name=name, message="Your NOC Application has been submitted!")
    return render_template("noc.html")

if __name__ == '__main__':
    app.run(debug=True)

'''
def export_to_excel(name):
    query = f'SELECT * FROM {name}'
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    excel_file_path = f'/home/lexluke007/mysite/{name}.xlsx'
    df.to_excel(excel_file_path, index=False)
    return f'Data exported to {excel_file_path}'
'''

'''app.secret_key = 'your_secret_key'  # Change this to your secret key
login_manager = LoginManager(app)
login_manager.login_view = 'login'
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key='245274832340-9fiea5l7s5shvusl7nbu5g2dithn85sj.apps.googleusercontent.com',  # Replace with your Google API client ID
    consumer_secret='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',  # Replace with your Google API client secret
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        flash('Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        ))
        return redirect(url_for('index'))

    user_info = google.get('userinfo')
    user_email = user_info.data['email']

    if not user_email.endswith('@thapar.edu'):
        flash('Access denied: Only organization users are allowed.')
        return redirect(url_for('index'))

    session['access_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    user = User()
    user.id = user_info.data['id']
    login_user(user)
    return redirect(url_for('index'))
'''