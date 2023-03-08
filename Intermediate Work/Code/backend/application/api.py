from flask_restful import Resource, request, abort
from flask import jsonify
from datetime import datetime
from dateutil import tz, parser
from application.models import User, Student, Admin, Manager, Response, Ticket
from application.models import token_required, db

class TicketAPI(Resource):
    def get(self):
        # TO-DO: Chirag
        pass
    
    def post(self):
        #TO-DO: Chirag
        pass
        
    @token_required
    def patch(user, self):
        #TO-DO: Arya
        args = request.get_json(force = True)
        a = None
        try:
            a = int(args["ticket_id"])
            print(a)
            print(user.user_id)
        except:
            abort(403, message = "Please mention the ticketId field in your form")
        ticket = None
        try:
            ticket = Ticket.query.filter_by(ticket_id = a, creator_id = user.user_id).first()
        except:
            abort(404, message = "There is no such ticket by that ID")
        title = None
        try:
            title = args["title"]
            ticket.title = title
        except:
            pass
        description = None
        try:
            description = args["description"]
            ticket.description = description
        except:
            pass
        number_of_upvotes = None

        try:
            number_of_upvotes = int(args["number_of_upvotes"])
            ticket.number_of_upvotes = number_of_upvotes
        except:
            pass
        is_read = None
        try:
            if args["is_read"] is not None:
                is_read = args["is_read"]
                ticket.is_read = is_read
        except:
            pass
        is_open = None
        try:
            if args["is_open"] is not None:
                is_open = args["is_open"]
                ticket.is_open = is_open
        except:
            pass
        is_offensive = None
        try:
            if args["is_offensive"] is not None:
                is_offensive = args["is_offensive"]
                ticket.is_offensive = is_offensive
        except:
            pass
        is_FAQ = None
        try:
            if args["is_FAQ"] is not None:
                is_FAQ = args["is_FAQ"]
                ticket.is_FAQ = is_FAQ
        except:
            pass   
        db.session.commit()
        return jsonify({"message": "success"})
        


        

    def delete(self):
        #TO-DO: Varun
        pass
