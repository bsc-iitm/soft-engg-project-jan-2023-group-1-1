from application.workers import celery
from flask import current_app as app
import requests

@celery.task()
def send_email(html, eid, subject):
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