from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from todoApi.resources import *
api.add_resource(TodoResource, '/')


from todoApi.models import User, Todo
db.create_all()

migrate= Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# from todoApi import routes

