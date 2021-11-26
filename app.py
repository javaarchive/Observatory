#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
# from flask_login import LoginManager
import logging
from logging import Formatter, FileHandler
# from forms import *
import os



#----------------------------------------------------------------------------#
# App Configuration. This gets values from config.py so we have a easy place to change things. 
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')

# makes a database
db = SQLAlchemy(app)

from api import api,db_session,Product,Webpage,WebpageDataResult

# Automatically tear down SQLAlchemy.

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

# send about page from templates/home.html
@app.route('/')
def home():
    return render_template('pages/home.html', is_authenticated=(os.environ.get('ADMIN_SECRET') == request.cookies.get("secret")))

# send about page from templates/placeholder.about.html
@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/create_product')
def create_product():
    return render_template('pages/create_product.html')

@app.route('/edit_product/<id>')
def edit_product(id):
    return render_template('pages/edit_product.html')

@app.route('/add_webpage')
def add_webpage():
    return render_template('pages/add_webpage.html')

@app.route('/products')
def products():
    return render_template('pages/products.html')

@app.route('/try_login', methods = ['POST'])
def try_login():
    if os.environ.get('ADMIN_SECRET') == request.form.get("password"):
        response = redirect(url_for('products'))
        response.set_cookie('secret', os.environ.get('ADMIN_SECRET'))
        return response
    else:
        return redirect(url_for('home'))

# exit routes because stopping is broken
@app.route("/destroy")
def destroy():
    exit()
@app.route("/destroy2")
def destroy2():
    import sys
    sys.exit(0)

app.register_blueprint(api,url_prefix='/api')
app.config["SECRET_KEY"] = os.environ.get("SECRET")
if not os.environ.get("SECRET"):
    import random
    app.config["SECRET_KEY"] = "xxx" + str(random.randint(0,100000000000)) + "xxx"
app.config['FLASK_ADMIN_SWATCH'] = 'lumen'

admin = Admin(app, name='Observatory', template_mode='bootstrap3')
class RestrictedModelView(ModelView):

    def is_accessible(self):
        return request.cookies.get('secret') == os.environ.get("ADMIN_SECRET")

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('/', next=request.url))
admin.add_view(RestrictedModelView(Product, db_session))
admin.add_view(RestrictedModelView(Webpage, db_session))
admin.add_view(RestrictedModelView(WebpageDataResult, db_session))

# Error handlers.

# if an error happens above
@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


# not found page, if none of the above code runs
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    # controls messages appearing in the console/terminal
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # run our app at <our local ip>:<port>
    # in an actual machine without a firewall, our app will be visible to the entire world. 
    app.run(host='0.0.0.0', port=port) 