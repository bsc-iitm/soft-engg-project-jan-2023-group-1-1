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

#TICKET ALL GET Request.

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

# TICKET ALL PATCH request

def test_ticket_all_patch():
    input_dict = { "number_of_upvotes": 146,"is_read": False, "ticket_id": 2}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_ticket_all,data=data, headers=header)
    assert request.status_code==200
    assert request.json()['message']=="success"
    ticket = Ticket.query.filter_by(ticket_id=input_dict["ticket_id"]).first()
    assert input_dict["number_of_upvotes"] == ticket.number_of_upvotes
    assert input_dict["is_read"] == ticket.is_read

def test_ticket_all_patch_ticket_not_found():
    input_dict = { "number_of_upvotes": 10023,"is_read": False, "ticket_id": 1e4}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_ticket_all,data=data, headers=header)
    assert request.status_code==404
    assert request.json()['message']=="There is no such ticket by that ID"

def test_ticket_all_patch_no_ticket_id():
    input_dict = { "number_of_upvotes": 10023,"is_read": False}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_ticket_all,data=data, headers=header)
    assert request.status_code==403
    assert request.json()['message']=="Please mention the ticketId field in your form"


def test_ticket_all_unauthenticated_patch():
    request=requests.patch(url_ticket_all)
    response=request.json()
    assert request.status_code==200
    assert response['status']=='unsuccessful, missing the authtoken'