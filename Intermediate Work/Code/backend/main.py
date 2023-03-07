from application import app
from application.routes import *
if __name__ == '__main__':
  # Run the Flask app
  app.run(debug=True)