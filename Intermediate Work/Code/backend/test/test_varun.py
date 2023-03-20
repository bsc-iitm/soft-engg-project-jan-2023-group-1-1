# # Celery Tasks, FAQApi
# # GET: Check Status Code and Key-Value Pairs
# # POST/PATCH: Check Status Code, GET Request and Check Key-Value Pairs
# # DELETE: Delete Request, Get Status Code, GET Request and raise Error/not 200 status code
import pytest
from application.tasks import send_email, response_notification, unanswered_ticket_notification
from application.tasks import celery
from celery import chain
from application.config import UnansweredNotificationSentConfig


# #Send Email test case when html, subject and email id is correct
# # def test_send_email_all_parameters_okay():
# #     html = '<html> <p> Hi! </p> </html>'
# #     eid = 'calyx.keadon@dollstore.org'
# #     subject = 'This is a subject'
# #     email = (html,eid,subject)
# #     assert send_email.s(email).apply_async().get() == 200

# # # Email variable should be a tuple of the form (html, email_address, subject)
# # def test_send_email_improper_tuple_supplied():
# #     html = '<html> <p> Hi! </p> </html>'
# #     subject = 'This is a subject'
# #     email = (html, subject)
# #     with pytest.raises(ValueError):
# #         send_email.s(email).apply_async().get()

# # #Improper Email Address
# # def test_incorrect_email_address():
# #     html = '<html> <p> Hi! </p> </html>'
# #     subject = 'This is a subject'
# #     eid = 'abc'
# #     email = (html,eid,subject)
# #     assert send_email.s(email).apply_async().get() == 400

# # #All Fields properly defined for Response Notification, whatever error you get will be from 
# # def test_response_notfication_all_okay():
# #     ticket_obj = {'title': 'Problems with my ID Card', 'ticket_id': 1, 'creator_id': 1, 'creator_email': 'redding.abba@dollstore.org'}
# #     response_obj = {'responder_id': 2, 'response': 'test response', 'response_id': 17, 'responder_uname': 'chirag'}
# #     send_notification = chain(response_notification.s(ticket_obj = ticket_obj, response_obj=response_obj), send_email.s()).apply_async()
# #     assert send_notification.get() == 200

# # #One Or more keys missing from expected input
# # def test_response_notification_inadequate_data_passed():
# #     ticket_obj = {'title': 'Problems with my ID Card', 'ticket_id': 1, 'creator_id': 1,}
# #     response_obj = {'responder_id': 2, 'response': 'test response', 'response_id': 17, 'responder_uname': 'chirag'}
# #     send_notification = chain(response_notification.s(ticket_obj = ticket_obj, response_obj=response_obj), send_email.s()).apply_async()
# #     with pytest.raises(KeyError):
# #         send_notification.get()

# # Unanswered Ticket Notification Sent
# def test_unanswered_ticket_notification_():
#     from application import app
#     app.config.from_object(UnansweredNotificationSentConfig)
#     app.app_context().push()
#     assert unanswered_ticket_notification() == 'Notification Sent'



import requests
from flask import json
#import db models here
import sys
import os
BASE="http://127.0.0.1:5000"

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

# FAQ ENDPOINT TESTING #
url_faq=BASE+"/api/faq"
from application.models import FAQ
from datetime import datetime
import dateutil.parser as dt
from flask import jsonify

# GET REQUEST FOR STUDENT #
def test_faq_authorized_get():
    header={"secret_authtoken":token_login_student()}
    request=requests.get(url_faq,headers=header)
    faqs=FAQ.query.all()
    response=request.json()
    responses=response['data']
    assert request.status_code==200
    for d in responses:
        for q in faqs:
            if q.ticket_id == d['ticket_id']:
                assert d['ticket_id'] ==  q.ticket_id
                assert d['category'] == q.category
                assert d['is_approved'] == q.is_approved
                assert d['title'] == q.ticket.title
                assert d['description'] == q.ticket.description
                # assert dt.parse(d['creation_date']) == q.ticket.creation_date
                assert d['creator_id'] == q.ticket.creator_id
                assert d['number_of_upvotes'] == q.ticket.number_of_upvotes
                assert d['is_read'] == q.ticket.is_read
                assert d['is_open'] == q.ticket.is_open
                assert d['is_offensive'] == q.ticket.is_offensive
                assert d['is_FAQ'] == q.ticket.is_FAQ
                assert d['rating'] == q.ticket.rating

def test_faq_inauthenticated_get():
    request=requests.get(url_faq)
    response=request.json()
    assert request.status_code==200
    assert response['status']=='unsuccessful, missing the authtoken'

## POST REQUEST ##
def test_faq_unauthorized_role_post():
    data = json.dumps({ "category": "operational","is_approved": False, "ticket_id": 2})
    header={"secret_authtoken":token_login_student(), "Content-Type":"application/json"}
    request=requests.post(url_faq,data=data, headers=header)
    assert request.status_code==403
    assert request.json()['message']=="Unauthorized"

def test_faq_inauthenticated_post():
    data = json.dumps({ "category": "operational","is_approved": False, "ticket_id": 2})
    header={"Content-Type":"application/json"}
    request=requests.post(url_faq,data=data)
    assert request.status_code==200
    assert request.json()['status']=='unsuccessful, missing the authtoken'

