from flask import Blueprint, jsonify, current_app
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from jinja2 import TemplateNotFound

from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

from snowflake import SnowflakeGenerator

gen = SnowflakeGenerator(42)

engine = create_engine('sqlite:///database.db', echo=True) # use the file database.db in the current directory to make a database
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()

# Models
class Product(Base):
    __tablename__ = 'products'
    id = Column(String(40), primary_key=True) # unique uuid ig
    name = Column(String(40))
    def __init__(self, name):
        self.id = gen.next()
        self.name = name
class Webpage(Base):
    __tablename__ = 'webpages'
    id = Column(String(40), primary_key=True) # unique uuid ig
    url = Column(String(100),unique=True)
    name = Column(String(50))
    productID = Column(String(40))
    def __init__(self, url, name, productID):
        self.id = gen.next()
        self.url = url
        self.name = name;
        self.productID = productID 

class WebpageDataResult(Base):
    __tablename__ = 'webpage_data'
    id = Column(BigInteger(), primary_key=True)
    webpage_id = Column(String(40)) 
    data = Column(String(2048)) # json encoded data
    date = Column(BigInteger()) # unix timestamp
    def __init__(self, webpage_id, data, date):
        self.id = gen.next()
        self.webpage_id = webpage_id
        self.data = data
        self.date = date


# Routes

api = Blueprint('api', __name__)

# when your browser wants the data for the the site item
@api.route('/all_webpages')
def everything():
    return jsonify(db_session.query(Webpage).all())

@api.route('/webpage/<id>')
def find_webpage(id):
    return jsonify(db_session.query(Webpage).filter_by(id=id).first()) # send data

@api.route('/product/<productID>',methods=['GET'])
def find_product(productID):
    return jsonify(db_session.query(Product).filter_by(id=productID).first()) # send data

@api.route('/product_name/<name>',methods = ["POST"])
def add_product(productName):
    if db_session.query(Product).filter_by(name = productName).count() > 0:
        return jsonify({
            "status": "error",
            "message": ""
        })
    product = Product(productName)
    db_session.add(product)
    db_session.commit()
    return jsonify({
       "status": "ok",
       "id": product.id
    })

@api.route('/webpages_for_product/<productID>')
def filter_webpages_by_product(productID):
    return jsonify(db_session.query(Webpage).filter_by(productID=productID).first()) # send data


Base.metadata.create_all(engine)
