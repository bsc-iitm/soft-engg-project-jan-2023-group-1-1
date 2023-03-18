
from application.models import User
from application.models import db
from application.workers import celery
from celery import chain
import pandas
import os
import secrets,string    
from random_username.generate import generate_username   

class invalidRoleException(Exception):
    pass

class emptyFileException(Exception):
    pass

def str_to_int_roles(role):
    res = None
    if role.lower() == "student":
        res = 1
    elif role.lower() == "support agent":
        res = 2
    elif role.lower() == "admin":
        res = 3
    elif role.lower() == "manager":
        res = 4
    else:
        raise invalidRoleException
    return res

@celery.task
def add_users_import(csv_file_path):
    """
    Adds users as a batch job wherein a CSV file is passed from the frontend and then operated upon by the backend.
    csv_file_path is the path to the csv file which has the CSV file of details. Please change it accordingly.
    """
    df = None
    b = None
    try:
        df = pandas.read_csv(csv_file_path)
    except:
        print("Your file must have atleast one row of data apart from the columns") #Chirag: Please adjust this error by sending an email for an empty file.
    try:
        b = len(df)
        #print(b)
        if b == 0:
            raise emptyFileException
    except:
        print("Your file must have ateast one row of data apart from the columns") #Chirag: Please adjust this error by sending an email for an empty file.
    flag = 0
    for i in range(b):
            row = df.iloc[i]
            email_id = None
            try:
                email_id = row["email_id"]
            except:
                print("Please have an 'email_id' column in your csv file") #Chirag: Please adjust this error by sending an email for requiring an email_id column in the.
                flag = -1
                break
            try:
                role = row["roles"]
                role = str_to_int_roles(role)
            except:
                flag = 1
                continue
            secure_str = ''.join((secrets.choice(string.ascii_letters) for i in range(8)))
            user_name=generate_username(1)[0]
            user = User(user_name=user_name,email_id=email_id,password=secure_str,role_id=role)
            db.session.add(user)
            db.session.commit()

    if flag == 1:
            print("Either you don't have a 'roles' column in your csv or some roles were not amongst 'student', 'support agent', 'admin', 'manager'. Those not having an appropriate role haven't been added to the database. Rest have been added.")
            #Chirag: Please adjust this error by sending an email informing the admin about this.
    elif flag == -1:
         pass
    else:
            print("All user have been added successfully to the database.")  #Chirag: Please adjust this notification by sending an email informing the admin about this.