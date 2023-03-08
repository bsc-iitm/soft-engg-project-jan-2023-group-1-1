from flask_restful import Resource, request, abort
from flask import jsonify
from datetime import datetime
from dateutil import tz, parser
from application.models import User, Student, Admin, Manager, Response, Ticket, token_required, db

class TicketAPI(Resource):
    def get(self):
        # TO-DO: Chirag
        pass

    def post(self):
        #TO-DO: Chirag
        pass

    def put(self):
        #TO-DO: Arya
        pass

    @token_required
    def delete(user, self):
        try:
            ticket_id = request.get_json()['ticket_id']
        except:
            abort(400, 'ticket_id must exist and should not be null')
        current_ticket = db.session.query(Ticket).filter(Ticket.ticket_id==ticket_id,Ticket.creator_id==user.user_id).first()
        if current_ticket:
            responses = db.session.query(Response).filter(Response.ticket_id==ticket_id).all()
            if responses:
                for post in responses:
                    db.session.delete(post)
                    db.session.commit() 
            db.session.delete(current_ticket)
            db.session.commit()
            return 200, "OK"
        else:
            abort(400, 'No such ticket_id exists for the user')
