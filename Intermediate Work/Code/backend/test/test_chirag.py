# Ticket, User, ImportResourceUser Celery Task
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
url_ticket=BASE+"/api/ticket"

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

def test_response_check():
    response=requests.get(BASE)
    assert response.status_code==200
    
def test_ticket_student_get():
    header={"secret_authtoken":token_login_student()}
    request=requests.get(url_ticket,headers=header)
    ticket=Ticket.query.filter_by(creator_id=1).all()
    response=request.json()
    response=response['data']
    assert request.status_code==200
    for i in ticket:
        for j in response: 
            if(j["creator_id"]!=i.creator_id):
                assert j["ticket_id"]!=i.ticket_id
                assert j["title"]!=i.title
                assert j["description"]!=i.description
                assert j["creation_date"]!=i.creation_date
                assert j["number_of_upvotes"]!=i.number_of_upvotes
                assert j["is_read"]!=i.is_read
                assert j["is_open"]!=i.is_open
                assert j["is_FAQ"]!=i.is_FAQ
                assert j["is_offensive"]!=i.is_offensive
                assert j["rating"]!=i.rating

def test_ticket_admin_get():
    header={"secret_authtoken":token_login_admin()}
    request=requests.get(url_ticket,headers=header)
    assert request.status_code==403
    
def test_ticket_support_agent_get():
    header={"secret_authtoken":token_login_support_agent()}
    request=requests.get(url_ticket,headers=header)
    assert request.status_code==403
    
def test_ticket_student_post():
    header={"secret_authtoken":token_login_student(),"Content-Type":"application/json"}
    data={
        "title":"test1234",
        "description":"hi",
        "number_of_upvotes":13,
        "is_read":0,
        "is_open":1,
        "is_offensive":0,
        "is_FAQ":0
        }
    data=json.dumps(data)
    response=requests.post(url_ticket,data=data,headers=header)
    assert response.status_code==200
    response_get=requests.get(url_ticket,headers=header)
    response_get=response_get.json()
    response_get=response_get['data']
    for i in response_get:
        if(i["title"]=="test1234"):
            assert i["description"]=="hi"
            assert i["number_of_upvotes"]==13
            assert i["is_read"]==0
            assert i["is_open"]==1
            assert i["is_offensive"]==0
            assert i["is_FAQ"]==0
   
def test_ticket_admin_post():
    header={"secret_authtoken":token_login_admin(),"Content-Type":"application/json"}
    data={
        "title":"test1234",
        "description":"hi",
        "number_of_upvotes":13,
        "is_read":0,
        "is_open":1,
        "is_offensive":0,
        "is_FAQ":0
        }
    data=json.dumps(data)
    response=requests.post(url_ticket,data=data,headers=header)
    assert response.status_code==403
    
def test_ticket_support_agent_post():
    header={"secret_authtoken":token_login_support_agent(),"Content-Type":"application/json"}
    data={
        "title":"test1234",
        "description":"hi",
        "number_of_upvotes":13,
        "is_read":0,
        "is_open":1,
        "is_offensive":0,
        "is_FAQ":0
        }
    data=json.dumps(data)
    response=requests.post(url_ticket,data=data,headers=header)
    assert response.status_code==403
    
def test_ticket_title_student_patch():
    header={"secret_authtoken":token_login_student(),"Content-Type":"application/json"}
    payload={
        "ticket_id":3,
        "title":"test",
    }
    payload=json.dumps(payload)
    response=requests.patch(url_ticket,data=payload,headers=header)
    assert response.status_code==200
    response_get=requests.get(url_ticket,headers=header)
    response_get=response_get.json()
    response_get=response_get['data']
    for i in response_get:
        if(i["ticket_id"]==3):
            assert i["title"]=="test"
    
def test_ticket_admin_patch():
    header={"secret_authtoken":token_login_admin(),"Content-Type":"application/json"}
    payload={
        "ticket_id":3,
        "title":"test",
    }
    payload=json.dumps(payload)
    response=requests.patch(url_ticket,data=payload,headers=header)
    assert response.status_code==403
    
def test_ticket_support_agent_patch():
    header={"secret_authtoken":token_login_support_agent(),"Content-Type":"application/json"}
    payload={
        "ticket_id":3,
        "title":"test",
    }
    payload=json.dumps(payload)
    response=requests.patch(url_ticket,data=payload,headers=header)
    assert response.status_code==403
    
def test_ticket_student_delete():
    header={"secret_authtoken":token_login_student(),"Content-Type":"application/json"}
    payload={"ticket_id":3}
    payload=json.dumps(payload)
    response=requests.delete(url_ticket,data=payload,headers=header)
    assert response.status_code==200
    ticket=Ticket.query.filter_by(ticket_id=3).first()
    assert ticket==None
    
def test_ticket_admin_delete():
    header={"secret_authtoken":token_login_admin(),"Content-Type":"application/json"}
    payload={"ticket_id":1}
    payload=json.dumps(payload)
    response=requests.delete(url_ticket,data=payload,headers=header)
    assert response.status_code==400
    
def test_ticket_support_agent_delete():
    header={"secret_authtoken":token_login_support_agent(),"Content-Type":"application/json"}
    payload={"ticket_id":1}
    payload=json.dumps(payload)
    response=requests.delete(url_ticket,data=payload,headers=header)
    assert response.status_code==400
