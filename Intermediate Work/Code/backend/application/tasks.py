from application.workers import celery
from flask import current_app as app
from application.models import db, User, Ticket, Response
import requests

@celery.task()
def response_notification(tid, rid):
    ticket_obj = db.session.query(Ticket).filter(Ticket.ticket_id==tid).first()
    response_obj = db.session.query(Response).filter(Response.response_id==rid).first()
    creator_obj = db.session.query(User).filter(User.user_id==ticket_obj.creator_id).first()
    responder_obj = db.session.query(User).filter(User.user_id==response_obj.responder_id).first()
    subject = f'There is a new response to your ticket {ticket_obj.title}'
    eid = creator_obj.email_id
    html = f'''
        <html> 
            <head>
                {responder_obj.user_name} has posted a respone to your ticket {ticket_obj.title}
            </head>
            <body>
                <blockquote>
                {response_obj.response}
                </blockquote>
            </body>
        </html>
    '''
    return html, eid, subject

@celery.task()
def send_email(email):
    html, eid, subject = email
    api_key = app.config['MAILGUN_API_KEY']
    api_url = 'https://api.mailgun.net/v3/iitm.venkatesh.xyz/messages'
    a = requests.post(
        api_url,
        auth=('api', api_key),
        data={
            'from': 'mailgun@iitm.venkatesh.xyz',
            'to': eid,
            'subject': subject,
            'html': html,
        }
    )
    return 200