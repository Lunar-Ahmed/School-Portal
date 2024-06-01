from flask import Flask, render_template, redirect, request, url_for, session, send_file
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime
import re
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

app.secret_key = 'HiddenKey'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'school'

mysql = MySQL(app)

# page routes CODE START

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        return redirect(url_for('result'))
    return render_template('result.html')

@app.route('/student_dashboard', methods=['GET', 'POST'])
def student_dashboard():
    if request.method == 'POST':
        return redirect(url_for('student_dashboard'))
    return render_template('studentboard.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/assignment', methods=['GET', 'POST'])
def assignment():
    if request.method == 'POST':
        return redirect(url_for('assignment.html'))
    return render_template('assignment.html')

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reg")
    data = cur.fetchall()
    cur.close()
    return render_template('attendance.html', data=data)

@app.route('/bursar', methods=['GET', 'POST'])
def bursar():
    if request.method == 'POST':
        return redirect(url_for('bursar.html'))
    return render_template('bursar.html')
     
#Form routes
 
@app.route('/register/admin', methods=['GET', 'POST'])
def admin_register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO reg VALUES (NULL, %s, %s, %s)', (username, password, email))
        mysql.connection.commit()
        msg = 'You have successfully registered!'
        return render_template('login.html', msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('adminboard.html', msg=msg)

@app.route('/register', methods=['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST'  and 'firstname' in request.form and 'lastname' in request.form and 'middlename' in request.form and 'addnumber' in request.form  and 'state' in request.form and 'country' in request.form and 'lga' in request.form and 'address' in request.form and 'dob' in request.form and 'email' in request.form and 'guardian' in request.form and 'password' in request.form  and 'dropdown' in request.form:
        firstname = request.form['firstname']
        lastname= request.form['lastname']
        middlename = request.form['middlename']
        addnumber = request.form['addnumber']
        state = request.form['state']
        country = request.form['country']
        lga = request.form['lga']
        address = request.form['address']
        dob = request.form['dob']
        email = request.form['email']
        guardian = request.form['guardian']
        password = request.form['password']
        dropdown = request.form['dropdown']
        cursor = mysql.connection.cursor()
        if dropdown == 'school1':
            cursor.execute('INSERT INTO std1 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (firstname, lastname, middlename, addnumber,state, country, lga, address, dob, email, guardian, password))
        elif dropdown == 'school2':
            cursor.execute('INSERT INTO std2 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (firstname, lastname, middlename, addnumber,state, country, lga, address, dob, email, guardian, password))
        elif dropdown == 'school3':
            cursor.execute('INSERT INTO std3 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (firstname, lastname, middlename, addnumber,state, country, lga, address, dob, email, guardian, password))
        elif dropdown == 'school4':
            cursor.execute('INSERT INTO std4 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (firstname, lastname, middlename, addnumber,state, country, lga, address, dob, email, guardian, password))
        elif dropdown == 'school5':
            cursor.execute('INSERT INTO std5 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (firstname, lastname, middlename, addnumber,state, country, lga, address, dob, email, guardian, password))
        elif dropdown == 'school6':
            cursor.execute('INSERT INTO std6 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (firstname, lastname, middlename, addnumber,state, country, lga, address, dob, email, guardian, password))
        mysql.connection.commit()
        msg = 'You have successfully registered!'
        return render_template('user_reg.html', msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('user_reg.html', msg=msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM reg WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['Id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('contact.html', msg = 'username')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)


@app.route('/register/user', methods=['GET', 'POST'])
def user_register():
    msg = ''
    if request.method == 'POST' and 'student' in request.form and 'parent' in request.form and 'former' in request.form and 'address' in request.form :
        student = request.form['student']
        parent = request.form['parent']
        former = request.form['former']
        address = request.form['address']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO enrol VALUES (NULL, %s, %s, %s, %s, %s)', (student, parent, former, address, datetime.now()))
        mysql.connection.commit()
        msg = 'You have successfully registered!'
        return render_template('login.html', msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('user_register.html', msg=msg)

# ------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('home'))

# -------------------------------------------------

@app.route('/')
@app.route('/admin')
def admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reg")
    data = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM reg")
    admin_count = cur.fetchone()[0]
    cur.close()
    return render_template('adminboard.html', data=data, admin_count=admin_count)

@app.route('/teacher')
def teacher():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM reg")
    data = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM reg")
    teacher_count = cur.fetchone()[0]
    cur.close()
    return render_template('teacher.html', data=data, teacher_count=teacher_count)

@app.route('/student')
def student():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reg")
    data = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM reg")
    student_count = cur.fetchone()[0]
    cur.close()
    return render_template('student.html', data=data, student_count=student_count)


@app.route('/view/<int:id>')
def view(id):
    return f'Viewing row  with ID {id}'

@app.route('/modify/<int:id>')
def modify(id):
    return f'Modifying row  with ID {id}'

@app.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html',)

# ---DASHBOARDS LOGN ROUTES
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    msg = ''
    if request.method == 'POST' and 'pry'+'username' in request.form and 'password' in request.form:
        username = request.form['username']
        modified_username = 'pry'+ username
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM reg WHERE username = % s AND password = % s', (modified_username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['Id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('studentboard.html', msg = 'username')
        else:
            msg = 'Incorrect username / password !'
    return render_template('user_login.html', msg = msg)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM reg WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['Id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('adminboard.html', msg = 'username')
        else:
            msg = 'Incorrect username / password !'
    return render_template('admin_login.html', msg = msg)

@app.route('/teacher/login', methods=['GET', 'POST'])
def teacher_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM reg WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['Id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('teacherboard.html', msg = 'username')
        else:
            msg = 'Incorrect username / password !'
    return render_template('teacher_login.html', msg = msg)

# ----- ACCOUNT ROUTE -------
@app.route('/upload', methods=['POST'])
def upload_file():
        cursor = mysql.connection.cursor()
        file = request.files['file']
        cursor.execute('INSERT  INTO files (name, data) VALUES(%s, %s)',(file.filename, file.read()))
        mysql.connection.commit()
        return '<h1>File uploaded successfully</h1>'

@app.route('/bursar/login', methods=['GET', 'POST'])
def bursar_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM reg WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['Id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('bursar.html', msg = 'username')
        else:
            msg = 'Incorrect username / password !'
    return render_template('bursar_login.html', msg = msg)

# @app.route('//<int:id>')
# def file(id):
#     cursor = mysql.connection.cursor()
#     cursor.execute('SELECT data FROM files where id=%s,' (id))
#     data = cursor.fetchone()[0]
#     return send_file(BytesIO(data), as_attachment_filename=True, attachment_filename='file.txt')

if __name__ == '__main__':
    app.run(debug=True)


if '__main__'== __name__:
    app.run(debug=True)