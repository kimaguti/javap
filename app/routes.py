from flask import Blueprint, render_template, request, redirect, url_for, session
from . import get_db_connection

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def home():
    if 'chairperson_id' in session:
        return redirect(url_for('routes.dashboard'))
    return redirect(url_for('auth.login'))

@routes_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'chairperson_id' not in session:
        return redirect(url_for('auth.login'))
    
    chairperson_id = session['chairperson_id']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT * FROM groups WHERE chairperson_id = %s', (chairperson_id,))
    groups = cursor.fetchall()

    if request.method == 'POST' and 'group_name' in request.form:
        group_name = request.form['group_name']
        group_description = request.form['group_description']
        
        cursor.execute('INSERT INTO groups (name, description, chairperson_id) VALUES (%s, %s, %s)', 
                       (group_name, group_description, chairperson_id))
        conn.commit()
        return redirect(url_for('routes.dashboard'))

    return render_template('dashboard.html', groups=groups)

@routes_bp.route('/register_member', methods=['GET', 'POST'])
def register_member():
    if 'chairperson_id' not in session:
        return redirect(url_for('auth.login'))

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
        return redirect(url_for('routes.dashboard'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM groups WHERE chairperson_id = %s', (chairperson_id,))
    groups = cursor.fetchall()
    
    return render_template('register_member.html', groups=groups)
