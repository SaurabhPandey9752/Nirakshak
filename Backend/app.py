from flask import Flask, render_template, request,session,redirect,url_for
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import re
import mysql.connector
import MySQLdb.cursors 
from werkzeug.utils import redirect
app = Flask(__name__, template_folder = 'template', static_folder  = 'template')
app.secret_key="database"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sam123'
app.config['MYSQL_DB'] = 'rajbase'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'cctvnirakshak@gmail.com'
app.config['MAIL_PASSWORD'] = 'xxxxxxxx'
app.config['MAIL_DEFAULT_SENDER'] = 'cctvnirakshak@gmail.com'
app.config['MAIL_DEBUG'] = True

mysql = MySQL(app)
mail=Mail(app) 

@app.route("/")
def index():
    return render_template('index.html')

'''@app.route("/home")
def home():
    msg=''
    if 'email' in session:
        msg=session['email']
        return render_template('home.html',msg=msg)
    return redirect(url_for('index'))'''


@app.route("/police.html" ,methods=['POST','GET'])
def police():
    msg = ""
    if request.method=='POST'and "email" in request.form and "password" in request.form :
        email=request.form['email']
        Password=request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM  police WHERE email=%s ',(email,))
        account=cursor.fetchone()
        cursor.close()
        if account and account['password']==Password:
            session['loggedin']=True
            session['email'] = email
            session['fullName'] = account['fullName']
           
            return render_template('index4.html')
        else:
            msg='Incorrect username/password!'  
    else:
        msg = " Please fill the form !"  
    return render_template('police.html',msg='hello')

@app.route("/logout")
def user_logout():
    session.pop('loggedin',None)
    session.pop('Email_id',None)
    session.pop('Phone_num',None)
    session.pop('First_name',None)
    session.pop('Last_name',None)
    return redirect(url_for('police'))

@app.route("/forgot", methods=["GET"])
def forgot():
    return render_template("forgot.html")


def email_exists(email):
    try:
        #conn = mysql.connector.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_db)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM police WHERE email = %s', (email,))
        result = cursor.fetchone()
        cursor.close()
        #conn.close()
        return result is not False
    except Exception as e:
        print("Error checking email:", e)
        return False
    
def send_reset_email(email, reset_link):
    try:
        msg = Message('Password Reset', recipients=[email])
        msg.body = f'Click the link below to reset your password:\n{reset_link}'
        mail.send(msg)
        return True  # Return True if email sent successfully
    except Exception as e:
        print("Error sending reset email:", e)
        return False  # Return False if there's an error sending the email


@app.route("/handle_forgot_password", methods=['POST','GET'])
def handle_forgot_password():
    # Get the email address from the form
    email = request.form.get("email")

    # Check if the email exists in the database
    if email_exists(email):
        # Generate and send the password reset link
        reset_link = f"https://example.com/reset-password?email={email}"  # Example reset link
        send_reset_email(email, reset_link)
        return render_template("password_reset_confirmation.html")
    else:
        # Email does not exist in the database
        return render_template("forgot.html", error="Email not found. Please try again.")


@app.route("/index4", methods=['POST','GET'])
def index4():
    # Handle form submission here
    return render_template('index4.html')

@app.route("/index3", methods=['POST','GET'])
def index3():
    # Handle form submission here
    return render_template('index3.html')


@app.route("/security", methods=['POST','GET'])
def security():
    # Handle form submission here
    return render_template('security.html')

@app.route("/map", methods=['POST','GET'])
def map():
    # Handle form submission here
    return render_template('uptopolicewithgeocoder.html')

@app.route("/markers.json", methods=['POST','GET'])
def mmark():
    # Handle form submission here
    return render_template('markers.json')


'''@app.route("/user_logout")
def user_logout():
    session.pop('loggedin',None)
    session.pop('email',None)
    session.pop('contact',None)
    session.pop('name',None)
    session.pop('Last_name',None)
    return redirect(url_for('user_login'))'''


@app.route("/user.html",methods=['POST','GET'])
def user():
    msg=''
    if request.method=='POST' and  'name' in request.form and 'email' in request.form and 'subject' in request.form and 'contact' in request.form and 'ipAddress' in request.form and 'modelNo' in request.form and 'latitude' in request.form and 'longitude' in request.form and 'cameraAccess' in request.form :
        name=request.form['name']
        email=request.form['email']
        subject=request.form['subject']
        contact=request.form['contact']
        ipAddress=request.form['ipAddress']
        modelNo=request.form['modelNo']
        latitude=request.form['latitude']
        longitude=request.form['longitude']
        cameraAccess=request.form['cameraAccess']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email= % s', (email, ))
        account1=cursor.fetchone()
        cursor.execute('SELECT * FROM user WHERE contact= % s', (contact, ))
        account2=cursor.fetchone()
        cursor.close()
        if account1 :
            msg="An account is already registered with this email."
        elif account2 :
            msg="An account is already registered with this Phone Number."
        elif not re.match(r'[0-9]+', contact):
            msg = 'Invalid Phone number !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif len(contact) != 10:
            msg = 'Please enter a 10 digit correct phone number !'
        elif not contact or not email:
            msg = 'Please fill out the form !'
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO user(name,email,subject,contact,ipAddress,modelNo,latitude,longitude,cameraAccess) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)', (name,email,subject,contact,ipAddress,modelNo,latitude,longitude,cameraAccess))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('index'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    
    return render_template('user.html', msg = msg)
    
@app.route("/register.html",methods=['POST','GET'])
def register():
    msg=''
    if request.method=='POST' and  'fullName' in request.form and 'username' in request.form and 'email' in request.form and 'phoneNumber' in request.form and 'password' in request.form and  'confirmPassword' in request.form and 'gender' in request.form :
        fullName=request.form['fullName']
        username=request.form['username']
        email=request.form['email']
        phoneNumber=request.form['phoneNumber']
        password=request.form['password']
        confirmPassword=request.form['confirmPassword']
        gender=request.form['gender']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM police WHERE email= % s', (email, ))
        account1=cursor.fetchone()
        cursor.execute('SELECT * FROM police WHERE phoneNumber= % s', (phoneNumber, ))
        account2=cursor.fetchone()
        cursor.close()
        if account1 :
            msg="An account is already registered with this email."
        elif account2 :
            msg="An account is already registered with this Phone Number."
        elif not re.match(r'[0-9]+', phoneNumber):
            msg = 'Invalid Phone number !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif len(phoneNumber) != 10:
            msg = 'Please enter a 10 digit correct phone number !'
        elif not phoneNumber or not email:
            msg = 'Please fill out the form !'
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO police(fullName,username,email,phoneNumber,password,gender) VALUES(%s,%s,%s,%s,%s,%s)', (fullName,username,email,phoneNumber,password,gender))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('index'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    
    return render_template('register.html', msg = msg)


if __name__=="__main__":
    app.run(debug=True)

'''

@app.route('/search_blood_banks', methods = ['GET', 'POST'])
def search_blood_banks():
    msg = ''
    if request.method == "POST" and "State" in request.form and "District" in request.form:
        State = request.form['State']
        District = request.form['District']
        if len(State) > 0 and len(District) > 0:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT *  FROM Blood_bank WHERE State = %s AND District = %s', (State, District,))
            rows = cursor.fetchall()
            cursor.close()
            return render_template('search_blood_banks.html', rows = rows)
        else:
            msg = "Please fill all the details!"
            return render_template('search_blood_banks.html', msg = msg)
    return render_template('search_blood_banks.html')
'''