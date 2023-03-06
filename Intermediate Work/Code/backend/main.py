from application import models,app
from application.models import *
import jwt
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

@app.route("/")
def logins():
    return "hi"

# @app.route("/login", methods=["POST"])
# def login():
#     if request.is_json:
#         email = request.json["email"]
#         password = request.json["password"]
#     else:
#         email = request.form["email"]
#         password = request.form["password"]
#     test = User.query.filter_by(email=email).first()
#     # print(test)
#     if (test is None):
#         return jsonify(message="User does not exist"), 409
#     elif (test.password == password):
#         token = jwt.encode({
#             'public_id': test.public_id,
#             'exp': datetime.utcnow() + timedelta(minutes=80)
#         }, app.config['SECRET_KEY'], algorithm="HS256")
#         # access_token = create_access_token(identity=email)
#         print(token)
#         return jsonify(message="Login Succeeded!", token=token), 201
#     else:
#         return jsonify(message="Bad Email or Password"), 401


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)