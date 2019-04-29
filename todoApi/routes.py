from flask import jsonify, request, redirect, flash, url_for, abort, make_response
from datetime import datetime
from flask_restful import Resource
from todoApi.models import User, Todo
from todoApi import app, db, bcrypt, api


@app.route('/', methods=['GET'])
def helo():
	user= User.query.all()
	response = []
	
	return str(user)