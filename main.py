import re

from flask import Flask, render_template, request
import pymysql


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            mydb = pymysql.connect(
                host="reseau.proxy.rlwy.net",
                port=20874,
                user="root",
                password="jptqTngdTLrZVSAnxSldlOnHZxVwrEQg",
                database="railway",
                ssl={"ssl": {}}
            )

        except Exception as e:
            return f"Database connection failed: {str(e)}"

        mycursor = mydb.cursor()

        mycursor.execute(
            "SELECT * FROM userdata WHERE username = %s AND password = %s",
            (username, password)
        )

        account = mycursor.fetchone()

        if account:
            print('Login Successful')
            name = account[0]
            msg = 'Login Successful'
            return render_template('welcome.html', name=name, msg=msg)
        else:
            msg = 'Incorrect Credentials / Kindly Check'
            return render_template('login.html', msg=msg)

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        mydb = pymysql.connect(
            host="reseau.proxy.rlwy.net",
            port=20874,
            user="root",
            password="jptqTngdTLrZVSAnxSldlOnHZxVwrEQg",
            database="railway",
            ssl={"ssl": {}}
        )

        mycursor = mydb.cursor()

        mycursor.execute(
            "SELECT * FROM userdata WHERE username = %s AND email = %s",
            (username, email)
        )

        account = mycursor.fetchone()

        if account:
            msg = 'Account already exists!'
            
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'

        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'

        elif not username or not password or not email:
            msg = 'Kindly fill out all Details!'
        else:
            mycursor.execute(
                "INSERT INTO userdata VALUES (%s, %s, %s)", (username, password, email)
            )

            mydb.commit()

            msg = 'You have successfully registered!'

            name = username

            return render_template('welcome.html', name=name, msg=msg)
        
        return render_template('register.html', msg=msg)

    return render_template("register.html")

@app.route('/logout')
def logout():
    name = ''
    id = ''
    msg = "Logged Out Successfully"
    return render_template('login.html', msg=msg, name=name, id=id)

if __name__ == '__main__':
    app.run(debug=True)