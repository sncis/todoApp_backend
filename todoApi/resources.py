from todoApi.models import User, Todo
from todoApi import db
from datetime import datetime, timedelta,date
from flask_restful import Resource, abort, reqparse, fields, marshal_with

todo_fields = {
	'id': fields.Integer,
	'title': fields.String,
	'description': fields.String,
	'estTime': fields.Float,
	'created_at': fields.DateTime,
	'deadline': fields.DateTime,
	'user_id': fields.Integer,
	'done': fields.Boolean,
}

user_fields = {
	'id': fields.Integer,
	'username': fields.String,
	'email': fields.String,
	'image_file': fields.String,
	'password': fields.String,
}

todoParser = reqparse.RequestParser()
todoParser.add_argument('id',required=False)
todoParser.add_argument('title', required=False)
todoParser.add_argument('description', required=False)
todoParser.add_argument('estTime', required=False)
todoParser.add_argument('created_at', required=False)
todoParser.add_argument('deadline', required=False)
todoParser.add_argument('user_id', required=False)
todoParser.add_argument('done', required=False)
todoParser.add_argument('days')
# todo_args = todoParser.parse_args()

userParser = reqparse.RequestParser()
userParser.add_argument('id')
userParser.add_argument('username')
userParser.add_argument('email')
userParser.add_argument('password')
userParser.add_argument('todos')

class UserResource(Resource):
	@marshal_with(user_fields)
	def get(self, user_id):
		user = db.session.query(User).filter(User.id == user_id).all()
		if not user:
			abort(404, message="User with id {} does not exist".format(user_id))
		return user

	@marshal_with(user_fields)
	def post(self):
		parsed_args = userParser.parse_args()
		username = parsed_args['username']
		email = parsed_args['email']
		password= parsed_args['password']

		if not username or not email or not password:
			abort(400, message="username, email or password is missing ")
		
		user = User(username=username,email=email, password=password)
		db.session.add(user)
		db.session.commit()
		return user, 200

	@marshal_with(user_fields)
	def put(self,user_id):
		user = db.session.query(User).filter(User.id ==user_id).all()
		if not user:
			abort(404, message="User with id {} does not exist".format(user_id))
		parsed_args = userParser.parse_args()
		user.username = parsed_args['username']
		user.email = parsed_args['email']
		user.password = parsed_args['password']
		db.session.add(user)
		db.session.commit()
		return user, 201
	
	@marshal_with(user_fields)
	def delete(self, user_id):
		user = db.session.query(User).filter(User.id ==user_id).all()
		if not user:
			abort(404, message="User with id {} does not exist".format(user_id))
		db.session.delete(user)
		db.session.commit()
		return {},204


class TodoResource(Resource):
	@marshal_with(todo_fields)
	def get(self,user_id,id):
		todo = db.session.query(Todo).filter(Todo.id == id, Todo.user_id == user_id).all()
		if not todo:
			abort(404, message="Todo {} does'nt exist".format(id))
		return todo

	@marshal_with(todo_fields)
	def delete(self,user_id, id):
		todo = db.session.query(Todo).filter(Todo.id ==id, Todo.user_id == user_id).all()
		if not todo:
			abort(404, message="Todo {} does'nt exist".format(id))
		db.session.delete(todo)
		db.session.commit()
		return {}, 204

	@marshal_with(todo_fields)
	def put(self, user_id, id):
		parsed_args = todoParser.parse_args()
		todo = db.session.query(Todo).filter(Todo.id == id, Todo.User_id == user_id).all()
		todo.title = parsed_args['title']
		todo.description = parsed_args['description']
		todo.estTime = parsed_args['estTime']
		todo.created_at=parsed_args['created_at'],
		deadline=datetime.strptime(parsed_args['deadline']),
		todo.user_id = parsed_args['user_id'],
		todo.done = parsed_args['done']
		db.session.add(todo)
		db.session.commit()
		return todo, 201


class TodoListResource(Resource):
	@marshal_with(todo_fields)
	def post(self):
		parsed_args = todoParser.parse_args()
		todo = Todo(title=parsed_args['title'], 
		description=parsed_args['description'],
		estTime=parsed_args['estTime'],
		created_at=parsed_args['created_at'],
		deadline=datetime.strptime(parsed_args['deadline'], '%d/%m/%Y %H:%M'),
		done = parsed_args['done'],
		user_id=parsed_args['user_id'])
		db.session.add(todo)
		db.session.commit()
		return todo, 201

	@marshal_with(todo_fields)
	def get(self, user_id):
		todos = db.session.query(Todo).filter(Todo.user_id == user_id).all()
		if not todos:
			abort(204, message='There are no Todos yet')
		return todos
	
class DoneTodosListResource(Resource):
	@marshal_with(todo_fields)
	def get(self, user_id):
		todo = db.session.query(Todo).filter(Todo.user_id == user_id, Todo.done == True).all()
		if not todo:
			abort(204, message="no finished todos")
		return todo, 200
	
	def put(self,id):
		parsed_args = todoParser.parse_args()
		todo = db.session.query(Todo).filter(Todo.id == id).all()
		todo.done = True
		db.session.add(todo)
		db.session.commit()
		return(todo, 201)

class FilteredTodos(Resource):
	@marshal_with(todo_fields)
	def get(self, user_id):
		day = int(todoParser.parse_args()['days'])
		days = datetime.today() + timedelta(days=day)
		todos = db.session.query(Todo).filter(Todo.deadline <= days, Todo.user_id == user_id).all()
		if not todos:
			abort(204, message='no todos')
		return todos, 200




# class UserListResource(Resource):
# 	@marshal_with(user_fields)
# 	def get(self):
# 		users=db.session.query(User).all()
# 		return users
	
# 	@marshal_with(user_fields)
# 	def delete(self, id):
# 		user = db.session.query(User).filter(User.id ==id).all()
# 		if not user:
# 			abort(404, message="User with id {} does not exist".format(id))
# 		db.session.delete(user)
# 		db.session.commit()
# 		return {},204
	
# 	@marshal_with(user_fields)
# 	def put(self,id):
# 		user = db.session.query(User).filter(User.id ==id).all()
# 		if not user:
# 			abort(404, message="User with id {} does not exist".format(id))
# 		parsed_args = userParser.parse_args()
# 		user.username = parsed_args['username']
# 		user.email = parsed_args['email']
# 		user.password = parsed_args['password']
# 		db.session.add(user)
# 		db.session.commit()
# 		return user, 201

# 	@marshal_with(user_fields)
# 	def post(self):
# 		parsed_args = userParser.parse_args()
# 		username = parsed_args['username']
# 		email = parsed_args['email']
# 		password= parsed_args['password']

# 		if not username or not email or not password:
# 			abort(400, message="username, email or password is missing ")
# 		user = User(username=username,email=email, password=password)
# 		db.session.add(user)
# 		db.session.commit()
# 		# allUsers= db.session.query(User).all()
# 		return user, 200


# class UserTodosResources(Resource):
# 	@marshal_with(todo_fields)
# 	def get(self, user_id):
# 		todos = db.session.query(Todo).filter(Todo.user_id == user_id).all()
# 		if not todos:
# 			abort(404,message="no todos for this user {}".format(user_id))
# 		return todos, 200