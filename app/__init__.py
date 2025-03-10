from flask import Flask
from .auth import auth_bp
from .routes import routes_bp
import mysql.connector

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(routes_bp)

    return app

# MySQL database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='javap'
    )
