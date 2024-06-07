import os
from flask import Flask, request,jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from application.controllers import register_resources
from flask_cors import CORS
from celery.schedules import crontab
from cache_config import make_cache
import tasks

app1 = None
api = None

def create_app():
    app1 = Flask(__name__, template_folder="templates")
    app1.secret_key = "NikhilAnand"
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app1.config.from_object(LocalDevelopmentConfig)

    # Configure JWT
    jwt = JWTManager(app1)
    app1.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this to a secure secret key
    app1.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']  # Set the expected token locations
    app1.config['JWT_ACCESS_COOKIE_PATH'] = '/'  # Specify the cookie path (adjust as needed)
    app1.config['JWT_COOKIE_SAMESITE'] = 'None'
    

    db.init_app(app1)

    # Use CORS to enable Cross-Origin Resource Sharing
    CORS(app1, origins='*')  # Allow requests from all origins


    return app1

app1 = create_app()
app1.app_context().push()
api = Api(app1)

cache = make_cache(app1)
app1.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app1.config['CELERY_BACKEND'] = 'redis://localhost:6379/0'

from celery_config import make_celery
celery = make_celery(app1)



# Register your API resources
register_resources(api)



if __name__ == '__main__':
    app1.run(host='0.0.0.0', port=5001)