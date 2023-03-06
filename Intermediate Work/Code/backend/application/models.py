from flask import *
from flask_sqlalchemy import SQLAlchemy
import jwt
from functools import wraps
from application import app

db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

class User(db.Model):
    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_name=db.Column(db.String(100),unique=True,nullable=False)
    name=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),unique=True,nullable=False)
    email_id=db.Column(db.String(100),unique=True,nullable=False)
    role_id=db.Column(db.Integer,nullable=False)
    
class Student(db.Model):
    user_id=db.Column(db.Integer, db.ForeignKey('User.user_id'),primary_key=True)
    roll_number=db.Column(db.String(100),nullable=False,primary_key=True)
    
    
class Support_Agent(db.Model):
    user_id=db.Column(db.Integer, db.ForeignKey('User.user_id'),primary_key=True)
    agent_id=db.Column(db.String(100),nullable=False,primary_key=True)
    
class Admin(db.Model):
    user_id=db.Column(db.Integer, db.ForeignKey('User.user_id'),primary_key=True)
    admin_id=db.Column(db.String(100),nullable=False,primary_key=True)
    
class Manager(db.Model):
    user_id=db.Column(db.Integer, db.ForeignKey('User.user_id'),primary_key=True)
    manager_id=db.Column(db.String(100),nullable=False,primary_key=True)

class Ticket(db.Model):
    ticket_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    description=db.Column(db.String(100),nullable=False)
    creation_date=db.Column(db.DateTime,nullable=False)
    creator_id=db.Column(db.Integer, db.ForeignKey('User.user_id'))
    responder_id=db.Column(db.Integer, db.ForeignKey('User.user_id'))
    number_of_upvotes=db.Column(db.Integer,default=0)
    is_read=db.Column(db.Boolean,nullable=False)
    is_open=db.Column(db.Boolean,nullable=False)
    is_offensive=db.Column(db.Boolean,nullable=False)
    is_FAQ=db.Column(db.Boolean,nullable=False)
    
# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        return f(current_user, *args, **kwargs)

    return decorated
    
    