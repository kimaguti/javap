# app/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .database import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_phone = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('SELECT * FROM chairperson WHERE username = %s OR phone_no = %s', (username_or_phone, username_or_phone))
        chairperson = cursor.fetchone()
        
        if chairperson and check_password_hash(chairperson['password'], password):
            session['chairperson_id'] = chairperson['id']
            return redirect(url_for('routes.dashboard'))
        else:
            return 'Invalid credentials', 403

    return render_template('login.html')

@auth_bp.route('/register_chairperson', methods=['GET', 'POST'])
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
        return redirect(url_for('auth.login'))
    
    return render_template('register_chairperson.html')
