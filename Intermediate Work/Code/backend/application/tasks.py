from application.workers import celery
from flask import current_app as app
from application.models import db, User, Ticket, Response, Support_Agent
import requests
from datetime import datetime, timedelta
from celery.schedules import crontab

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=11, minute=30), unanswered_ticket_notification.s(), name='Daily Unanswered Ticket Reminder Reminder')


@celery.task()
def unanswered_ticket_notification():
    now = datetime.now()
    three_day_old_timestamp = now - timedelta(hours=72)
    unresolved_tickets = db.session.query(Ticket).filter(Ticket.is_open==1, Ticket.creation_date < three_day_old_timestamp).all()
    agents_user_ids = [a.user_id for a in db.session.query(User.user_id).filter(User.role_id==2).all() ]
    unanswered_tickets = []
    if unresolved_tickets:
        for ticket in unresolved_tickets:
            responses = ticket.responses
            flag = True
            for response in responses:
                if response.responder_id in agents_user_ids:
                    flag = False
                    break
            if flag:
                unanswered_tickets.append(ticket)
    
    if unanswered_tickets:
        html = '''
            <html>
            <head> The following tickets were created over 72 hours ago and still haven't been answered </head> 
            <body>
            <ol>
        '''
        for ticket in unanswered_tickets:
            html += f'<li> {ticket.title} created on {ticket.creation_date.strftime("%Y-%m-%d")} is still unanswered'
        html+= '</ol> </body> </html>'

        eid = db.session.query(User).filter(User.role_id==4).first().email_id
        subject = f'{len(unanswered_tickets)} ticket(s) older than 72 hours are yet to be answered'
        send_email.s((html, eid, subject)).apply_async()
        return "Notification Sent"
    return "All Tickets Answered"
                            
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