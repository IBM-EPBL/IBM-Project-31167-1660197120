from flask import Flask, redirect, url_for, request, app, render_template, session
import ibm_db
from flask_session import Session

app = Flask(__name__)
app = Flask(__name__, template_folder='./views')
# Session Config
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# DB2 Config
dsn_hostname = "125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
dsn_uid = "cwy77416"
dsn_pwd = "4zg0yQJwQ5ZQMwki"
dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "bludb"
dsn_port = "30426"
dsn_protocol = "tcpip"
dsn_security = "ssl"

dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7}"
).format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd, dsn_security)

try:
    conn = ibm_db.connect(dsn, "", "")
    print("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)
except:
    print("Unable to connect: ", ibm_db.conn_errormsg())

# Create DB
# createQuery = """CREATE TABLE users (
# 	id INT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
# 	email VARCHAR(50) NOT NULL UNIQUE,
# 	password VARCHAR(50) NOT NULL,
# 	username VARCHAR(50) NOT NULL UNIQUE,
# 	rollno VARCHAR(15) NOT NULL UNIQUE
# )"""
# createTable = ibm_db.exec_immediate(conn, createQuery)

# APIs
@app.route('/')
def home():
    if(session.get('isLoggedIn')):
        return render_template('home.html')
    else:
        return redirect(url_for('register'))

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        rollno = request.form['rollno']
        password = request.form['password']

        checkQuery = "SELECT * FROM users WHERE email = '{0}'".format(email)
        checkTable = ibm_db.exec_immediate(conn, checkQuery)

        if(ibm_db.fetch_row(checkTable) == False):
            insertQuery = """INSERT INTO user (email, username, password, rollno) 
                            VALUES ('{0}', '{1}', '{2}', '{3}');""".format(email, username, password, rollno)
            insertTable = ibm_db.exec_immediate(conn, insertQuery)
            session['isLoggedIn'] = True
        else:
            return render_template('login.html', mode = 'user exists')

        return render_template('home.html', mode = 'success', username = username, email = email, rollno = rollno)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        checkQuery = "SELECT * FROM users WHERE email = '{0}' AND password = '{1}'".format(email, password)
        checkTable = ibm_db.exec_immediate(conn, checkQuery)

        if(not ibm_db.fetch_row(checkTable)):
            session['isLoggedIn'] = True
            return render_template('home.html', mode = 'success', email = email)
        else:
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['isLoggedIn'] = None
    return redirect('/')