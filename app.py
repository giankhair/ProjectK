from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

import os

load_dotenv()

mysql=SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config["SECRET_KEY"] = os.urandom(64)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'+os.getenv('DB_USER')+':'+os.getenv('DB_PASSWORD')+'@'+os.getenv('DB_HOST')+'/'+os.getenv('DB_NAME')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_POOL_SIZE"] = 10
    app.config["SQLALCHEMY_MAX_OVERFLOW"] = 20
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 1000

    mysql.init_app(app)
    
    from routes import pages
    app.register_blueprint(pages)
    
    return app





