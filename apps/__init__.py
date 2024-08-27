from dotenv import load_dotenv
from flask import Flask
from flask_session.__init__ import Session
from importlib import import_module

def register_routes(app):
    for module_name in ('auth','home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    register_routes(app)
    return app