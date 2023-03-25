## TicketAll, GetResolutionTimes, ResolutionTimes, FlaggPostAPI, ResponseAPI_by_ticket, getResponseAPI_by_ticket
# GET: Check Status Code and Key-Value Pairs
# POST/PATCH: Check Status Code, GET Request and Check Key-Value Pairs
# DELETE: Delete Request, Get Status Code, GET Request and raise Error/not 200 status code

import requests
from flask import json
#import db models here
import sys
import os
from datetime import datetime

SCRIPT_DIRP = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIRP))

from application.models import Ticket, Response
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

def token_login_manager():
    url = BASE+"/login"
    data = {"email": "boss@boss.com", "password": "boss"}
    response = requests.post(url, data = data)
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

#GETRESOLUTIONTIMES POST REQUEST

def test_getResolutionTimes_post_unauthenticated():
    request=requests.post(url_getResolutionTimes)
    response=request.json()
    assert request.status_code==200
    assert response['status']=='unsuccessful, missing the authtoken'

def test_getResolutionTimes_post_wrong_role():
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    input_dict = { "number_of_upvotes": 10023,"is_read": False, "ticket_id": 1e4}
    data = json.dumps(input_dict)
    request=requests.post(url = url_getResolutionTimes,data = data, headers=header)
    response = request.json()
    assert request.status_code == 404
    assert response["message"] == "You are not authorized to access this feature!"

def test_getResolutionTimes_post_no_ticket_id():
    header={"secret_authtoken":token_login_manager(), "Content-Type":"application/json"}
    input_dict = {}
    data = json.dumps(input_dict)
    request=requests.post(url = url_getResolutionTimes,data = data, headers=header)
    response = request.json()
    assert request.status_code == 403
    assert response["message"] == "Please enter the ticket ID."
    
def test_getResolutionTimes_post_ticket_isopen():
    header={"secret_authtoken":token_login_manager(), "Content-Type":"application/json"}
    input_dict = {"ticket_id": 1}
    data = json.dumps(input_dict)
    request=requests.post(url = url_getResolutionTimes,data = data, headers=header)
    response = request.json()
    assert request.status_code == 404
    assert response["message"] == "This ticket hasn't been responded to yet or is still open!"

def test_getResolutionTimes_post_wrong_ticket_id():
    header={"secret_authtoken":token_login_manager(), "Content-Type":"application/json"}
    input_dict = {"ticket_id": 1000}
    data = json.dumps(input_dict)
    request=requests.post(url = url_getResolutionTimes,data = data, headers=header)
    response = request.json()
    assert request.status_code == 404
    assert response["message"] == "No such ticket exists by the given ticket ID."

def test_getResolutionTimes_post():
    #Only checks if days, seconds, microseconds and ticket IDs match
    header={"secret_authtoken":token_login_manager(), "Content-Type":"application/json"}
    input_dict = {"ticket_id": [1,2]} 
    data = json.dumps(input_dict)
    request=requests.post(url = url_getResolutionTimes,data = data, headers=header)
    response = request.json()
    assert request.status_code == 200
    if isinstance(input_dict["ticket_id"], int):
        responses = Response.query.filter_by(ticket_id = input_dict["ticket_id"]).all()
        responses = list(responses)
        ticket = Ticket.query.filter_by(ticket_id = input_dict["ticket_id"]).first()
        a = {}
        response_times = []
        for thing in responses:
            if isinstance(thing.response_timestamp, datetime):
                #print("Here 1")
                response_times.append(thing.response_timestamp)
            elif isinstance(thing.response_timestamp, str):
                #print("Here 2")
                response_times.append(datetime.strptime(thing.response_timestamp,'%Y-%m-%d %H:%M:%S.%f'))
            response_time = max(response_times)
            a["creation_time"] = None
            if isinstance(ticket.creation_date, str):
                a["creation_time"] = datetime.strptime(ticket.creation_date, '%Y-%m-%d %H:%M:%S.%f')
            elif isinstance(ticket.creation_date, datetime):
                a["creation_time"] = ticket.creation_date
            a["response_time"] = response_time
            a["resolution_time_datetime_format"] = a["response_time"] - a["creation_time"]
            a["days"] = a["resolution_time_datetime_format"].days
            a["seconds"] = a["resolution_time_datetime_format"].seconds
            a["microseconds"] = a["resolution_time_datetime_format"].microseconds
            a["resolution_time_datetime_format"] = str(a["resolution_time_datetime_format"])
            a["creation_time"] = a["creation_time"]
            a["ticket_id"] = input_dict["ticket_id"]
            a["response_time"] = None
            a["resolution_time_datetime_format"] = None
            a["creation_time"] = None
        d = response["data"]
        for keys in a:
            if a[keys] is not None:
                assert a[keys] == d[keys]
    elif isinstance(input_dict["ticket_id"], list):
        data = []        
        for item in input_dict["ticket_id"]:
            d = {}
            ticket = None
            ticket = Ticket.query.filter_by(ticket_id = item).first()
            if ticket is None:
                continue
            if isinstance(ticket.creation_date, str):
                d["creation_time"] = datetime.strptime(ticket.creation_date, '%Y-%m-%d %H:%M:%S.%f')
            elif isinstance(ticket.creation_date, datetime):
                d["creation_time"] = ticket.creation_date
            responses = Response.query.filter_by(ticket_id = item).all()
            if ticket.is_open == False:
                responses = list(responses)
                response_times = []
                for thing in responses:
                    if isinstance(thing.response_timestamp, datetime):
                        response_times.append(thing.response_timestamp)
                    elif isinstance(thing.response_timestamp, str):
                        #print("Here 2")
                        response_times.append(datetime.strptime(thing.response_timestamp,'%Y-%m-%d %H:%M:%S.%f'))
                    
                response_time = max(response_times)
                d["response_time"] = response_time
                d["resolution_time_datetime_format"] = d["response_time"] - d["creation_time"]
                d["days"] = d["resolution_time_datetime_format"].days
                d["seconds"] = d["resolution_time_datetime_format"].seconds
                d["microseconds"] = d["resolution_time_datetime_format"].microseconds
                d["response_time"] = d["response_time"]
                d["resolution_time_datetime_format"] = str(d["resolution_time_datetime_format"])
                d["creation_time"] = d["creation_time"]
                d["ticket_id"] = item
                d["response_time"] = None
                d["resolution_time_datetime_format"] = None
                d["creation_time"] = None
                data.append(d)
        x = response["data"]
        for item in x:
            for thing in data:
                if item["ticket_id"] == thing["ticket_id"]:
                    for keys in thing:
                        if thing[keys] is not None:
                            assert thing[keys] == item[keys]


