import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister

app = Flask(__name__)

app.config['DEBUG'] = True

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://myawesomeuser:mysecretpassword@database/mydatabase')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Make sure that mariadb/mysql doesn't drop connection
app.config['SQLALCHEMY_POOL_RECYCLE'] = 5

app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)
