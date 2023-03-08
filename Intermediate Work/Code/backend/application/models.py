from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
import functools
from flask import request, jsonify
import jwt
from .config import Config
engine = None
Base = declarative_base()
db = SQLAlchemy()
from datetime import datetime

class User(db.Model):
    __tablename__='user'
    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_name=db.Column(db.String(100),unique=True,nullable=False)
    #name=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),unique=True,nullable=False)
    email_id=db.Column(db.String(100),unique=True,nullable=False)
    role_id=db.Column(db.Integer,nullable=False) #Role ID for students is 1, for Support Agents is 2, Admins is 3, Manager is 4.

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

class Response(db.Model):
    response_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.ticket_id'))
    response = db.Column(db.String(200), nullable=False) 
    responder_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    response_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    parent_list = db.relationship('Ticket',back_populates='responses', lazy='subquery')

class Ticket(db.Model):
    ticket_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    description=db.Column(db.String(100),nullable=False)
    creation_date=db.Column(db.DateTime,nullable=False, default=datetime.utcnow())
    creator_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
    number_of_upvotes=db.Column(db.Integer,default=0)
    is_read=db.Column(db.Boolean,nullable=False)
    is_open=db.Column(db.Boolean,nullable=False)
    is_offensive=db.Column(db.Boolean,nullable=False)
    is_FAQ=db.Column(db.Boolean,nullable=False)
    responses = db.relationship('Response', back_populates='parent_list', lazy='subquery')

class Category(db.Model):
    category = db.Column(db.String(50), primary_key=True)

class FAQ(db.Model):
    ticket_id = db.Column(db.Integer,db.ForeignKey('ticket.ticket_id'),primary_key=True,autoincrement=True)
    category = db.Column(db.String, db.ForeignKey('category.category'))
    is_approved = db.Column(db.Boolean,nullable=False)
    ticket = db.relationship('Ticket', backref='faq')

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
