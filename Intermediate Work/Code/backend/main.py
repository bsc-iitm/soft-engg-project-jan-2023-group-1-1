from application import app, api

from application.api import TicketAPI, ResponseAPI_by_ticket, ResponseAPI_by_response_id, ResponseAPI_by_user
api.add_resource(TicketAPI, '/api/ticket')
api.add_resource(ResponseAPI_by_ticket, '/api/respTicket') #For getting responses with ticket_id
api.add_resource(ResponseAPI_by_response_id, '/api/respResp') #For getting responses with response_id
api.add_resource(ResponseAPI_by_user, '/api/respUser') #For getting responses with user id.

from application.routes import *
if __name__ == '__main__':
  # Run the Flask app
  app.run(debug=True)