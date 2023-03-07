from application import app, api

from application.api import TicketAPI
api.add_resource(TicketAPI, '/api/ticket')

from application.routes import *
if __name__ == '__main__':
  # Run the Flask app
  app.run(debug=True)