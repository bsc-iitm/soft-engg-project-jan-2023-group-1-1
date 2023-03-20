# Celery Tasks, FAQApi
# GET: Check Status Code and Key-Value Pairs
# POST/PATCH: Check Status Code, GET Request and Check Key-Value Pairs
# DELETE: Delete Request, Get Status Code, GET Request and raise Error/not 200 status code
import pytest
from application.tasks import send_email, response_notification
from application.tasks import celery
from celery import chain

#Send Email test case when html, subject and email id is correct
# def test_send_email_all_parameters_okay():
#     html = '<html> <p> Hi! </p> </html>'
#     eid = 'calyx.keadon@dollstore.org'
#     subject = 'This is a subject'
#     email = (html,eid,subject)
#     assert send_email.s(email).apply_async().get() == 200

# Email variable should be a tuple of the form (html, email_address, subject)
def test_send_email_improper_tuple_supplied():
    html = '<html> <p> Hi! </p> </html>'
    subject = 'This is a subject'
    email = (html, subject)
    with pytest.raises(ValueError):
        send_email.s(email).apply_async().get()

#Improper Email Address
def test_incorrect_email_address():
    html = '<html> <p> Hi! </p> </html>'
    subject = 'This is a subject'
    eid = 'abc'
    email = (html,eid,subject)
    assert send_email.s(email).apply_async().get() == 400

#All Fields properly defined for Response Notification, whatever error you get will be from 
def test_response_notfication_all_okay():
    ticket_obj = {'title': 'Problems with my ID Card', 'ticket_id': 1, 'creator_id': 1, 'creator_email': 'redding.abba@dollstore.org'}
    response_obj = {'responder_id': 2, 'response': 'test response', 'response_id': 17, 'responder_uname': 'chirag'}
    send_notification = chain(response_notification.s(ticket_obj = ticket_obj, response_obj=response_obj), send_email.s()).apply_async()
    assert send_notification.get() == 200

#One Or more keys missing from expected input
def test_response_notification_inadequate_data_passed():
    ticket_obj = {'title': 'Problems with my ID Card', 'ticket_id': 1, 'creator_id': 1,}
    response_obj = {'responder_id': 2, 'response': 'test response', 'response_id': 17, 'responder_uname': 'chirag'}
    send_notification = chain(response_notification.s(ticket_obj = ticket_obj, response_obj=response_obj), send_email.s()).apply_async()
    with pytest.raises(KeyError):
        send_notification.get()

