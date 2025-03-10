import mysql.connector

# MySQL database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='javap'
    )
