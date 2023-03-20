# Celery Tasks, FAQApi
# GET: Check Status Code and Key-Value Pairs
# POST/PATCH: Check Status Code, GET Request and Check Key-Value Pairs
# DELETE: Delete Request, Get Status Code, GET Request and raise Error/not 200 status code
import pytest
from application.tasks import send_email

# Send Email test case when html, subject and email id is correct
def test_send_email_all_parameters_okay():
    html = '<html> <p> Hi! </p> </html>'
    eid = 'calyx.keadon@dollstore.org'
    subject = 'This is a subject'
    email = (html,eid,subject)
    assert send_email(email) == 200

# Email variable should be a tuple of the form (html, email_address, subject)
def test_send_email_improper_tuple_supplied():
    html = '<html> <p> Hi! </p> </html>'
    subject = 'This is a subject'
    email = (html, subject)
    with pytest.raises(ValueError):
        send_email(email)

# Improper Email Address
def test_incorrect_email_address():
    html = '<html> <p> Hi! </p> </html>'
    subject = 'This is a subject'
    eid = 'abc'
    email = (html,eid,subject)
    assert send_email(email) == 400