from todoApi import db
from datetime import datetime


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file= db.Column(db.String(20), default='default.jpg')
	password = db.Column(db.String(60),nullable=False)
	todos = db.relationship('Todo', backref='author', lazy=True) 
	# backref add an nother colum to the todo and put the autoher(user who create the post) in it 
	#lazy is how the databse loads the data, if lazy=True it loads the data at once
	#how object is represented when we print it out
	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"


class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120),nullable=False)
	description = db.Column(db.Text, nullable=True)
	estTime = db.Column(db.Float, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	deadline = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	#user in lowercase because we are referencing the table name (there are alsway lowercase) and Todo in User is a relationship an there
	#we are referencing the class Todo
	def __repr__(self):
		return f"Todo('{self.title}', '{self.estTime}','{self.date_finished}')"

