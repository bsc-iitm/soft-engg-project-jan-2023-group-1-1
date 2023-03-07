from flask_restful import Resource, request
from flask import jsonify
from datetime import datetime
from dateutil import tz, parser
from application.models import User, Student, Admin, Manager, Response, Ticket

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

    def delete(self):
        #TO-DO: Varun
        pass
