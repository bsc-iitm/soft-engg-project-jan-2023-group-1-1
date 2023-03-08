from application import app, api

from application.api import TicketAPI , UserAPI, FAQApi
api.add_resource(TicketAPI, '/api/ticket')
api.add_resource(UserAPI,'/api/user')
api.add_resource(FAQApi, '/api/faq')
from application.routes import *
if __name__ == '__main__':
  # Run the Flask app
  app.run(debug=True)