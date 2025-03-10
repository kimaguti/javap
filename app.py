from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='chama_app'
    )

# Routes
@app.route('/')
def home():
    if 'chairperson_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_phone = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if it's username or phone
        cursor.execute('SELECT * FROM chairperson WHERE username = %s OR phone_no = %s', (username_or_phone, username_or_phone))
        chairperson = cursor.fetchone()
        
        if chairperson and check_password_hash(chairperson['password'], password):
            session['chairperson_id'] = chairperson['id']
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials', 403

    return render_template('login.html')

@app.route('/register_chairperson', methods=['GET', 'POST'])
def register_chairperson():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        id_number = request.form['id_number']
        phone_no = request.form['phone_no']
        username = request.form['username']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO chairperson (first_name, middle_name, last_name, id_number, phone_no, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                       (first_name, middle_name, last_name, id_number, phone_no, username, hashed_password))
        conn.commit()
        return redirect(url_for('login'))
    
    return render_template('register_chairperson.html')

@app.route('/dashboard')
def dashboard():
    if 'chairperson_id' not in session:
        return redirect(url_for('login'))
    
    chairperson_id = session['chairperson_id']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch groups created by the chairperson
    cursor.execute('SELECT * FROM groups WHERE chairperson_id = %s', (chairperson_id,))
    groups = cursor.fetchall()

    return render_template('dashboard.html', groups=groups)

@app.route('/register_member', methods=['GET', 'POST'])
def register_member():
    if 'chairperson_id' not in session:
        return redirect(url_for('login'))

    chairperson_id = session['chairperson_id']
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_no = request.form['phone_no']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        group_id = request.form['group_id']
        
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO members (first_name, last_name, phone_no, username, password, role, group_id) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                       (first_name, last_name, phone_no, username, hashed_password, role, group_id))
        conn.commit()
        return redirect(url_for('dashboard'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM groups WHERE chairperson_id = %s', (chairperson_id,))
    groups = cursor.fetchall()
    
    return render_template('register_member.html', groups=groups)

if __name__ == '__main__':
    app.run(debug=True)
