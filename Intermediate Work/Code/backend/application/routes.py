from application import app
from flask import request, jsonify
from datetime import datetime, timedelta
import jwt
# from .models import User
# import jwt
from .models import *
from .config import Config

@app.route("/")
def home():
    return 'hi'

@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        email = request.json["email"]
        password = request.json["password"]
    else:
        email = request.form["email"]
        password = request.form["password"]
    test = User.query.filter_by(email_id=email).first()
    # print(test)
    if (test is None):
        return jsonify(message="User does not exist"), 409
    elif (test.password == password):
        token = jwt.encode({
            'user_id': test.user_id,
            'exp': datetime.utcnow() + timedelta(minutes=80)
        }, Config.SECRET_KEY, algorithm="HS256")
        # access_token = create_access_token(identity=email)
        print(token)
        return jsonify(message="Login Succeeded!", token=token,user_id=test.user_id), 201
    else:
        return jsonify(message="Bad Email or Password"), 401

@app.route("/users", methods=["GET"])
@token_required
def get_users(current_user):
    print(current_user)
    users = User.query.all()
    results = [
        {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "name": user.name,
            "email_id": user.email_id,
            "role_id": user.role_id
        } for user in users]

    return jsonify(results)