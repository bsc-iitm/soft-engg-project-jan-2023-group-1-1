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

from application.models import Ticket
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

def test_ticket_all_get():
    header = {"secret_authtoken":token_login_student()}
    request=requests.get(url_ticket_all,headers=header)
    tickets = list(Ticket.query.filter_by().all())
    response = request.json()
    responses = response["data"]
    assert request.status_code==200
    for d in responses:
        for q in tickets:
            if q.ticket_id == d['ticket_id']:
                assert d['ticket_id'] ==  q.ticket_id
                assert d['title']==q.title
                assert d['description']==q.description
                assert d['creation_date']== str(q.creation_date)
                assert d['creator_id']==q.creator_id
                assert d['number_of_upvotes']==q.number_of_upvotes
                assert d['is_read']==q.is_read
                assert d['is_open']==q.is_open
                assert d['is_offensive']== q.is_offensive
                assert d['is_FAQ']==q.is_FAQ
                assert d['rating']==q.rating

def test_ticket_all_unauthenticated_get():
    request=requests.get(url_ticket_all)
    response=request.json()
    assert request.status_code==200
    assert response['status']=='unsuccessful, missing the authtoken'

