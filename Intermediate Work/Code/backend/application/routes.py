from application import app
from flask import request, jsonify
from datetime import datetime, timedelta
import jwt
# from .models import User
# import jwt
from .models import User


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
        }, app.config['SECRET_KEY'], algorithm="HS256")
        # access_token = create_access_token(identity=email)
        print(token)
        return jsonify(message="Login Succeeded!", token=token), 201
    else:
        return jsonify(message="Bad Email or Password"), 401