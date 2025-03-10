import os

class Config:
    SECRET_KEY = os.urandom(24)
    DATABASE_URI = 'mysql://root:@localhost/javap'
