from os import environ

SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS',False)
SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI','mysql+mysqlconnector://root:demo@localhost:3306/ambulance_data')