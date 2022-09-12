from flask import Flask, render_template, request, flash, url_for, redirect, session
from flask_mysqldb import MySQL
import re
import sounddevice as sound
from scipy.io.wavfile import write
import wavio as wv
import random
import shutil

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '1a2b3c4d5e'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'multiuser'

# Intialize MySQL
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('reg.html')


@app.route('/logout')
def logout():
    session['name'] = ''
    session['email'] = ''
    session.clear()
    msg = 'successfully logged out'
    return render_template('login.html', message=msg)


@app.route('/UserDashboard')
def udashboard():
    if 'email' in session:
        cursor = mysql.connection.cursor()
        cursor.execute(' SELECT * FROM chat ORDER  BY id DESC ')
        chats = cursor.fetchall()
        return render_template('user/dashboard.html', chat=chats)

    return render_template('login.html')


@app.route('/AdminDashboard')
def adashboard():
    if 'email' in session:
        cursor = mysql.connection.cursor()
        cursor.execute(' SELECT * FROM chat ORDER  BY id DESC ')
        chats = cursor.fetchall()
        return render_template('admin/dashboard.html', chat=chats)

    return render_template('login.html')


@app.route('/users')
def users():
    if 'email' in session:
        cursor = mysql.connection.cursor()
        cursor.execute(' SELECT * FROM user ORDER  BY id DESC ')
        users = cursor.fetchall()
        return render_template('admin/users.html', user=users)

    return render_template('login.html')


@app.route('/delete/<string:email>', methods=['POST', 'GET'])
def delete(email):
    if 'email' in session:
        cursor = mysql.connection.cursor()
        cursor.execute(''' DELETE FROM chat WHERE email=%s ''', [email])
        cursor.execute(''' DELETE FROM user WHERE email=%s ''', [email])
        cursor.execute(''' DELETE FROM login WHERE email=%s ''', [email])
        mysql.connection.commit()
        cursor.close()
        return redirect('/users')

    return render_template('login.html')


@app.route('/deletechat/<string:id>', methods=['POST', 'GET'])
def deletechat(id):
    if 'email' in session:
        cursor = mysql.connection.cursor()
        cursor.execute(''' DELETE FROM chat WHERE id=%s ''', [id])
        mysql.connection.commit()
        cursor.close()
        return redirect('/AdminDashboard')

    return render_template('login.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/insertchat', methods=['POST', 'GET'])
def insertchat():
    if 'email' in session:
        if request.method == 'POST':
            msg = ''
            # collect inputs
            name = request.form['name']
            email = request.form['email']
            message = request.form['chat']
            mtype = 'text'
            # check if empty symptoms are submitted
            if name == '' or email == '' or message == '':
                msg = 'Please fill all boxes'
                return render_template('user/dashboard.html', message=msg)
            else:
                # Process inputs
                # Check if account exists using MySQL
                cursor = mysql.connection.cursor()

                cursor.execute(''' INSERT INTO chat VALUES(NULL,%s,%s,%s,%s,NULL)''', (name, email, message, mtype))
                mysql.connection.commit()
                cursor.close()
        return redirect('UserDashboard')

    return render_template('login.html')


@app.route('/insertaudio', methods=['POST', 'GET'])
def insertaudio():
    if 'email' in session:
        if request.method == 'POST':
            msg = ''
            # collect inputs
            email = request.form['email']
            name = request.form['name']
            time = request.form['time']
            mtype = 'audio'
            # check if empty symptoms are submitted
            if name == '' or email == '':
                msg = 'Please fill all boxes'
                return render_template('user/dashboard.html', message=msg)
            else:
                freq = 44100
                dur = int(time)
                recording = sound.rec(dur * freq,
                                      samplerate=freq, channels=2)
                sound.wait()
                message = 'recording_' + str(random.randint(1, 1000)) + '.wav'
                write(message, freq, recording)

                src_path = r"C:\Users\codepreacher\PycharmProjects\Multiuser\\" + message
                dst_path = r"C:\Users\codepreacher\PycharmProjects\Multiuser\static\audio\\" + message
                shutil.copy(src_path, dst_path)

                # Process inputs
                # Check if account exists using MySQL
                cursor = mysql.connection.cursor()

                cursor.execute(''' INSERT INTO chat VALUES(NULL,%s,%s,%s,%s,NULL)''', (name, email, message, mtype))
                mysql.connection.commit()
                cursor.close()
        return redirect('UserDashboard')

    return render_template('login.html')