def test_faq_authorized_role_post_no_ticket_id():
    data = json.dumps({ "category": "operational","is_approved": False})
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.post(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="ticket_id is required and should be integer"

def test_faq_authorized_role_post_no_category():
    data = json.dumps({"is_approved": False, "ticket_id": 2})
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.post(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="category is required and should be string"

def test_faq_authorized_role_post_no_is_approved():
    data = json.dumps({ "category": "operational", "ticket_id": 2})
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.post(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="is_approved is required and should be boolean"

def test_faq_authorized_role_post_nonexistant_ticket_id():
    input_dict = { "category": "operational","is_approved": False, "ticket_id": 10000}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.post(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="ticket_id does not exist"
    assert FAQ.query.filter_by(ticket_id=input_dict["ticket_id"]).first() is None

def test_faq_authorized_role_post_nonexistant_category():
    input_dict = { "category": "abc","is_approved": False, "ticket_id": 2}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.post(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="category does not exist"
    assert FAQ.query.filter_by(ticket_id=input_dict["ticket_id"]).first() is None

def test_faq_authorized_role_post_invalid_isapproved():
    input_dict = { "category": "operational","is_approved": "abs", "ticket_id": 2}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.post(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="is_approved must be boolean"
    assert FAQ.query.filter_by(ticket_id=input_dict["ticket_id"]).first() is None

def test_faq_authorized_role_post_ticket_already_in_db():
    data = json.dumps({ "category": "operational","is_approved": False, "ticket_id": 1})
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.post(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="ticket already in FAQ"

def test_faq_authorized_role_post_valid_data():
    input_dict = { "category": "operational","is_approved": False, "ticket_id": 2}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.post(url_faq,data=data, headers=header)
    assert request.status_code==200
    assert request.json()['message']=="FAQ item added successfully"
    faq = FAQ.query.filter_by(ticket_id=2).first()
    assert input_dict["category"] == faq.category
    assert input_dict["is_approved"] == faq.is_approved

## DELETE REQUEST ##
delete_url = url_faq+'/2'

def test_faq_authorized_role_delete_valid():
    header={"secret_authtoken":token_login_admin()}
    request=requests.delete(delete_url, headers=header)
    assert request.status_code==200
    assert request.json()['message']=="FAQ item deleted successfully"
    assert FAQ.query.filter_by(ticket_id=2).first() is None

def test_faq_unauthorized_role_delete():
    header={"secret_authtoken":token_login_student()}
    request=requests.delete(delete_url, headers=header)
    assert request.status_code==403
    assert request.json()['message']=="Unauthorized"

def test_faq_inauthenticated_delete():
    request=requests.delete(delete_url)
    assert request.status_code==200
    assert request.json()['status']=='unsuccessful, missing the authtoken'

def test_faq_authorized_role_delete_nonexistant_ticket():
    header={"secret_authtoken":token_login_admin()}
    request=requests.delete(url_faq+'/1000', headers=header)
    assert request.status_code==400
    assert request.json()['message']=="ticket_id does not exist"

def test_faq_authroized_role_delete_ticket_not_in_faq():
    header={"secret_authtoken":token_login_admin()}
    request=requests.delete(url_faq+'/2', headers=header)
    assert request.status_code==400
    assert request.json()['message']=="ticket_id is not in FAQ"

## PATCH ## 

def test_faq_inauthenticated_patch():
    request=requests.patch(delete_url)
    assert request.status_code==200
    assert request.json()['status']=='unsuccessful, missing the authtoken'

def test_faq_unauthorized_role_patch():
    data = json.dumps({ "category": "operational","is_approved": False, "ticket_id": 2})
    header={"secret_authtoken":token_login_student(), "Content-Type":"application/json"}
    request=requests.patch(url_faq,data=data, headers=header)
    assert request.status_code==403
    assert request.json()['message']=="Unauthorized"

def test_faq_authorized_role_patch_no_ticket_id():
    data = json.dumps({ "category": "operational","is_approved": False})
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="ticket_id is required and should be integer"

def test_faq_authorized_role_patch_no_category():
    input_dict = {"is_approved": False, "ticket_id": 1}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_faq,data=data, headers=header)
    assert request.status_code==200
    assert request.json()['message']=="FAQ item updated successfully"
    assert input_dict["is_approved"]==FAQ.query.filter_by(ticket_id=1).first().is_approved

def test_faq_authorized_role_patch_no_is_approved():
    input_dict = { "category": "operational", "ticket_id": 1}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_faq,data=data, headers=header)
    assert request.status_code==200
    assert request.json()['message']=="FAQ item updated successfully"
    assert input_dict["category"] == FAQ.query.filter_by(ticket_id=1).first().category

def test_faq_authorized_role_patch_nonexistant_ticket_id():
    data = json.dumps({ "category": "operational","is_approved": False, "ticket_id": 10000})
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="ticket_id does not exist"
    assert not FAQ.query.filter_by(ticket_id=10000).first() 

def test_faq_authorized_role_patch_nonexistant_category():
    input_dict={ "category": "abc","is_approved": False, "ticket_id": 1}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="category does not exist"
    assert input_dict["category"] != FAQ.query.filter_by(ticket_id=1).first().category


def test_faq_authorized_role_patch_invalid_isapproved():
    input_dict = { "category": "operational","is_approved": "abs", "ticket_id": 1}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="is_approved must be boolean"
    assert input_dict["is_approved"] != FAQ.query.filter_by(ticket_id=1).first().is_approved


def test_faq_authorized_role_patch_valid_data():
    input_dict = { "category": "random","is_approved": False, "ticket_id": 1}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_faq,data=data, headers=header)
    assert request.status_code==200
    assert request.json()['message']=="FAQ item updated successfully"
    faq = FAQ.query.filter_by(ticket_id=1).first()
    assert input_dict["category"] == faq.category
    assert input_dict["is_approved"] == faq.is_approved