from flask import Flask, redirect, url_for, request, app, render_template

app = Flask(__name__)
app = Flask(__name__, template_folder='./views')

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/register", methods = ['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        return render_template('register.html', mode = 'success', username = username, email = email, phone = phone)