"""
    Dumitrescu Alexandra 343 C1 - SPRC - December 2023
"""
import routes
import time
from flask import Flask
from models import db


# method for initializing main server
def init_app():
    # configure app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']           = 'postgresql://postgre:postgre@db-postgres:5432/db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]    = False
    
    # set main routes for the app
    routes.set_routes(app=app)
    
    # initialize database with app
    db.init_app(app)

    # create tables in database
    with app.app_context():
        db.create_all()
    return app

if __name__ == '__main__':
    time.sleep(5)
    app = init_app()
    app.run(port=6000, host='0.0.0.0', debug=True)

