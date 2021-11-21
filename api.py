from flask import Blueprint, jsonify, current_app
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from jinja2 import TemplateNotFound

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///database.db', echo=True) # use the file database.db in the current directory to make a database
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()


api = Blueprint('api', __name__)

# when your browser wants the data for the the site item
@api.route('/<site>/<item>')
def show(site,item):
    return jsonify("someting") # send data

@api.route('/everything')
def everything():
    return jsonify("someting")

Base.metadata.create_all(engine)
