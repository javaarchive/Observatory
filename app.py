#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os

#----------------------------------------------------------------------------#
# App Configuration. This gets values from config.py so we have a easy place to change things. 
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.

# @app.teardown_request
# def shutdown_session(exception=None):
#    db_session.remove()


# Login required decorator.

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

# send about page from templates/placeholder.home.html
@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')

# send about page from templates/placeholder.about.html
@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

# login forms
@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

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