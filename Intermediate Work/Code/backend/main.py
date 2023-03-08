from application import app, api

from application.api import TicketAPI , UserAPI
api.add_resource(TicketAPI, '/api/ticket')
api.add_resource(UserAPI,'/api/user')
from application.routes import *
if __name__ == '__main__':
  # Run the Flask app
  app.run(debug=True)