from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
import functools
from flask import request, jsonify
import jwt
from .config import Config
engine = None
Base = declarative_base()
db = SQLAlchemy()

class User(db.Model):
    # __tablename__ = 'user'
    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_name=db.Column(db.String(100),unique=True,nullable=False)
    name=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),unique=True,nullable=False)
    email_id=db.Column(db.String(100),unique=True,nullable=False)
    role_id=db.Column(db.Integer,nullable=False)
    
class Student(db.Model):
    user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'),primary_key=True)
    roll_number=db.Column(db.String(100),nullable=False,primary_key=True)
    
class Support_Agent(db.Model):
    user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'),primary_key=True)
    agent_id=db.Column(db.String(100),nullable=False,primary_key=True)

    
class Admin(db.Model):
    user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'),primary_key=True)
    admin_id=db.Column(db.String(100),nullable=False,primary_key=True)
    
class Manager(db.Model):
    user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'),primary_key=True)
    manager_id=db.Column(db.String(100),nullable=False,primary_key=True)

class Ticket(db.Model):
    ticket_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    description=db.Column(db.String(100),nullable=False)
    creation_date=db.Column(db.DateTime,nullable=False)
    creator_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
    responder_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
    number_of_upvotes=db.Column(db.Integer,default=0)
    is_read=db.Column(db.Boolean,nullable=False)
    is_open=db.Column(db.Boolean,nullable=False)
    is_offensive=db.Column(db.Boolean,nullable=False)
    is_FAQ=db.Column(db.Boolean,nullable=False)
    
def token_required(function):
	@functools.wraps(function)
	def loggedin(*args,**kwargs):
		auth_token=None
		try:
			auth_token = request.headers['secret_authtoken']
		
		except:
			return jsonify({"status":'unsuccessful, missing the authtoken'})
		
		try: 
			output = jwt.decode(auth_token,Config.SECRET_KEY,algorithms=["HS256"])
			#print(output)
			user = User.query.filter_by(user_id = output["user_id"]).first()
		except:
			return jsonify({"status":"failure, your token details do not match"})
		
		return function(user,*args,**kwargs)
	return loggedin
