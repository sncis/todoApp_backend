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
api.add_resource(TodoListResource, '/todos')
api.add_resource(TodoResource, '/todo/<string:id>')
api.add_resource(UserResource,'/user<string:id>')
api.add_resource(UserListResource,'/users/')
api.add_resource(UserTodosResources, '/user/<string:user_id>/todos/')



from todoApi.models import User, Todo
db.create_all()

migrate= Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

