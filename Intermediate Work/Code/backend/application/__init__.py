from flask import *
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
