## TicketAll, GetResolutionTimes, ResolutionTimes, FlaggPostAPI
# GET: Check Status Code and Key-Value Pairs
# POST/PATCH: Check Status Code, GET Request and Check Key-Value Pairs
# DELETE: Delete Request, Get Status Code, GET Request and raise Error/not 200 status code

import requests
from flask import json
#import db models here
import sys
import os

SCRIPT_DIRP = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIRP))

from application.models import User,Ticket
BASE="http://127.0.0.1:5000"
url_ticket_all=BASE+"/api/ticketAll"
url_getResolutionTimes=BASE+"/api/getResolutionTimes"

def token_login_student():
    url=BASE+"/login"
    data={"email":"redding.abba@dollstore.org","password":"arya"}
    response=requests.post(url,data=data)
    return response.json()["token"]

def token_login_support_agent():
    url=BASE+"/login"
    data={"email":"chirag@chirag.com","password":"chirag"}
    response=requests.post(url,data=data)
    return response.json()["token"]

def token_login_admin():
    url=BASE+"/login"
    data={"email":"varun@varun.com","password":"varun"}
    response=requests.post(url,data=data)
    return response.json()["token"]
