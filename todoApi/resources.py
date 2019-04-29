from todoApi.models import User, Todo
from todoApi import db
from datetime import datetime
from flask import jsonify
from flask_restful import Resource, abort, reqparse, fields, marshal_with

todo_fields = {
	'id': fields.Integer,
	'title': fields.String,
	'description': fields.String,
	'created_at': fields.DateTime,
	'deadline': fields.DateTime,
	'user_id': fields.Integer
}

parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('description')
parser.add_argument('created_at')
parser.add_argument('deadline')
parser.add_argument('user_id')


class TodoResource(Resource):
	@marshal_with(todo_fields)
	def get(self):
		todo = db.session.query(Todo).all()
		if not todo:
			abort(404,message='Todo does not exist')

		return todo