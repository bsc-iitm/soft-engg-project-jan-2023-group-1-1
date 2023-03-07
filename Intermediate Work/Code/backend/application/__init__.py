from flask import Flask
from flask_cors import CORS
from application.config import LocalDevelopmentConfig
from application.models import db
# from application.models import User, Role
# from application import workers
# from flask_caching import Cache

app = None
# api = None
# celery = None
# cache = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    app.logger.info("App setup complete")
    db.create_all()  
    app.app_context().push() 
    # api = Api(app)
    # app.app_context().push() 
    CORS(app, resources={r'/*':{'origins':'*'}}) 
    app.app_context().push()    
    # create celery
    # celery = workers.celery
    # celery.conf.update(
    #     broker_url = app.config['CELERY_BROKER_URL'],
    #     result_backend = app.config['CELERY_RESULT_BACKEND']
    # )
    # celery.Task = workers.ContextTask
    # app.app_context().push() 

    # cache = Cache(app)
    # cache.clear()
    # app.app_context().push() 

    return app

app = create_app()
    