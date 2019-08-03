from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, DateField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

#config MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'HELPNET'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('home.html')

#About
@app.route('/about')
def about():
    return render_template('about.html')

# Register Form class
class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=6, max =50)])
    name = StringField('Name', [validators.Length(min=1, max =50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    dob = DateField('Date of Birth')
    registerNo = StringField('Register No./ EmployeeId', [validators.Length(min=1, max =50)])
    company = StringField('Company / College', [validators.Length(min=1, max =50)])
    department = StringField('Department', [validators.Length(min=1, max =50)])

#  User Register
@app.route('/register', methods = ['GET','POST'])
def reguster():
    form = RegisterForm(request.form)
    if request.method ==  'POST' and form.validate():
        username = form.username.data
        name = form.name.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        dob = form.dob.data
        registerNo =form.registerNo.data
        company = form.company.data
        department = form.department.data
        # Create Cursor
        cur = mysql.connection.cursor()

        #Execute query
        cur.execute("INSERT INTO users (username,name,email,password,dob,RegisterNo,company,department)"
                "VALUES(%s, %s, %s, %s,%s, %s, %s, %s)",(username,name,email,password,dob,registerNo,company,department))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('index'))
    return render_template('register.html', form=form)



if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug = True)


# from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
# from flask_mysqldb import MySQL
# from wtforms import Form, StringField, TextAreaField, PasswordField, validators
# from passlib.hash import sha256_crypt
# from functools import wraps
#
# app = Flask(__name__)
#

#

# # Register Form class
# class RegisterForm(Form):
#     username = StringField('Name', [validators.Length(min=1, max =50)])
#     email = StringField('Email', [validators.Length(min=6, max=50)])
#     password = PasswordField('Password', [
#         validators.DataRequired(),
#         validators.EqualTo('confirm', message='Passwords do not match')
#     ])
#     confirm = PasswordField('Confirm Password')
#
# #  User Register
# @app.route('/register', methods = ['GET','POST'])
# def reguster():
#     form = RegisterForm(request.form)
#     if request.method ==  'POST' and form.validate():
#         username = form.username.data
#         email = form.email.data
#         password = sha256_crypt.encrypt(str(form.password.data))
#
#         # Create Cursor
#         cur = mysql.connection.cursor()
#
#         #Execute query
#         cur.execute("INSERT INTO users (username,name,email,password,dob,RegisterNo,company,department)"
#                 "VALUES(%s, %s, %s, %s,%s, %s, %s, %s)",(username,name,email,password,dob,RegisterNo,company,department))
#
#         # Commit to DB
#         mysql.connection.commit()
#
#         # Close connection
#         cur.close()
#
#         flash('You are now registered and can log in', 'success')
#
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)
#
# # User login
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # Get Form Fields
#         username = request.form['username']
#         password_candidate = request.form['password']
#
#         # Create cursor
#         cur = mysql.connection.cursor()
#
#         # Get user by username
#         result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
#
#         if result > 0:
#             # Get stored hash
#             data = cur.fetchone()
#             password = data['password']
#
#             # Compare Passwords
#             if sha256_crypt.verify(password_candidate, password):
#                 # Passed
#                 session['logged_in'] = True
#                 session['username'] = username
#
#                 flash('You are now logged in', 'success')
#                 return redirect(url_for('dashboard'))
#             else:
#                 error = 'Invalid login'
#                 return render_template('login.html', error=error)
#             # Close connection
#             cur.close()
#         else:
#             error = 'Username not found'
#             return render_template('login.html', error=error)
#
#     return render_template('login.html')
#
# # Check if user logged in
# def is_logged_in(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return f(*args, **kwargs)
#         else:
#             flash('Unauthorized, Please login', 'danger')
#             return redirect(url_for('login'))
#     return wrap
#
# # Logout
# @app.route('/logout')
# @is_logged_in
# def logout():
#     session.clear()
#     flash('You are now logged out', 'success')
#     return redirect(url_for('login'))
#
