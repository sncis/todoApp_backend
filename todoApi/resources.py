from todoApi.models import User, Todo
from todoApi import db
from datetime import datetime
from flask_restful import Resource, abort, reqparse, fields, marshal_with

todo_fields = {
	'id': fields.Integer,
	'title': fields.String,
	'description': fields.String,
	'estTime': fields.Float,
	'created_at': fields.DateTime,
	'deadline': fields.DateTime,
	'user_id': fields.Integer
}

user_fields = {
	'id': fields.Integer,
	'username': fields.String,
	'email': fields.String,
	'image_file': fields.String,
	'password': fields.String,
	# 'todos': fields.List,
}

todoParser = reqparse.RequestParser()
todoParser.add_argument('id')
todoParser.add_argument('title')
todoParser.add_argument('description')
todoParser.add_argument('estTime')
todoParser.add_argument('created_at')
todoParser.add_argument('deadline')
todoParser.add_argument('user_id')

userParser = reqparse.RequestParser()
userParser.add_argument('id')
userParser.add_argument('username')
userParser.add_argument('email')
userParser.add_argument('password')
userParser.add_argument('todos')

class UserResource(Resource):
	@marshal_with(user_fields)
	def get(self, id):
		user = db.session.query(User).filter(User.id ==id).all()
		if not user:
			abort(404, message="User with id {} does not exist".format(id))
		return user

class UserListResource(Resource):
	@marshal_with(user_fields)
	def get(self):
		users=db.session.query(User).all()
		return users
	
	@marshal_with(user_fields)
	def delete(self, id):
		user = db.session.query(User).filter(User.id ==id).all()
		if not user:
			abort(404, message="User with id {} does not exist".format(id))
		db.session.delete(user)
		db.session.commit()
		return {},204
	
	@marshal_with(user_fields)
	def put(self,id):
		user = db.session.query(User).filter(User.id ==id).all()
		if not user:
			abort(404, message="User with id {} does not exist".format(id))
		parsed_args = userParser.parse_args()
		user.username = parsed_args['username']
		user.email = parsed_args['email']
		user.password = parsed_args['password']
		db.session.add(user)
		db.session.commit()
		return user, 201


class TodoResource(Resource):
	@marshal_with(todo_fields)
	def get(self,id):
		todo = db.session.query(Todo).filter(Todo.id ==id).all()
		if not todo:
			abort(404, message="Todo {} does'nt exist".format(id))
		return todo

	def delete(self,id):
		todo = db.session.query(Todo).filter(Todo.id ==id).all()
		if not todo:
			abort(404, message="Todo {} does'nt exist".format(id))
		db.session.delete(todo)
		db.session.commit()
		return {}, 204

	@marshal_with(todo_fields)
	def put(self, id):
		parsed_args = todoParser.parse_args()
		todo = db.session.quert(Todo).filter(Todo.id == id).all()
		todo.title = parsed_args['title']
		todo.description = parsed_args['description']
		todo.estTime = parsed_args['estTime']
		todo.create_at = parsed_args['create_at']
		todo.deadline = parsed_args['desdline']
		todo.user_id = parsed_args['user_id']
		db.session.add(todo)
		db.session.commit()
		return todo, 201


class TodoListResource(Resource):
	@marshal_with(todo_fields)
	def post(self):
		parsed_args = todoParser.parse_args()
		todo = Todo(title=parsed_args['title'], 
		description=parsed_args['description'],
		estTim=parsed_args['estTime'],
		created_at=parsed_args['created_at'],
		deadline=parsed_args['deadline'],
		user_id=parsed_args['user_id'])
		db.session.add(todo)
		db.session.commit()
		return todo, 201

	@marshal_with(todo_fields)
	def get(self):
		todos = db.session.query(Todo).all()
		if not todos:
			abort(404,message='There are no Todos yet')
		return todos

class UserTodosResources(Resource):
	@marshal_with(todo_fields)
	def get(self, user_id):
		todos = db.session.query(Todo).filter(Todo.user_id == user_id).all()
		if not todos:
			abort(404,message="no todos for this user {}".formt(id))
		return todos, 200