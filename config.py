import os

class Config:
    SECRET_KEY = "supersecretkey" 
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://flaskuser:flaskpassword@localhost/yugioh'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