@app.route('/insertchat2', methods=['POST', 'GET'])
def insertchat2():
    if 'email' in session:
        if request.method == 'POST':
            msg = ''
            # collect inputs
            name = request.form['name']
            email = request.form['email']
            message = request.form['chat']
            mtype = 'text'
            # check if empty symptoms are submitted
            if name == '' or email == '' or message == '':
                msg = 'Please fill all boxes'
                return render_template('user/dashboard.html', message=msg)
            else:
                # Process inputs
                # Check if account exists using MySQL
                cursor = mysql.connection.cursor()

                cursor.execute(''' INSERT INTO chat VALUES(NULL,%s,%s,%s,%s,NULL)''', (name, email, message, mtype))
                mysql.connection.commit()
                cursor.close()
        return redirect('AdminDashboard')

    return render_template('login.html')


@app.route('/insertaudio2', methods=['POST', 'GET'])
def insertaudio2():
    if 'email' in session:
        if request.method == 'POST':
            msg = ''
            # collect inputs
            email = request.form['email']
            name = request.form['name']
            time = request.form['time']
            mtype = 'audio'
            # check if empty symptoms are submitted
            if name == '' or email == '':
                msg = 'Please fill all boxes'
                return render_template('user/dashboard.html', message=msg)
            else:
                freq = 44100
                dur = int(time)
                recording = sound.rec(dur * freq,
                                      samplerate=freq, channels=2)
                sound.wait()
                message = 'recording_' + str(random.randint(1, 1000)) + '.wav'
                write(message, freq, recording)

                src_path = r"C:\Users\codepreacher\PycharmProjects\Multiuser\\" + message
                dst_path = r"C:\Users\codepreacher\PycharmProjects\Multiuser\static\audio\\" + message
                shutil.copy(src_path, dst_path)

                # Process inputs
                # Check if account exists using MySQL
                cursor = mysql.connection.cursor()

                cursor.execute(''' INSERT INTO chat VALUES(NULL,%s,%s,%s,%s,NULL)''', (name, email, message, mtype))
                mysql.connection.commit()
                cursor.close()
        return redirect('AdminDashboard')

    return render_template('login.html')


@app.route('/createAccount', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        msg = ''
        # collect inputs
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        address = request.form['address']
        # check if empty input are submitted
        if name == '' or email == '' or password == '' or phone == '' or address == '':
            msg = 'Please fill all boxes'
            return render_template('reg.html', message=msg)
        else:
            # Process inputs
            # Check if account exists using MySQL
            cursor = mysql.connection.cursor()

            cursor.execute(''' INSERT INTO user VALUES(NULL,%s,%s,%s,%s,%s,NULL)''',
                           (name, email, password, phone, address))
            cursor.execute(''' INSERT INTO login VALUES(NULL,%s,%s,%s,%s,NULL)''', (name, email, password, '2'))
            mysql.connection.commit()
            cursor.close()
            msg = 'Registration success'

            return render_template('reg.html', message=msg)
    return render_template('reg.html')


@app.route('/checkLogin', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        msg = ''
        # collect inputs
        email = request.form['email']
        password = request.form['password']
        # check if empty symptoms are submitted
        if email == '' or password == '':
            msg = 'Please fill all boxes'
            return render_template('login.html', message=msg)
        else:
            session['name'] = ''
            session['email'] = ''
            # Process inputs
            cursor = mysql.connection.cursor()

            cursor.execute(''' SELECT * FROM login WHERE email=%s AND password=%s ''', (email, password))
            account = cursor.fetchone()
            if account:
                if account[4] == 1:
                    session['name'] = account[1]
                    session['email'] = account[2]
                    return redirect('/AdminDashboard')
                else:
                    session['name'] = account[1]
                    session['email'] = account[2]
                    return redirect('/UserDashboard')
            else:
                msg = 'Login failure !'
            mysql.connection.commit()
            cursor.close()

            return render_template('login.html', message=msg)
    return render_template('login.html')


if __name__ == '__main__':
    app.run()
