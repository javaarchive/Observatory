from flask import Blueprint, jsonify, current_app, request
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from jinja2 import TemplateNotFound

from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

from snowflake import SnowflakeGenerator

import time, json

import queue

from extractors.all_extractors import create_instances

from dataclasses import dataclass

gen = SnowflakeGenerator(42)

engine = create_engine('sqlite:///database.db', echo=True) # use the file database.db in the current directory to make a database
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()

def make_jsonable(inp):
    print(dict(inp.__dict__))
    return dict(inp.__dict__)

# Models
@dataclass
class Product(Base):
    __tablename__ = 'products'
    id: str = Column(String(40), primary_key=True) # unique uuid ig
    name: str = Column(String(40))
    def __init__(self, name):
        self.id = next(gen)
        self.name = name
@dataclass
class Webpage(Base):
    __tablename__ = 'webpages'
    id: str = Column(String(40), primary_key=True) # unique uuid ig
    url: str = Column(String(100),unique=True)
    name: str = Column(String(50))
    productID: str = Column(String(40))
    def __init__(self, url, name, productID):
        self.id = next(gen)
        self.url = url
        self.name = name;
        self.productID = productID 

@dataclass
class WebpageDataResult(Base):
    __tablename__ = 'webpage_data'
    id: int = Column(BigInteger(), primary_key=True)
    webpage_id: str = Column(String(40)) 
    data: str = Column(String(2048)) # json encoded data
    date: str = Column(BigInteger()) # unix timestamp
    def __init__(self, webpage_id, data, date):
        self.id = next(gen)
        self.webpage_id = webpage_id
        self.data = data
        self.date = date

# scheduled task

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler(daemon = True)

print(scheduler)

is_fetching = False

extractors = create_instances()

current_webpages = []

newProductData = queue.Queue()

def data_fetch_loop():
    global is_fetching
    if is_fetching:
        return

    is_fetching = True

    print("Fetching data", current_webpages)

    webpages = current_webpages

    for webpage in webpages:
        print("Processing",webpage.id)
        try:
            price = next(filter(lambda ext: ext.is_valid_url(webpage.url),extractors)).extract_data(webpage.url)
            obj = {
                "webpage_id": webpage.id,
                "url": webpage.url,
                "name": webpage.name,
                "productID": webpage.productID,
                "price": price,
                "date": int(time.time()),
                "data": json.dumps({"price": price})
            }
            newProductData.put(obj)
            print("inserting",obj)
        except Exception as ex:
            print("Error processing", webpage.url, ex)

    is_fetching = False

job = scheduler.add_job(data_fetch_loop, 'interval', seconds=10)

scheduler.start()

# Routes

api = Blueprint('api', __name__)

@api.before_request
def syncThreads():
    global current_webpages
    current_webpages = db_session.query(Webpage).all()
    while(not newProductData.empty()):
        productData = newProductData.get()
        print("Adding new product data: ", productData)
        db_session.add(WebpageDataResult(productData["webpage_id"], productData["data"], productData["date"]))
        db_session.commit()

# when your browser wants the data for the the site item
@api.route('/all_webpages')
def everything():
    return jsonify(db_session.query(Webpage).all())

@api.route('/unschedule')
def unschedule():
    scheduler.remove_job(job.id)
    return jsonify({"success": True})

@api.route('/webpage/<id>')
def find_webpage(id):
    return jsonify(db_session.query(Webpage).filter_by(id=id).first()) # send data

@api.route('/product/<productID>',methods=['GET'])
def find_product(productID):
    return jsonify(db_session.query(Product).filter_by(id=productID).first()) # send data

@api.route('/product_name/<productName>',methods = ["POST"])
def add_product(productName):
    if db_session.query(Product).filter_by(name = productName).count() > 0:
        return jsonify({
            "status": "error",
            "message": "Product already exists"
        })
    product = Product(productName)
    db_session.add(product)
    db_session.commit()
    return jsonify({
       "status": "ok",
       "id": product.id
    })

@api.route('/add_webpage_for_product/<productName>',methods = ["POST"])
def add_webpage_for_product(productName):
    if db_session.query(Product).filter_by(name = productName).count() != 1:
        return jsonify({
            "status": "error",
            "message": "Product doesn't exist or has been entered multiple times (illegal)"
        })
    productID = db_session.query(Product).filter_by(name = productName).first()
    url = request.json['url']
    name = request.json['name']
    if db_session.query(Webpage).filter_by(url = url).count() > 0:
        return jsonify({
            "status": "error",
            "message": "Webpage with url already exists. "
        })
    webpage = Webpage(url,name,productID.id)
    db_session.add(webpage)
    db_session.commit()
    return jsonify({
         "status": "ok",
        "id": webpage.id
    })


@api.route('/webpages_for_product/<productID>')
def filter_webpages_by_product(productID):
    return jsonify(db_session.query(Webpage).filter_by(productID=productID).first()) # send data


Base.metadata.create_all(engine)
