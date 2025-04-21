import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_for_development')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@postgres:5432/car_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

