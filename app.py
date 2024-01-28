from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_mysqldb import MySQL
import MySQLdb.cursors,re,hashlib



app=Flask(__name__)

app.secret_key = '8870914318'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'John2424.s'
app.config['MYSQL_DB'] = 'user'

mysql = MySQL(app)

def display_employees():
               cursor = mysql.connection.cursor()
               cursor.execute('SELECT * FROM emp')
               employees = cursor.fetchall()
               return render_template('home.html', employees=employees)
           
@app.route('/')
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    # Clear the session to log out the user
    session.clear()
    return redirect(url_for('login'))

@app.route('/home', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM emp WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()

        if account:
            return display_employees()            
        else:
            # Failed login
            return "Invalid user"
    if request.method == 'GET':
        return display_employees()

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO emp (username, password, email) VALUES (%s, %s, %s)', (username, password, email,))
        mysql.connection.commit()

        return redirect(url_for('home'))

    return render_template('add_employee.html')

# Route to delete employee
@app.route('/delete_employee/<int:employee_id>')
def delete_employee(employee_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM emp WHERE id = %s', (employee_id,))
    mysql.connection.commit()

    return redirect(url_for('home'))

# Route to update employee details
@app.route('/update_employee/<int:employee_id>', methods=['GET', 'POST'])
def update_employee(employee_id):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE emp SET username=%s, password=%s, email=%s WHERE id=%s', (username, password, email, employee_id,))
        mysql.connection.commit()
        
        return redirect(url_for('home'))

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM emp WHERE id = %s', (employee_id,))
    employee = cursor.fetchone()

    return render_template('update_employee.html', employee=employee) 
           
        

@app.after_request
def add_cache_control(response):
    # Disable caching for sensitive pages
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response