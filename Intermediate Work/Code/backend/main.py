from application import app, api, celery

from application.api import TicketAPI , UserAPI, FAQApi, ResponseAPI_by_ticket, ResponseAPI_by_response_id, ResponseAPI_by_user,TicketAll, getResolutionTimes
api.add_resource(TicketAPI, '/api/ticket')
api.add_resource(UserAPI,'/api/user')
api.add_resource(FAQApi, '/api/faq')
api.add_resource(ResponseAPI_by_ticket, '/api/respTicket') #For getting responses with ticket_id
api.add_resource(ResponseAPI_by_response_id, '/api/respResp') #For getting responses with response_id
api.add_resource(ResponseAPI_by_user, '/api/respUser') #For getting responses with user id.
api.add_resource(TicketAll, '/api/ticketAll') #For getting all tickets
api.add_resource(getResolutionTimes, '/api/getResolutionTimes') # For getting resolution times of support agents, only accessible to managers.
from application.routes import *
if __name__ == '__main__':
  # Run the Flask app
  app.run(debug=True)