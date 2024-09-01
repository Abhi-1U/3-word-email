from dotenv import load_dotenv
from flask import Flask
from flask_session.__init__ import Session
from importlib import import_module
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def register_routes(app):
    for module_name in ('auth','home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def setup_cache_db(app):
    app.config['USE_SQLITE'] = True
    app.config['SECRET_KEY'] = os.environ.get("APP_SECRET_KEY")
    if not os.path.exists('/tmp/flask/cache'):
        os.makedirs('/tmp/flask/cache')
    basedir = "/tmp/flask/cache"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    db.init_app(app)

def create_cache_db(app):
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        print(e)


def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    register_routes(app)
    setup_cache_db(app)
    create_cache_db(app)
    return app